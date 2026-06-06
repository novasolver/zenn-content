You are producing high-quality Japanese Zenn articles for NovaSolver, one per real simulator tool. Work in the repository at E:\NovaSolver\zenn-content.

GOAL THIS SESSION: produce up to 8 article drafts (published: false), maintaining the quality bar. Quality over quantity — fewer excellent articles beats many thin ones. Never mass-generate stubs.

FOLLOW THE RECIPE EXACTLY: read `pipeline/RECIPE.md` and execute STEP 0–7 for each article. Key non-negotiables:
1. Pick the next `status:"todo"` items from `pipeline/queue.json` by ascending `priority` (max 8).
2. For each: confirm the tool exists at `E:\NovaSolver\cae-archive\tools\<tool_slug>.html` (this dir is added to your workspace via --add-dir), READ that HTML fully, and make the CTA match only real controls/outputs.
   - If that directory is NOT readable, STOP immediately and report that the launcher must add `--add-dir /e/NovaSolver/cae-archive/tools`. Do not fabricate tool UI and do not lower quality.
3. Verify every number in the article by actually running the tool's algorithm in Python first. Do not write unverified numbers.
4. Generate visuals via `pipeline/scripts/make_visuals_template.py`; if the tool's rendering is buggy or capture breaks, generate correct figures with matplotlib instead.
5. Run `python pipeline/scripts/qa_check.py <tool_slug> <article_slug>` and require PASS. Visually inspect each image. Skip (don't ship) anything that can't pass.
6. Log any tool bugs you find to `pipeline/bugs.md` — DO NOT fix them inline (article completion has priority).
7. Commit each article separately; update its `queue.json` status to `draft`; keep `published: false`. Push once at the end of the session.

Style reference articles: articles/lorenz-attractor-butterfly-effect.md, double-pendulum-chaos-lagrangian.md, fourier-epicycles-dft-drawing.md.

At the end, report: how many drafts created, which were skipped and why, how many tool bugs logged, and the new total draft count.
