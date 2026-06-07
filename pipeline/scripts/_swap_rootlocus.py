# -*- coding: utf-8 -*-
"""Mark root-locus skipped (critical sign bug) and add wheatstone-bridge substitute."""
import json, os
os.chdir(r"E:\NovaSolver\zenn-content")
p="pipeline/queue.json"; d=json.load(open(p,encoding="utf-8"))
ids={q["id"] for q in d["queue"]}
for q in d["queue"]:
    if q["tool_slug"]=="root-locus":
        q["status"]="skipped"; q["skip_reason"]="critical sign bug in closed-loop pole calc (+RHP); see bugs.md"
nid=max(ids)+1
d["queue"].append({"id":nid,"priority":300,"topic_ja":"ホイートストンブリッジ","tool_slug":"wheatstone-bridge",
    "article_slug":"wheatstone-bridge-resistance-measurement","emoji":"⚖️",
    "topics":["javascript","電気回路","計測","可視化","数値計算"],"gif_hint":"","status":"todo"})
json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("root-locus skipped; added wheatstone-bridge id",nid)
