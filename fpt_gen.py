# -*- coding: utf-8 -*-
"""Thu giọng FPT.AI TTS (v5). Key đọc từ fpt_key.txt (KHÔNG commit)."""
import os, sys, json, time
import urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = open(os.path.join(BASE, "fpt_key.txt"), encoding="utf-8").read().strip()
ENDPOINT = "https://api.fpt.ai/hmi/tts/v5"

def synth(text, voice, out_path, speed=""):
    req = urllib.request.Request(
        ENDPOINT, data=text.encode("utf-8"), method="POST",
        headers={"api-key": KEY, "voice": voice, "speed": str(speed),
                 "Content-Type": "text/plain; charset=utf-8"})
    resp = urllib.request.urlopen(req, timeout=60)
    j = json.loads(resp.read().decode("utf-8"))
    if str(j.get("error", "0")) not in ("0", "None"):
        raise RuntimeError("FPT error: " + json.dumps(j, ensure_ascii=False))
    url = j.get("async")
    if not url:
        raise RuntimeError("Khong co async url: " + json.dumps(j, ensure_ascii=False))
    last = None
    for i in range(40):
        time.sleep(2)
        try:
            a = urllib.request.urlopen(url, timeout=60)
            ct = a.headers.get("Content-Type", "")
            blob = a.read()
            if "audio" in ct or "octet" in ct or len(blob) > 3000:
                with open(out_path, "wb") as f:
                    f.write(blob)
                return len(blob)
            last = (a.status, ct, len(blob))
        except urllib.error.HTTPError as e:
            last = ("HTTP", e.code)
        except Exception as e:
            last = ("ERR", str(e))
    raise RuntimeError("Audio chua san sang, last=" + str(last) + " url=" + url)

if __name__ == "__main__":
    voice = sys.argv[1] if len(sys.argv) > 1 else "banmai"
    text = open(os.path.join(BASE, "sample.txt"), encoding="utf-8").read()
    out = os.path.join(BASE, "audio", "sample_fpt_" + voice + ".mp3")
    n = synth(text, voice, out)
    print("OK", voice, n, "bytes ->", out)
