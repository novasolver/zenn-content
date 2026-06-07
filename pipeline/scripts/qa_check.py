"""Quality gate for one Zenn article + its visuals.
Usage: python pipeline/scripts/qa_check.py <tool_slug> <article_slug>
Exit 0 = PASS, 1 = FAIL (prints reasons).
"""
import os, re, sys
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def img_informative(path, min_kb=4, min_std=6):
    if not os.path.exists(path): return False, f"missing {os.path.basename(path)}"
    if os.path.getsize(path) < min_kb*1024: return False, f"{os.path.basename(path)} too small (<{min_kb}KB)"
    try:
        im = Image.open(path)
        if getattr(im, "is_animated", False): im.seek(0)
        arr = np.asarray(im.convert("RGB")).astype(float)
    except Exception as e:
        return False, f"{os.path.basename(path)} unreadable: {e}"
    if arr.std() < min_std:
        return False, f"{os.path.basename(path)} looks blank (std={arr.std():.1f})"
    return True, "ok"

def main(tool_slug, article_slug):
    fails = []
    # slug format
    if not re.fullmatch(r"[a-z0-9_-]{12,50}", article_slug):
        fails.append(f"article_slug '{article_slug}' must be [a-z0-9_-] and 12-50 chars")
    # article file
    apath = os.path.join(REPO, "articles", f"{article_slug}.md")
    if not os.path.exists(apath):
        fails.append(f"article not found: articles/{article_slug}.md")
    else:
        txt = open(apath, encoding="utf-8").read()
        fm = txt.split("---", 2)
        head = fm[1] if len(fm) >= 3 else ""
        if "published: false" not in head: fails.append("frontmatter must have 'published: false'")
        for key in ("title:", "emoji:", 'type: "tech"', "topics:"):
            if key not in head: fails.append(f"frontmatter missing {key}")
        body = fm[2] if len(fm) >= 3 else txt
        if len(re.sub(r"\s", "", body)) < 1500:
            fails.append("body too short (<1500 non-space chars)")
        for img in ("cover.png", "charts-closeup.png", "slider-anim.gif"):
            ref = f"/images/{tool_slug}/{img}"
            if ref not in txt: fails.append(f"article does not reference {ref}")
        if f"novasolver.jp/tools/{tool_slug}.html" not in txt:
            fails.append("article missing CTA link to the tool")
    # images
    idir = os.path.join(REPO, "images", tool_slug)
    for img in ("cover.png", "charts-closeup.png", "slider-anim.gif"):
        p = os.path.join(idir, img)
        ok, why = img_informative(p)
        if not ok: fails.append(why)
        # Zenn aborts the whole deploy if any file exceeds 3MB -> hard cap at 2.9MB
        elif os.path.getsize(p) > 2.9 * 1024 * 1024:
            fails.append(f"{img} is {os.path.getsize(p)/1024/1024:.2f}MB (>2.9MB Zenn deploy limit)")
    if fails:
        print("FAIL")
        for f in fails: print("  -", f)
        return 1
    print(f"PASS  {article_slug}  (tool: {tool_slug})")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
