"""Verify an explicit local or public release ZIP and checksum without executing it."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile


def verify_pair(archive,checksum):
    archive,checksum=Path(archive),Path(checksum)
    fields=checksum.read_text(encoding='utf-8').strip().split()
    if len(fields)!=2 or not re.fullmatch('[0-9a-fA-F]{64}',fields[0]) or fields[1].lstrip('*')!=archive.name:
        raise ValueError('Checksum must identify exactly the expected ZIP filename')
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest!=fields[0].lower():raise ValueError('Published ZIP checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            path=PurePosixPath(info.filename)
            if path.is_absolute() or '..' in path.parts or '\\' in info.filename or ':' in info.filename:
                raise ValueError('Unsafe ZIP member')
        if z.testzip() is not None:raise ValueError('Corrupt ZIP payload')
    checks=[]
    native_path=archive.resolve().as_posix()
    for name,args in [('sha256sum',['sha256sum',native_path]),('shasum',['shasum','-a','256',native_path])]:
        if not shutil.which(name):checks.append({'tool':name,'outcome':'not_run'});continue
        value=subprocess.check_output(args,text=True).split()[0].lower()
        if value!=digest:raise ValueError(f'{name} differs from published checksum')
        checks.append({'tool':name,'outcome':'passed'})
    if shutil.which('pwsh'):
        with tempfile.TemporaryDirectory() as temporary:
            script=Path(temporary)/'checksum.ps1'
            script.write_text('param([string]$Artifact)\n(Get-FileHash -LiteralPath $Artifact -Algorithm SHA256).Hash.ToLowerInvariant()\n')
            value=subprocess.check_output(['pwsh','-NoProfile','-NonInteractive','-File',str(script),'-Artifact',str(archive.resolve())],text=True).strip()
            if value!=digest:raise ValueError('PowerShell Get-FileHash mismatch')
        checks.append({'tool':'PowerShell Get-FileHash','outcome':'passed'})
    else:checks.append({'tool':'PowerShell Get-FileHash','outcome':'not_run'})
    return {'verified':True,'artifact':archive.name,'sha256':digest,'bytes':archive.stat().st_size,'native_checks':checks}


def download(repo,tag,output):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+',tag):
        raise ValueError('Expected owner/repo and stable vMAJOR.MINOR.PATCH tag')
    if output.exists() and any(output.iterdir()):raise ValueError('Download directory must be empty')
    output.mkdir(parents=True,exist_ok=True)
    name=f'opendevguild-{tag[1:]}.zip'
    urls=[]
    for filename in [name,name+'.sha256']:
        url=f'https://github.com/{repo}/releases/download/{tag}/{filename}'
        # Ordinary anonymous HTTPS: no token, cookie or credential is supplied.
        with urllib.request.urlopen(url,timeout=30) as response:
            data=response.read(32*1024*1024+1)
        if len(data)>32*1024*1024:raise ValueError('Release artifact exceeds bounded download size')
        with (output/filename).open('xb') as stream:stream.write(data)
        urls.append(url)
    report=verify_pair(output/name,output/(name+'.sha256'));report['public_urls']=urls
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--zip',type=Path);p.add_argument('--checksum',type=Path)
    p.add_argument('--repo',default=os.environ.get('GITHUB_REPOSITORY','kkshiiit/opendevguild'))
    p.add_argument('--tag',default=os.environ.get('ODG_RELEASE_TAG'))
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        if a.zip and a.checksum:result=verify_pair(a.zip,a.checksum)
        elif a.tag and a.output:result=download(a.repo,a.tag,a.output)
        else:p.error('Provide --zip/--checksum or --tag/--output')
        print(json.dumps(result,indent=2))
    except (OSError,ValueError,subprocess.SubprocessError,zipfile.BadZipFile) as error:p.exit(1,f'{error}\n')


if __name__=='__main__':main()
