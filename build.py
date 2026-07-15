#!/usr/bin/env python3
import json, base64, struct, zlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "index.html")

# --- map image questions (by exact German question text) to image files ---
IMG = {
    "Welches ist das Wappen der Bundesrepublik Deutschland?": "aufgabe_21.png",
    "Was zeigt dieses Bild?": "aufgabe_55.png",
    "Welcher Stimmzettel wäre bei einer Bundestagswahl gültig?": "aufgabe_130.png",
    "Welches war das Wappen der Deutschen Demokratischen Republik?": "aufgabe_21.png",
    "Welche ist die Flagge der Europäischen Union?": "aufgabe_226.png",
    "Welches Wappen gehört zum Freistaat Bayern?": "bayern_1.png",
    "Welches Bundesland ist Bayern?": "bayern_8.png",
}

def data_uri(fn):
    with open(os.path.join(HERE, "img", fn), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

# --- load + filter to the real Bavaria test: 300 federal + 10 Bayern ---
raw = json.load(open(os.path.join(HERE, "data.json")))
STATES = {"Baden-Württemberg","Berlin","Brandenburg","Bremen","Hamburg","Hessen",
    "Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen","Rheinland-Pfalz",
    "Saarland","Sachsen","Sachsen-Anhalt","Schleswig-Holstein","Thüringen"}  # all states EXCEPT Bayern

# --- load Albanian translations (index-aligned list; keyed by position, not text,
#     because some questions share identical German text with different answers) ---
tfile = os.path.join(HERE, "translations", "combined.json")
combined = json.load(open(tfile, encoding="utf-8")) if os.path.exists(tfile) else []

uri_cache = {}
out = []
img_hits = 0
sq_hits = 0
for q in raw:
    if q["category"] in STATES:
        continue  # drop other states
    item = {"q": q["question"], "a": q["answers"], "c": q["correct"], "cat": q["category"]}
    fn = IMG.get(q["question"])
    if fn:
        uri_cache.setdefault(fn, data_uri(fn))
        item["img"] = uri_cache[fn]
        img_hits += 1
    i = len(out)  # position in filtered list == index in combined.json
    if i < len(combined) and combined[i] and combined[i].get("sq") and len(combined[i].get("sqa", [])) == 4:
        item["sq"] = combined[i]["sq"]
        item["sqa"] = combined[i]["sqa"]
        sq_hits += 1
    out.append(item)

federal = sum(1 for q in out if q["cat"] != "Bayern")
bayern  = sum(1 for q in out if q["cat"] == "Bayern")
assert federal == 300, f"expected 300 federal, got {federal}"
assert bayern == 10, f"expected 10 Bayern, got {bayern}"
assert img_hits == len(IMG), f"image mapping mismatch: {img_hits} vs {len(IMG)}"
if combined:
    assert len(combined) == len(out), f"translation misalignment: {len(combined)} vs {len(out)} questions"
    for it in out:
        if "sqa" in it:
            assert len(it["sqa"]) == len(it["a"]), f"answer count mismatch: {it['q'][:40]}"

# --- tiny solid-green 180x180 PNG app icon (no deps) ---
def solid_png(w, h, rgb):
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))  # filter byte + row
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    return "data:image/png;base64," + base64.b64encode(png).decode()

icon = solid_png(180, 180, (11, 107, 58))

# --- inject into template ---
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
html = tpl.replace("__QUESTIONS__", json.dumps(out, ensure_ascii=False)).replace("__ICON__", icon)
open(OUT, "w", encoding="utf-8").write(html)

print(f"wrote {OUT}")
print(f"  questions: {len(out)}  (federal {federal} + Bayern {bayern})")
print(f"  images embedded on {img_hits} questions ({len(uri_cache)} distinct)")
print(f"  albanian translations: {sq_hits}/{len(out)}")
print(f"  size: {os.path.getsize(OUT)//1024} KB")
