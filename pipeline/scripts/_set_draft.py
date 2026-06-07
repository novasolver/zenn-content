# -*- coding: utf-8 -*-
"""Set status=draft for given tool_slugs in queue.json. Usage: _set_draft.py slug1 slug2 ..."""
import json, os, sys
os.chdir(r"E:\NovaSolver\zenn-content")
p="pipeline/queue.json"; d=json.load(open(p,encoding="utf-8"))
slugs=set(sys.argv[1:]); n=0
for q in d["queue"]:
    if q["tool_slug"] in slugs:
        q["status"]="draft"; n+=1
json.dump(d,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("set draft:",n)
