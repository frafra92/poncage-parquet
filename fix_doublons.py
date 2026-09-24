# -*- coding: utf-8 -*-
"""Consolide les pages communes en double (redirige la faible vers la canonique
+ reecrit les liens internes) et ajoute style-fonts.css aux pages qui en manquent."""
import glob, re, os

BASE = "https://poncageparquetvitrificationfrancois.com/"

PAIRS = [
    ("boulogne", "boulogne-billancourt", "Ponçage parquet Boulogne-Billancourt"),
    ("neuilly", "neuilly-sur-seine", "Ponçage parquet Neuilly-sur-Seine"),
    ("versailles-ville", "versailles", "Ponçage parquet Versailles"),
]

REDIR = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Redirection — {label}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{base}poncage-parquet-{new}.html">
<meta http-equiv="refresh" content="0; url=poncage-parquet-{new}.html">
<script>window.location.replace("poncage-parquet-{new}.html");</script>
</head>
<body>
<p>Cette page a été regroupée avec <a href="poncage-parquet-{new}.html">{label}</a>.</p>
</body>
</html>
'''

rewrites = 0
for f in glob.glob("*.html"):
    h = open(f, encoding='utf-8').read()
    o = h
    for old, new, _ in PAIRS:
        h = h.replace(f'href="poncage-parquet-{old}.html"', f'href="poncage-parquet-{new}.html"')
        h = h.replace(f'href="./poncage-parquet-{old}.html"', f'href="poncage-parquet-{new}.html"')
    if h != o:
        open(f, 'w', encoding='utf-8').write(h); rewrites += 1

for old, new, label in PAIRS:
    op = f"poncage-parquet-{old}.html"
    open(op, 'w', encoding='utf-8').write(REDIR.format(label=label, new=new, base=BASE))

FONT = ('<link rel="preload" as="font" type="font/woff2" href="fonts/cormorant-garamond-latin-600-normal.woff2" crossorigin>\n'
        '<link rel="preload" as="font" type="font/woff2" href="fonts/jost-latin-400-normal.woff2" crossorigin>\n'
        '<link rel="stylesheet" href="style-fonts.css?v=20260924">\n')
fontfix = []
for f in glob.glob("*.html"):
    h = open(f, encoding='utf-8').read()
    if 'style-misc.css' in h and 'style-fonts.css' not in h and not re.search(r'http-equiv[^>]*refresh', h[:800]):
        m = re.search(r'<link[^>]*rel="stylesheet"[^>]*href="style-', h) or re.search(r'<link[^>]*rel="preload"[^>]*href="style-', h)
        if m:
            h = h[:m.start()] + FONT + h[m.start():]
            open(f, 'w', encoding='utf-8').write(h); fontfix.append(f)

print("liens internes reecrits sur", rewrites, "pages")
print("redirections creees :", [p[0] for p in PAIRS])
print("style-fonts.css ajoute a :", fontfix)
