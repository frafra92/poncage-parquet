# -*- coding: utf-8 -*-
"""Auto-hebergement des polices (RGPD + performance).
1) copie les woff2 (Cormorant Garamond + Jost) depuis @fontsource vers fonts/
2) genere style-fonts.css (latin + latin-ext, unicode-range, font-display:swap)
3) remplace les appels Google Fonts par la feuille locale + preload, sur les
   pages Cormorant+Jost uniquement (laisse celles a autres polices).
Le workflow installe @fontsource via npm avant de lancer ce script."""
import re, glob, os, shutil

VER = "20260924"
CANDS = ["node_modules/@fontsource", "/tmp/fontwork/node_modules/@fontsource"]
SRC = next((c for c in CANDS if os.path.isdir(c)), None)
assert SRC, "fontsource introuvable (npm install manquant)"

# ---------- 1) copie des woff2 ----------
os.makedirs("fonts", exist_ok=True)
SPECS = {
    "cormorant-garamond": [("400", "normal"), ("500", "normal"), ("600", "normal"),
                            ("700", "normal"), ("400", "italic")],
    "jost": [("300", "normal"), ("400", "normal"), ("500", "normal"),
             ("600", "normal"), ("700", "normal")],
}
for fam, specs in SPECS.items():
    for w, st in specs:
        for sub in ("latin", "latin-ext"):
            name = f"{fam}-{sub}-{w}-{st}.woff2"
            shutil.copy(f"{SRC}/{fam}/files/{name}", f"fonts/{name}")

# ---------- 2) style-fonts.css ----------
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LATINEXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"
FAMNAME = {"cormorant-garamond": "Cormorant Garamond", "jost": "Jost"}

def face(fam, w, st, sub, ur):
    return ("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
            "src:url(fonts/%s-%s-%s-%s.woff2) format('woff2');unicode-range:%s}\n"
            % (FAMNAME[fam], st, w, fam, sub, w, st, ur))

css = "/* Polices auto-hebergees (Cormorant Garamond + Jost) - RGPD + performance. Genere. */\n"
for fam, specs in SPECS.items():
    for w, st in specs:
        css += face(fam, w, st, "latin-ext", LATINEXT)
        css += face(fam, w, st, "latin", LATIN)
open("style-fonts.css", "w", encoding="utf-8").write(css)

# ---------- 3) patch des pages ----------
OTHER = re.compile(r'DM\+Sans|Merriweather|Libre\+Baskerville|Syne|Nunito|Inter|Lato')
INJECT = (
    '<link rel="preload" as="font" type="font/woff2" href="fonts/cormorant-garamond-latin-600-normal.woff2" crossorigin>\n'
    '<link rel="preload" as="font" type="font/woff2" href="fonts/jost-latin-400-normal.woff2" crossorigin>\n'
    '<link rel="stylesheet" href="style-fonts.css?v=%s">\n' % VER
)
changed, skipped = [], []
for f in sorted(glob.glob("*.html")):
    h = open(f, encoding='utf-8').read()
    if 'fonts.googleapis.com' not in h and 'fonts.gstatic.com' not in h:
        continue
    fam = re.search(r'css2\?family=([^"]+)', h)
    if not fam or 'Cormorant' not in fam.group(1) or OTHER.search(fam.group(1)):
        skipped.append(f); continue
    orig = h
    h = re.sub(r'<noscript>\s*<link[^>]*fonts\.googleapis[^>]*>\s*</noscript>', '', h)
    h = re.sub(r'<link[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>', '', h)
    assert 'fonts.googleapis.com' not in h and 'fonts.gstatic.com' not in h, f"{f}: reste une ref Google"
    h = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', h)
    m = re.search(r'<link[^>]*rel="stylesheet"[^>]*href="style-', h)
    if m:
        h = h[:m.start()] + INJECT + h[m.start():]
    else:
        h = h.replace('</head>', INJECT + '</head>', 1)
    assert h.count('style-fonts.css') == 1, f"{f}: style-fonts.css x{h.count('style-fonts.css')}"
    if h != orig:
        open(f, 'w', encoding='utf-8').write(h); changed.append(f)

print("woff2 copies :", len(glob.glob('fonts/*.woff2')))
print("PAGES MODIFIEES :", len(changed))
print("PAGES IGNOREES (autres polices) :", len(skipped), "->", skipped)
