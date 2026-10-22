"""Shared matplotlib/PIL figure helpers for Zenn article visuals.

Used when a tool's own rendering is buggy or can't be captured cleanly
(RECIPE STEP 4). Produces the same 3 files the QA gate expects:
  images/<slug>/cover.png         (1200x630, branded, chart preview)
  images/<slug>/charts-closeup.png
  images/<slug>/slider-anim.gif

Japanese-capable font is used so labels render correctly.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

REPO = r"E:\NovaSolver\zenn-content"

# Register a Japanese font for matplotlib so JP labels don't tofu.
_JP_FONT = r"C:\Windows\Fonts\YuGothM.ttc"
if not os.path.exists(_JP_FONT):
    _JP_FONT = r"C:\Windows\Fonts\meiryo.ttc"
if os.path.exists(_JP_FONT):
    font_manager.fontManager.addfont(_JP_FONT)
    _name = font_manager.FontProperties(fname=_JP_FONT).get_name()
    matplotlib.rcParams["font.family"] = _name
matplotlib.rcParams["axes.unicode_minus"] = False


def outdir(slug):
    d = os.path.join(REPO, "images", slug)
    os.makedirs(d, exist_ok=True)
    return d


def save_fig(fig, path, dpi=130):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def make_cover(slug, title1, title2, subtitle, chart_png):
    """Branded 1200x630 cover with a chart preview pasted on the right."""
    out = os.path.join(outdir(slug), "cover.png")
    cover = Image.new("RGB", (1200, 630), (12, 32, 64))
    gd = ImageDraw.Draw(cover)
    for y in range(630):
        t = y / 629
        r = int(12 + (0 - 12) * t)
        g = int(32 + (0 - 32) * t)
        b = int(64 + (28 - 64) * t)
        gd.line([(0, y), (1200, y)], fill=(r, g, b))

    if chart_png and os.path.exists(chart_png):
        chart = Image.open(chart_png).convert("RGB")
        tw = 620
        ratio = tw / chart.width
        chart = chart.resize((tw, int(chart.height * ratio)), Image.LANCZOS)
        if chart.height > 540:
            nh = 540
            nw = int(chart.width * nh / chart.height)
            chart = chart.resize((nw, nh), Image.LANCZOS)
        cx = 1200 - chart.width - 40
        cy = (630 - chart.height) // 2
        card = Image.new("RGB", (chart.width + 24, chart.height + 24), (255, 255, 255))
        cover.paste(card, (cx - 12, cy - 12))
        cover.paste(chart, (cx, cy))

    draw = ImageDraw.Draw(cover)
    fp = r"C:\Windows\Fonts\YuGothB.ttc"
    if os.path.exists(fp):
        tf = ImageFont.truetype(fp, 50)
        sf = ImageFont.truetype(fp, 25)
        bf = ImageFont.truetype(fp, 22)
    else:
        tf = sf = bf = ImageFont.load_default()
    draw.text((50, 36), "NovaSolver", font=bf, fill=(0, 180, 216))
    draw.text((50, 140), title1, font=tf, fill=(255, 255, 255))
    if title2:
        draw.text((50, 205), title2, font=tf, fill=(255, 255, 255))
    draw.text((50, 330), subtitle, font=sf, fill=(0, 180, 216))
    draw.text((50, 560), f"novasolver.jp/tools/{slug}.html", font=bf, fill=(255, 255, 255))
    cover.save(out, optimize=True)
    print("  cover ->", out)


def save_gif(frames, slug, duration=110):
    out = os.path.join(outdir(slug), "slider-anim.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True)
    print("  gif ->", out, f"({len(frames)} frames)")


def fig_to_pil(fig, dpi=110):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")
