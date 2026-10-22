"""Reusable visuals pipeline for Zenn articles about NovaSolver simulators.

Usage:
    python make_visuals_template.py <slug> <title_line1> <title_line2> <subtitle> [<slider_id_hint>]

Generates 5 files in E:\\NovaSolver\\zenn-content\\images\\<slug>\\:
  - cover.png (1200x630 with title overlay + chart preview)
  - full-view.png (PC full screenshot)
  - charts-closeup.png (chart area cropped)
  - stats.png (stat-cards if present)
  - slider-anim.gif (slider operation animation)
"""
import os, sys, time, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont

def make(slug, title1, title2, subtitle, slider_hint=''):
    REPO = r'E:\NovaSolver\zenn-content'
    OUT = os.path.join(REPO, 'images', slug)
    os.makedirs(OUT, exist_ok=True)
    URL = f'https://novasolver.jp/tools/{slug}.html?t={int(time.time())}'

    def driver(w=1400, h=2400):
        opts = Options()
        opts.add_argument('--headless=new')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-gpu')
        opts.add_argument(f'--window-size={w},{h}')
        opts.add_argument('--hide-scrollbars')
        d = webdriver.Chrome(options=opts)
        d.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})
        return d

    print(f'[1/4] Static screenshots for {slug}')
    d = driver()
    d.get(URL)
    time.sleep(6)

    # Try to disable any tab system if present (so we see all charts at once)
    d.execute_script("""
const vp = document.querySelector('.viz-panel');
if (vp) vp.dataset.uxVisualStage = 'off';
""")
    time.sleep(1)

    boxes = d.execute_script("""
function box(sel) {
  const el = document.querySelector(sel);
  if (!el) return null;
  const r = el.getBoundingClientRect();
  return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
}
function canvasesUnion() {
  const cs = document.querySelectorAll('canvas');
  if (!cs.length) return null;
  let L=1e9, T=1e9, R=-1e9, B=-1e9;
  cs.forEach(c => {
    const r = c.getBoundingClientRect();
    if (r.width > 50 && r.height > 50) {
      L = Math.min(L, r.left); T = Math.min(T, r.top);
      R = Math.max(R, r.right); B = Math.max(B, r.bottom);
    }
  });
  return L < 1e9 ? [Math.round(L), Math.round(T), Math.round(R), Math.round(B)] : null;
}
return {
  full: box('.main, .ux-main'),
  stats: box('.stat-cards'),
  charts: canvasesUnion(),
};
""")
    print(f'  boxes: {boxes}')

    full_png = os.path.join(OUT, 'full-view.png')
    d.save_screenshot(full_png)
    img = Image.open(full_png).convert('RGB')

    def crop(b, pad=12):
        if not b: return None
        l, t, r, bt = b
        # Include surrounding card/panel
        cc = img.crop((max(0,l-pad), max(0,t-pad-40), min(img.width,r+pad), min(img.height,bt+pad)))
        return cc

    closeup = crop(boxes['charts'])
    if closeup:
        closeup.save(os.path.join(OUT, 'charts-closeup.png'))
        print(f'  closeup: {closeup.size}')

    stats_img = crop(boxes['stats'], pad=6)
    if stats_img:
        stats_img.save(os.path.join(OUT, 'stats.png'))
        print(f'  stats: {stats_img.size}')

    # GIF: find a slider to animate
    print('[2/4] GIF animation')
    candidates = []
    if slider_hint:
        candidates.append(slider_hint)
    candidates += ['zeta','damping','Kp','Ki','Kd','tau','wn','sl-Kp','sl-Ti','sl-Td','sl-SP','lambda','theta','k','m','c','omega','f','amp','phi']
    slider_info = d.execute_script(f"""
const cands = {json.dumps(candidates)};
const all = Array.from(document.querySelectorAll('input[type=range]'));
for (const id of cands) {{
  const el = document.getElementById(id);
  if (el && el.type === 'range') {{
    return {{id, min: parseFloat(el.min), max: parseFloat(el.max),
            step: parseFloat(el.step)||0.01, value: parseFloat(el.value)}};
  }}
}}
// Fallback: first slider in DOM
if (all.length) {{
  const el = all[0];
  return {{id: el.id || '(unnamed)', min: parseFloat(el.min), max: parseFloat(el.max),
          step: parseFloat(el.step)||0.01, value: parseFloat(el.value)}};
}}
return null;
""")
    print(f'  slider: {slider_info}')

    frames = []
    if slider_info and boxes['charts']:
        s = slider_info
        n = 22
        vals = [s['min'] + (s['max'] - s['min']) * i / (n-1) for i in range(n)]
        vals = vals + vals[::-1]
        tmpdir = os.path.join(OUT, '_tmp')
        os.makedirs(tmpdir, exist_ok=True)
        union = boxes['charts']
        for i, v in enumerate(vals):
            d.execute_script(f"""
const el = document.getElementById('{s['id']}');
if (!el) return;
el.value = {v};
el.dispatchEvent(new Event('input', {{bubbles:true}}));
el.dispatchEvent(new Event('change', {{bubbles:true}}));
""")
            time.sleep(0.10)
            png = os.path.join(tmpdir, f'fr_{i:03d}.png')
            d.save_screenshot(png)
            fr = Image.open(png).convert('RGB').crop((union[0]-10, union[1]-30, union[2]+10, union[3]+10))
            tw = 700
            sc = tw / fr.width
            fr = fr.resize((tw, int(fr.height * sc)), Image.LANCZOS)
            frames.append(fr)
            os.remove(png)
        os.rmdir(tmpdir)
        gif_path = os.path.join(OUT, 'slider-anim.gif')
        frames[0].save(gif_path, save_all=True, append_images=frames[1:],
                       duration=80, loop=0, optimize=True)
        print(f'  GIF: {gif_path} ({len(frames)} frames)')
    d.quit()

    # Cover image
    print('[3/4] Cover image')
    cover = Image.new('RGB', (1200, 630), (12, 32, 64))
    grad = Image.new('RGB', (1200, 630))
    gd = ImageDraw.Draw(grad)
    for y in range(630):
        t = y / 629
        r = int(12 + (0 - 12) * t)
        g = int(32 + (0 - 32) * t)
        b = int(64 + (28 - 64) * t)
        gd.line([(0, y), (1200, y)], fill=(r, g, b))
    cover.paste(grad, (0, 0))

    if closeup:
        tw = 620
        ratio = tw / closeup.width
        chart_img = closeup.resize((tw, int(closeup.height * ratio)), Image.LANCZOS)
        if chart_img.height > 540:
            nh = 540
            nw = int(chart_img.width * nh / chart_img.height)
            chart_img = chart_img.resize((nw, nh), Image.LANCZOS)
        cx = 1200 - chart_img.width - 40
        cy = (630 - chart_img.height) // 2
        card = Image.new('RGB', (chart_img.width + 24, chart_img.height + 24), (255,255,255))
        cover.paste(card, (cx - 12, cy - 12))
        cover.paste(chart_img, (cx, cy))

    draw = ImageDraw.Draw(cover)
    font_path = r'C:\Windows\Fonts\YuGothB.ttc'
    if os.path.exists(font_path):
        title_font = ImageFont.truetype(font_path, 52)
        sub_font = ImageFont.truetype(font_path, 26)
        brand_font = ImageFont.truetype(font_path, 22)
    else:
        title_font = sub_font = brand_font = ImageFont.load_default()

    draw.text((50, 36), 'NovaSolver', font=brand_font, fill=(0, 180, 216))
    draw.text((50, 130), title1, font=title_font, fill=(255, 255, 255))
    if title2:
        draw.text((50, 200), title2, font=title_font, fill=(255, 255, 255))
    draw.text((50, 330), subtitle, font=sub_font, fill=(0, 180, 216))
    draw.text((50, 560), f'novasolver.jp/tools/{slug}.html', font=brand_font, fill=(255, 255, 255))

    cover.save(os.path.join(OUT, 'cover.png'), optimize=True)
    print(f'  cover saved')

    print('[4/4] Done. Files:')
    for f in sorted(os.listdir(OUT)):
        sz = os.path.getsize(os.path.join(OUT, f))
        print(f'  {f:<25} {sz/1024:.1f} KB')

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[1]
    t1 = sys.argv[2]
    t2 = sys.argv[3]
    sub = sys.argv[4]
    hint = sys.argv[5] if len(sys.argv) > 5 else ''
    make(slug, t1, t2, sub, hint)
