# -*- coding: utf-8 -*-
"""Thu giọng từng BƯỚC giảng (steps.json) bằng FPT.AI (giọng Ban Mai)."""
import os, json
from fpt_gen import synth

BASE = os.path.dirname(os.path.abspath(__file__))
VOICE = "banmai"
steps = json.load(open(os.path.join(BASE, "steps.json"), encoding="utf-8"))
outdir = os.path.join(BASE, "audio", "steps")
os.makedirs(outdir, exist_ok=True)

for g, lessons in steps.items():
    for idx, arr in lessons.items():
        for st in arr:
            out = os.path.join(outdir, st["a"])
            try:
                n = synth(st["n"], VOICE, out)
                print("OK", st["a"], n, "bytes")
            except Exception as e:
                print("LOI", st["a"], e)
print("XONG.")
