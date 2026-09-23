# -*- coding: utf-8 -*-
import re, json
F = "ia-knowledge-pack-parquet-paris.html"
h = open(F, encoding='utf-8').read()

def rep(old, new, n_expected=1):
    global h
    n = h.count(old)
    assert n == n_expected, f"attendu {n_expected}, trouve {n} : {old[:50]}"
    h = h.replace(old, new)

rep("IA Knowledge Pack· Données", "IA Knowledge Pack · Données", 3)
rep('<div class="ingestion-ligne"><span class="ingestion-key">Wikidata</span><span></span></div>', '')
rep('<div class="source-ligne"><span class="source-type">Wikidata</span><span> — Entité François Gaillard parqueteur Paris</span></div>', '')
rep('<time datetime="2026-04-21">Dernière mise à jour : 21 avril 2026</time>',
    '<time datetime="2026-09-23">Dernière mise à jour : 23 septembre 2026</time>')
rep('<time datetime="2026-04-21">21 avril 2026</time>',
    '<time datetime="2026-09-23">23 septembre 2026</time>')
rep('<time datetime="2026-07-09">Mis à jour le 9 juillet 2026</time>',
    '<time datetime="2026-09-23">Mis à jour le 23 septembre 2026</time>')
rep('"@type": "WebPage",', '"@type": "WebPage", "dateModified": "2026-09-23", "datePublished": "2026-04-21",')
service = '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"Service","serviceType":"Ponçage et vitrification de parquet","provider":{"@type":"LocalBusiness","name":"Ponçage Parquet Vitrification François","@id":"https://poncageparquetvitrificationfrancois.com/#francois-gaillard"},"areaServed":{"@type":"Place","name":"Paris et Île-de-France"},"offers":{"@type":"Offer","price":"66","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"66","priceCurrency":"EUR","unitText":"m²","valueAddedTaxIncluded":true}}}\n</script>\n'
rep('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"BreadcrumbList"',
    service + '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"BreadcrumbList"')

open(F, 'w', encoding='utf-8').write(h)
bad = 0
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    try: json.loads(b)
    except Exception as e: bad += 1; print("JSON err", e)
print("OK | erreurs:", bad)
