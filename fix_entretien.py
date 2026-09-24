# -*- coding: utf-8 -*-
import re, json
F = "entretien-parquet-vitrifie-paris.html"
h = open(F, encoding='utf-8').read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f"attendu {n}, trouve {c} : {old[:55]}"
    h = h.replace(old, new)

rep("<title>Entretien parquet vitrifié Paris</title>",
    "<title>Entretien et nettoyage d'un parquet vitrifié — Paris</title>")
rep('content="Entretien parquet vitrifié Paris — la méthode simple et efficace"',
    'content="Entretien et nettoyage d\'un parquet vitrifié à Paris — la méthode simple"')
rep('content="Comment entretenir un parquet vitrifié à Paris ? Balai, aspirateur, serpillière humide — la méthode simple."',
    'content="Comment entretenir et nettoyer un parquet vitrifié à Paris ? Balai, aspirateur, serpillière bien essorée, sans produit spécial — la méthode simple de l\'artisan François Gaillard."')
rep('content="Comment entretenir un parquet vitrifié. Balai, aspirateur, serpillière humide seulement.',
    'content="Comment entretenir et nettoyer un parquet vitrifié. Balai, aspirateur, serpillière bien essorée seulement.')
rep('<h1>Entretien parquet vitrifié Paris —<br>',
    '<h1>Entretien et nettoyage d\'un parquet vitrifié à Paris —<br>')
q = "Quel produit pour nettoyer un parquet vitrifié ?"
a = "Aucun produit spécial n'est nécessaire : une serpillière bien essorée à l'eau claire suffit. Évitez les nettoyants gras, la cire et l'excès d'eau, qui ternissent ou infiltrent le vernis. Sur une vitrification Bona Mega Evo, l'eau claire préserve durablement la finition."
item = ('<div class="faq-item"><button class="faq-q" onclick="tog(this)">%s'
        '<span class="faq-icon">+</span></button><div class="faq-a">%s</div></div>' % (q, a))
rep('<div class="faq-list">', '<div class="faq-list">' + item)
obj = json.dumps({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}, ensure_ascii=False)
rep('"mainEntity":[', '"mainEntity":[' + obj + ",")
h, nv = re.subn(r'(<time[^>]*datetime=")\d{4}-\d{2}-\d{2}("[^>]*>[^<]*[Mm]is à jour le )[^<]*',
                r'\g<1>2026-09-24\g<2>24 septembre 2026', h)
rep('"dateModified": "2026-05-14"', '"dateModified": "2026-09-24"')

open(F, 'w', encoding='utf-8').write(h)
bad = 0
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    try: json.loads(b)
    except Exception as e: bad += 1; print("JSON err", e)
print("OK | dates:", nv, "| erreurs:", bad)
