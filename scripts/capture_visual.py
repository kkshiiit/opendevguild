"""Render original local fixtures; no external pages or inferred native support."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import statistics
import time

ROOT = Path(__file__).resolve().parents[1]


def capture(output, chromium=None):
    from playwright.sync_api import sync_playwright
    from visual import contrast, pixel_diff
    if output.exists() and any(output.iterdir()):
        raise ValueError('Capture destination must be empty; existing goldens are preserved')
    output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    result = {'kind': 'actual Chromium fixture observations', 'platform': platform.platform(),
              'viewport_units': 'CSS px', 'device_scale_factor': 1,
              'font_policy': 'installed system-ui and Georgia; await document.fonts.ready',
              'captures': [], 'checks': [], 'external_requests': [], 'limitations': [
                  'Web fixtures only; not Android, iOS, desktop-native or a game runtime.',
                  'Token contrast pairs do not establish complete WCAG conformance.',
                  'Draw timing is this machine Canvas2D CPU-call timing, not end-to-end GPU frame time.',
                  'Pixel equality is a reproducibility check, not aesthetic quality or material fidelity approval.']}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=chromium)
        result['browser'] = browser.version
        for direction in ('a', 'b'):
            for width, height in ((1360, 960), (390, 844)):
                page = browser.new_page(viewport={'width': width, 'height': height},
                                        device_scale_factor=1, color_scheme='light', reduced_motion='reduce')
                page.on('request', lambda req: result['external_requests'].append(req.url)
                        if req.url.startswith(('https:', 'http:')) else None)
                path = ROOT / 'visual/fixtures/interface.html'
                # This managed browser blocks file:// navigation. Inline our own
                # self-contained fixture; no policy bypass or external resource.
                page.set_content(path.read_text(encoding='utf-8'))
                page.evaluate('(direction) => document.documentElement.dataset.direction=direction', direction)
                page.evaluate('document.fonts.ready')
                identifier = f'direction-{direction}-{width}'
                screenshot = output / f'{identifier}.png'
                page.screenshot(path=str(screenshot), full_page=True, animations='disabled')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), identifier
                result['checks'].append({'check': f'{identifier}: no horizontal overflow', 'outcome': 'passed'})
                result['captures'].append({'id': identifier, 'path': screenshot.name,
                                           'source_path': 'visual/fixtures/interface.html',
                                           'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                           'viewport': [width, height], 'direction': direction,
                                           'sha256': hashlib.sha256(screenshot.read_bytes()).hexdigest()})
                if direction == 'a' and width == 1360:
                    repeat = output / 'repeat-a.png'
                    page.screenshot(path=str(repeat), full_page=True, animations='disabled')
                    result['repeat_pixel_diff'] = pixel_diff(screenshot, repeat)
                    assert result['repeat_pixel_diff']['changed_pixels'] == 0
                    page.locator('#reserve').click()
                    assert page.locator('#status').inner_text() == 'Visit requested. Nothing was sent.'
                    page.screenshot(path=str(output/'interactive-state.png'), full_page=True)
                    result['checks'].append({'check': 'local request state transition', 'outcome': 'passed'})
                    page.locator('#motion').click()
                    assert not page.evaluate('window.glassAnimating')
                    result['checks'].append({'check': 'reduced motion prevents Canvas animation', 'outcome': 'passed'})
                    page.locator('#material-toggle').click()
                    page.screenshot(path=str(output/'simulated-material.png'), full_page=True)
                    page.evaluate('window.drawMaterial(25)')
                    page.screenshot(path=str(output/'simulated-material-shifted.png'), full_page=True)
                    diff = pixel_diff(output/'simulated-material.png', output/'simulated-material-shifted.png')
                    bounds=page.locator('#material').evaluate('(el)=>{let r=el.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height}}')
                    region=[round(bounds['x']+bounds['w']*.30),round(bounds['y']+bounds['h']*.32),round(bounds['w']*.40),round(bounds['h']*.36)]
                    pane_diff=pixel_diff(output/'simulated-material.png',output/'simulated-material-shifted.png',region=region)
                    assert pane_diff['changed_pixels'] > 0
                    result['material_full_page_change_informational'] = diff
                    result['material_pane_response'] = pane_diff
                    result['checks'].append({'check': 'sampled material reacts to changed source pixels', 'outcome': 'passed'})
                    result['canvas_draw_ms'] = page.evaluate('''() => {let x=[];for(let i=0;i<32;i++){let t=performance.now();window.drawMaterial(i);x.push(performance.now()-t)}return x}''')
                    result['canvas_draw_median_ms'] = statistics.median(result['canvas_draw_ms'])
                    page.keyboard.press('Tab')
                    focused = page.evaluate('document.activeElement.id || document.activeElement.tagName')
                    result['keyboard_focus_observed'] = focused
                    result['checks'].append({'check': 'focusable controls available', 'outcome': 'passed' if focused != 'BODY' else 'failed'})
                    result['backdrop_filter_supported'] = page.evaluate('CSS.supports("backdrop-filter", "blur(10px)")')
                    result['contrast_pairs'] = [{'foreground': fg, 'background': bg, 'ratio': contrast(fg, bg), 'threshold': 4.5}
                                                for fg, bg in [('#203229', '#f5f3ed'), ('#536357', '#f5f3ed'), ('#ffffff', '#18513b')]]
                    assert all(pair['ratio'] >= pair['threshold'] for pair in result['contrast_pairs'])
                    page.emulate_media(color_scheme='dark')
                    page.screenshot(path=str(output/'dark-state.png'), full_page=True)
                    result['checks'].append({'check': 'dark theme rendered; contrast pairs measured separately', 'outcome': 'passed'})
                    result['contrast_pairs'].extend({'foreground':fg,'background':bg,'ratio':contrast(fg,bg),'threshold':4.5}
                                                    for fg,bg in [('#edf3eb','#14231b'),('#bccbbd','#14231b'),('#ffffff','#246547')])
                page.close()
        holdout = ROOT / 'visual/fixtures/holdout.html'
        page = browser.new_page(viewport={'width':1360,'height':960}, reduced_motion='reduce')
        page.set_content(holdout.read_text(encoding='utf-8')); page.evaluate('document.fonts.ready')
        path = output / 'holdout.png'; page.screenshot(path=str(path),full_page=True)
        result['captures'].append({'id':'holdout-maintenance','path':path.name,'source_path':'visual/fixtures/holdout.html',
                                   'source_sha256':hashlib.sha256(holdout.read_bytes()).hexdigest(),
                                   'viewport':[1360,960],'direction':'holdout','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        page.close()
        context = browser.new_context(viewport={'width':700,'height':500}, record_video_dir=str(output/'video-temp'),
                                      record_video_size={'width':700,'height':500}, reduced_motion='no-preference')
        page = context.new_page(); page.set_content((ROOT/'visual/fixtures/interface.html').read_text(encoding='utf-8'))
        page.locator('#material-toggle').click(); page.locator('#material').scroll_into_view_if_needed()
        page.locator('#motion').click(); page.wait_for_timeout(650)
        frames = page.evaluate('window.glassFrames'); assert frames > 2
        result['animation_draw_calls_observed'] = frames
        video = page.video; context.close()
        video.save_as(str(output/'material-motion.webm'))
        shutil.rmtree(output/'video-temp')
        browser.close()
    assert not result['external_requests']
    assert all(pair['ratio'] >= pair['threshold'] for pair in result['contrast_pairs'])
    result['elapsed_seconds'] = time.perf_counter() - started
    result['human_preference'] = 'not_run: no human ratings supplied'
    (output/'capture.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--chromium',help='Explicit installed Chromium executable, otherwise Playwright-managed browser')
    args=parser.parse_args()
    try: result=capture(args.output,args.chromium)
    except (ValueError,ImportError) as error: parser.exit(2,f'{error}\n')
    print(json.dumps({'captures':len(result['captures']),'checks':len(result['checks']),
                      'seconds':result['elapsed_seconds'],'browser':result['browser']},indent=2))


if __name__=='__main__':main()
