# -*- coding: utf-8 -*-
"""Bucket 1 (audit du gras) : fusionne 2 vrais doublons restants.
Redirige la page faible vers la canonique + reecrit les liens internes."""
import glob, os

BASE = "https://poncageparquetvitrificationfrancois.com/"

PAIRS = [
    ("glossaire-parquet-paris", "glossaire-parquet-definitions-expert", "Glossaire du parquet"),
    ("poncage-parquet-point-de-hongrie-paris", "poncage-parquet-point-hongrie-paris", "Ponçage parquet point de Hongrie Paris"),
]

REDIR = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Redirection — {label}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{base}{new}.html">
<meta http-equiv="refresh" content="0; url={new}.html">
<script>window.location.replace("{new}.html");</script>
</head>
<body>
<p>Cette page a été regroupée avec <a href="{new}.html">{label}</a>.</p>
</body>
</html>
'''

rewrites = 0
for f in glob.glob("*.html"):
    h = open(f, encoding='utf-8').read()
    o = h
    for old, new, _ in PAIRS:
        h = h.replace(f'href="{old}.html"', f'href="{new}.html"')
        h = h.replace(f'href="./{old}.html"', f'href="{new}.html"')
    if h != o:
        open(f, 'w', encoding='utf-8').write(h); rewrites += 1

for old, new, label in PAIRS:
    open(f"{old}.html", 'w', encoding='utf-8').write(REDIR.format(label=label, new=new, base=BASE))

print("liens internes reecrits sur", rewrites, "pages")
for old, new, _ in PAIRS:
    print(f"{old}.html -> redirection vers {new}.html")
