#!/usr/bin/env python3
"""
Générateur de sitemap.xml — François Gaillard Parquet
Usage : python3 generate-sitemap.py
Placer ce script à la racine du repo, lancer avant chaque upload GitHub.
"""
import re, os
from datetime import date

DOMAIN = 'https://poncageparquetvitrificationfrancois.com'
TODAY = date.today().strftime('%Y-%m-%d')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

files = sorted([f for f in os.listdir(SCRIPT_DIR) if f.endswith('.html')])

EXCLUDE = {'404.html', 'test.html', 'redirect-ipfs.html', 'devis-rapide.html',
           'googlefefc9d50d82467ab.html'}
EXCLUDE_PATTERNS = ['fanout', 'flux-', 'strategie-geo', 'query-fanout',
                    'ia-knowledge', 'faq-aeo', 'donnees-marche']

HIGH = {'index.html': ('1.0', 'weekly'),
        'prix-poncage-parquet-paris.html': ('0.9', 'weekly'),
        'specialiste-parquet-ancien-paris.html': ('0.9', 'weekly'),
        'expert-poncage-parquet-paris.html': ('0.9', 'weekly'),
        'devis-poncage-parquet-paris.html': ('0.9', 'weekly'),
        '100-questions-poncage-parquet-paris.html': ('0.9', 'weekly')}

def get_prio(fname):
    if fname in EXCLUDE: return None, None
    if any(p in fname for p in EXCLUDE_PATTERNS): return None, None
    if fname in HIGH: return HIGH[fname]
    if re.match(r'poncage-parquet-paris-\d+\.html', fname): return '0.8', 'monthly'
    if any(x in fname for x in ['poncage-parquet-', 'guide-', 'comparatif-']): return '0.7', 'monthly'
    return '0.6', 'monthly'

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
count = 0
for f in files:
    p, cf = get_prio(f)
    if not p: continue
    lines += [f'  <url>', f'    <loc>{DOMAIN}/{f}</loc>',
              f'    <lastmod>{TODAY}</lastmod>',
              f'    <changefreq>{cf}</changefreq>',
              f'    <priority>{p}</priority>', f'  </url>']
    count += 1
lines.append('</urlset>')

out = os.path.join(SCRIPT_DIR, 'sitemap.xml')
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))
print(f'sitemap.xml mis à jour : {count} URLs — {TODAY}')
