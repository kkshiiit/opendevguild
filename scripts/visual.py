"""Visual library validation and bounded measurements; no aesthetic oracle."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]


def contrast(foreground, background):
    """WCAG relative-luminance ratio for two opaque, already-composited sRGB colors."""
    def luminance(value):
        if not isinstance(value,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',value):
            raise ValueError('Use opaque six-digit sRGB; composite transparency on its actual background first')
        channels=[int(value[i:i+2],16)/255 for i in (1,3,5)]
        linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c,w in zip(linear,(0.2126,0.7152,0.0722)))
    left,right=sorted((luminance(foreground),luminance(background)))
    return (right+0.05)/(left+0.05)


def pixel_diff(left,right,region=None):
    """Count exact RGBA changes; callers must match browser/font/render conditions."""
    from PIL import Image,ImageChops
    with Image.open(left) as a,Image.open(right) as b:
        if a.size!=b.size: raise ValueError('Screenshot dimensions differ; comparison is invalid')
        a,b=a.convert('RGBA'),b.convert('RGBA')
        if region is not None:
            if len(region)!=4 or any(type(v) is not int for v in region) or min(region)<0 or region[2]*region[3]==0 or region[0]+region[2]>a.width or region[1]+region[3]>a.height:
                raise ValueError('Invalid comparison region')
            x,y,width,height=region
            a,b=a.crop((x,y,x+width,y+height)),b.crop((x,y,x+width,y+height))
        delta=ImageChops.difference(a,b)
        total=a.width*a.height
        channels=delta.split()
        mask=channels[0]
        for channel in channels[1:]:mask=ImageChops.lighter(mask,channel)
        changed=total-mask.histogram()[0]
    return {'changed_pixels':changed,'total_pixels':total,'changed_fraction':changed/total,'region':region,
            'interpretation':'pixel change only; no aesthetic or functional verdict'}


def material_errors(material):
    errors=[]
    if material.get('class') not in ('stylized_glass','simulated_dynamic_glass','native_official'):
        errors.append('Unknown material class')
    if material.get('class')=='native_official' and (material.get('platform') not in ('ios','macos','ipados')
            or material.get('api') not in ('SwiftUI glassEffect','UIKit UIGlassEffect','AppKit NSGlassEffectView')):
        errors.append('Native Apple material needs an actual supported Apple platform and official API')
    if material.get('class')=='native_official':
        supported={'SwiftUI glassEffect':{'ios','macos','ipados'},'UIKit UIGlassEffect':{'ios','ipados'},'AppKit NSGlassEffectView':{'macos'}}
        if material.get('platform') not in supported.get(material.get('api'),set()):
            errors.append('Native API does not match target platform')
        if not isinstance(material.get('target_version'),str) or not material['target_version'].strip():
            errors.append('Declare supported target OS/SDK version and availability guards')
    if not material.get('evidence'): errors.append('Material approval needs rendered evidence, not code inspection alone')
    return errors


def checked_file(root,value):
    root=Path(root)
    if root.is_symlink():raise ValueError('Symlink source root')
    if not isinstance(value,str) or not value or '\\' in value or ':' in value:
        raise ValueError('Artifact must be a relative project path')
    path=root/value
    if Path(value).is_absolute() or '..' in Path(value).parts or path.is_symlink():
        raise ValueError('Unsafe visual artifact path')
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Visual artifact is missing or outside the project')
    cursor=path
    while cursor!=root:
        if cursor.is_symlink(): raise ValueError('Symlink in artifact path')
        cursor=cursor.parent
    return path


def schema_errors(root,name,value):
    schema=json.loads((root/'visual/schemas'/name).read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return [f'{list(e.path)}: {e.message}' for e in Draft202012Validator(schema).iter_errors(value)]


def reference_errors(root,item):
    errors=schema_errors(root,'reference.schema.json',item)
    if errors:return errors
    if not item['visual_reference']['inspected']:errors.append('Reference not visually inspected')
    if not item['license']['redistribution_allowed']:errors.append('No sufficient redistribution rights')
    try:
        path=checked_file(root,item['visual_reference']['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['visual_reference']['sha256']:
            errors.append('Reference image hash mismatch')
        source=checked_file(root,item['provenance']['source_path'])
        if hashlib.sha256(source.read_bytes()).hexdigest()!=item['provenance']['source_sha256']:
            errors.append('Reference source hash mismatch')
    except (OSError,ValueError) as error:errors.append(str(error))
    return errors


def split_errors(development,evaluation):
    errors=[]
    for key in ('id','image','source'):
        def identities(records):
            if key=='id':return {r['id'] for r in records}
            if key=='image':return {r['visual_reference']['sha256'] for r in records}
            return {r['provenance']['source_sha256'] for r in records}
        if identities(development)&identities(evaluation):errors.append(f'Development/evaluation share {key} identity')
    return errors


def environment_errors(left,right):
    keys=('browser','platform','viewport','device_scale_factor','color_scheme','reduced_motion','font_policy','state')
    return [f'Missing or different render condition: {key}' for key in keys
            if key not in left or key not in right or left[key]!=right[key]]


def antipattern_errors(observation,root=ROOT):
    errors=[]
    known={r['id'] for r in json.loads((root/'visual/antipatterns.json').read_text())}
    if observation.get('id') not in known:errors.append('Unknown antipattern')
    for key in ('context','task_impact','legitimate_use'):
        if not observation.get(key):errors.append(f'Antipattern observation missing {key}')
    if observation.get('decision') not in ('candidate','confirmed','justified_use'):
        errors.append('Unknown observation decision')
    if observation.get('decision')=='confirmed' and not observation.get('task_evidence'):
        errors.append('Confirmed defect needs task evidence, not appearance alone')
    if not observation.get('evidence'):errors.append('Visible evidence required')
    for evidence in observation.get('evidence',[]):
        try:
            path=checked_file(root,evidence['path'])
            data=path.read_bytes()
            if not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Evidence must be an inspected PNG')
            if hashlib.sha256(data).hexdigest()!=evidence['sha256']:errors.append('Evidence hash mismatch')
            width,height=struct.unpack('>II',data[16:24])
            region=evidence['region']
            if not isinstance(region,list) or len(region)!=4 or any(type(v) is not int for v in region):
                errors.append('Region requires integer x,y,width,height')
            elif min(region)<0 or region[2]==0 or region[3]==0 or region[0]+region[2]>width or region[1]+region[3]>height:
                errors.append('Evidence region outside actual capture')
        except (OSError,ValueError,KeyError,TypeError,struct.error) as error:errors.append(str(error))
    return errors


def feedback_errors(feedback,known):
    errors=[]
    if feedback.get('reviewer_kind')!='human':errors.append('Human preference must come from a human, not an agent')
    alternatives=feedback.get('alternatives',[])
    if len(alternatives)!=2 or len(set(alternatives))!=2 or not set(alternatives)<=known:
        errors.append('Two known distinct alternatives required')
    if feedback.get('choice') not in alternatives+['tie','neither']:errors.append('Unknown preference choice')
    if not isinstance(feedback.get('rationale'),str) or len(feedback['rationale'].strip())<12:
        errors.append('Specific human rationale required')
    if set(feedback.get('presentation_order',[]))!=set(alternatives):errors.append('Record actual presentation order')
    if feedback.get('consent_to_store') is not True:errors.append('No consent to retain pseudonymous feedback')
    if '@' in feedback.get('reviewer_id',''):errors.append('Use pseudonymous reviewer ID, not email')
    return errors


def correction_errors(correction,root=ROOT):
    errors=[]
    root=Path(root)
    for field in ('original_design','problem','proposed_correction','justification','result','evaluation','regression'):
        if not correction.get(field):errors.append(f'Correction missing {field}')
    if correction.get('status')!='validated':errors.append('Correction is still a proposal')
    if not correction.get('reviewer') or correction.get('reviewer')==correction.get('author'):
        errors.append('Independent reviewer required')
    if correction.get('review_decision')!='APPROVED':errors.append('Correction review not approved')
    if correction.get('split')!='development':errors.append('Holdout observations cannot be promoted into development rules')
    if correction.get('regression_status')!='passed' or not correction.get('result_evidence'):
        errors.append('Post-change render and passing regression required')
    development=json.loads((root/'visual/data/development.json').read_text())
    evaluation=json.loads((root/'visual/data/evaluation.json').read_text())
    if correction.get('original_design') not in {r['id'] for r in development}:
        errors.append('Original design must identify a development reference')
    heldout_images={r['visual_reference']['sha256'] for r in evaluation}
    heldout_sources={r['provenance']['source_sha256'] for r in evaluation}
    for evidence in correction.get('result_evidence',[]):
        if not isinstance(evidence,dict) or set(evidence)!={'path','sha256','capture_manifest'}:
            errors.append('Correction evidence needs render path, SHA-256 and capture manifest');continue
        try:
            artifact=checked_file(root,evidence['path'])
            if hashlib.sha256(artifact.read_bytes()).hexdigest()!=evidence['sha256']:
                errors.append('Correction evidence hash mismatch')
            if evidence['sha256'] in heldout_images:errors.append('Known holdout render cannot be promoted')
            if artifact.suffix!='.png':raise ValueError('Correction needs actual PNG render evidence')
            try:from PIL import Image
            except ImportError:raise ValueError('Install optional visual dependencies to decode correction render')
            with Image.open(artifact) as image:image.verify()
            manifest_path=checked_file(root,evidence['capture_manifest'])
            manifest=json.loads(manifest_path.read_text())
            if any(not manifest.get(key) for key in ('browser','platform','font_policy')):
                errors.append('Capture environment is incomplete')
            matches=[entry for entry in manifest.get('captures',[]) if (manifest_path.parent/entry['path']).resolve()==artifact.resolve() and entry['sha256']==evidence['sha256']]
            if not matches:errors.append('Render is not bound to this capture manifest')
            for entry in matches:
                if entry['source_sha256'] in heldout_sources:errors.append('Holdout source cannot be relabeled for promotion')
                source=checked_file(root,entry['source_path'])
                if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['source_sha256']:
                    errors.append('Capture source is stale')
        except (OSError,ValueError,KeyError,TypeError) as error:errors.append(str(error))
    return errors


def validate_library(root):
    root=Path(root); errors=[];datasets={}
    for split in ('development','evaluation'):
        path=root/'visual/data'/f'{split}.json'
        try:records=json.loads(path.read_text(encoding='utf-8'))
        except (OSError,ValueError) as error:errors.append(str(error));continue
        if not isinstance(records,list) or not records:errors.append(f'{split} needs inspected references');continue
        datasets[split]=records
        seen=set()
        for item in records:
            if not isinstance(item,dict):errors.append(f'{split}: malformed reference');continue
            errors.extend(f'{split}/{item.get("id")}: {e}' for e in reference_errors(root,item))
            if item.get('id') in seen:errors.append('Duplicate reference ID')
            seen.add(item.get('id'))
    if len(datasets)==2 and not errors:errors+=split_errors(datasets['development'],datasets['evaluation'])
    known={item.get('id') for records in datasets.values() for item in records if isinstance(item,dict)}
    for name in ('feedback','corrections'):
        try:records=json.loads((root/'visual/data'/f'{name}.json').read_text(encoding='utf-8'))
        except (OSError,ValueError) as error:errors.append(str(error));continue
        if not isinstance(records,list):errors.append(f'{name} must be an array');continue
        for record in records:
            if name=='feedback':
                structure=schema_errors(root,'feedback.schema.json',record);errors+=structure
                if not structure:errors+=feedback_errors(record,known)
            else:
                structure=schema_errors(root,'correction.schema.json',record);errors+=structure
                # Proposals are allowed in the log, but never silently promoted.
                if not structure and record.get('status')=='validated':errors+=correction_errors(record,root)
    try:
        catalog=json.loads((root/'visual/antipatterns.json').read_text(encoding='utf-8'))
        if len(catalog)!=12:errors.append('Expected twelve contextual antipatterns')
        for item in catalog:
            for field in ('id','signal','evidence_required','task_impact','legitimate_use'):
                if not item.get(field):errors.append(f'Antipattern missing {field}')
    except (OSError,ValueError) as error:errors.append(str(error))
    try:
        observations=json.loads((root/'visual/data/observations.json').read_text())
        for observation in observations:errors+=antipattern_errors(observation,root)
    except (OSError,ValueError,TypeError) as error:errors.append(str(error))
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('validate')
    ratio=commands.add_parser('contrast');ratio.add_argument('foreground');ratio.add_argument('background')
    diff=commands.add_parser('diff');diff.add_argument('left',type=Path);diff.add_argument('right',type=Path)
    for name in ('check-correction','check-feedback'):
        command=commands.add_parser(name);command.add_argument('file',type=Path)
    args=parser.parse_args()
    try:
        if args.command=='contrast':print(json.dumps({'ratio':contrast(args.foreground,args.background)}));return 0
        if args.command=='diff':print(json.dumps(pixel_diff(args.left,args.right),indent=2));return 0
        if args.command=='validate':errors=validate_library(args.root)
        elif args.command=='check-correction':
            record=json.loads(args.file.read_text());errors=schema_errors(args.root,'correction.schema.json',record)
            if not errors:errors=correction_errors(record,args.root)
        else:
            known={r['id'] for split in ('development','evaluation') for r in json.loads((args.root/'visual/data'/f'{split}.json').read_text())}
            record=json.loads(args.file.read_text());errors=schema_errors(args.root,'feedback.schema.json',record)
            if not errors:errors=feedback_errors(record,known)
        print(json.dumps({'errors':errors,'limitations':'Validates declared evidence, not truth, aesthetics or model weights'},indent=2))
        return 1 if errors else 0
    except (OSError,ValueError,KeyError,TypeError) as error:parser.exit(2,f'{error}\n')


if __name__=='__main__':raise SystemExit(main())
