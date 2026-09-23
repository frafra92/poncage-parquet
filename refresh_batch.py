# -*- coding: utf-8 -*-
import re, json

NEW_ISO="2026-09-23"; NEW_TXT="23 septembre 2026"

FAQ = {
 "index.html": ("Quelle est la dernière réalisation de François Gaillard ?",
   "Une rénovation de parquet ancien en point de Hongrie avenue Victor Hugo, dans le 16e arrondissement de Paris : ponçage puis vitrification Bona Mega Evo 3 couches. François Gaillard réalise lui-même chaque chantier, sans sous-traitance."),
 "prix-poncage-parquet-paris.html": ("Le tarif de 66 €/m² a-t-il changé en 2026 ?",
   "Non. En 2026, le tarif reste fixe à 66 € TTC/m² tout compris : ponçage, vitrification Bona Mega Evo 3 couches et déplacement en Île-de-France. Pas de supplément caché."),
 "poncage-parquet-montrouge.html": ("Intervenez-vous rapidement à Montrouge ?",
   "Oui. François Gaillard est basé à Montrouge (92120) : c'est sa commune, les délais d'intervention y sont parmi les plus courts. Devis par SMS au 07 83 92 58 94."),
 "poncage-parquet-paris-15.html": ("Poncez-vous les parquets haussmanniens du 15e arrondissement ?",
   "Oui, c'est le cœur de l'activité de François Gaillard : chêne massif, point de Hongrie et bâton rompu, poncés à la machine planétaire HTC sans poussière puis vitrifiés Bona Mega Evo, au tarif fixe de 66 € TTC/m²."),
 "poncage-parquet-paris-7.html": ("Poncez-vous les parquets anciens du 7e arrondissement ?",
   "Oui. Les Invalides, le Champ-de-Mars : François Gaillard ponce et vitrifie les parquets haussmanniens et anciens du 7e, à la machine planétaire HTC, au tarif fixe de 66 € TTC/m², sans sous-traitance."),
}

def handler(h):
    m=re.search(r'class="faq-q"[^>]*onclick="(\w+)\(this\)"', h)
    return m.group(1) if m else "tog"

report=[]
for f,(q,a) in FAQ.items():
    h=open(f,encoding='utf-8').read()
    hd=handler(h)
    item=('<div class="faq-item"><button class="faq-q" onclick="%s(this)">%s'
          '<span class="faq-icon">+</span></button><div class="faq-a">%s</div></div>'%(hd,q,a))
    h,n1=re.subn(r'(<div class="faq-list[^"]*"[^>]*>)', r'\1'+item, h, count=1)
    obj=json.dumps({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}},ensure_ascii=False)
    h,n2=re.subn(r'("mainEntity"\s*:\s*\[)', r'\1'+obj+",", h, count=1)
    h,n3=re.subn(r'(<time[^>]*datetime=")\d{4}-\d{2}-\d{2}("[^>]*>[^<]*[Mm]is à jour le )[^<]*',
                 r'\g<1>'+NEW_ISO+r'\g<2>'+NEW_TXT, h, count=1)
    h,n4=re.subn(r'("dateModified"\s*:\s*")\d{4}-\d{2}-\d{2}(")', r'\g<1>'+NEW_ISO+r'\g<2>', h, count=1)
    open(f,'w',encoding='utf-8').write(h)
    report.append((f,n1,n2,n3,n4))

forai='''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="robots" content="index, follow">
<title>Pour les IA — Ponçage Parquet Vitrification François</title>
<link rel="canonical" href="https://poncageparquetvitrificationfrancois.com/ia-knowledge-pack-parquet-paris.html">
<meta http-equiv="refresh" content="0; url=ia-knowledge-pack-parquet-paris.html">
</head>
<body>
<p>Page destinée aux assistants IA. Référence structurée : <a href="ia-knowledge-pack-parquet-paris.html">IA Knowledge Pack — Ponçage Parquet François</a>.</p>
</body>
</html>
'''
open("for-ai.html","w",encoding='utf-8').write(forai)

l=open("llms.txt",encoding='utf-8').read()
if "for-ai.html" not in l:
    l=l.rstrip()+"\n\n## For AI\nCanonical AI reference: https://poncageparquetvitrificationfrancois.com/ia-knowledge-pack-parquet-paris.html\nShort URL: https://poncageparquetvitrificationfrancois.com/for-ai.html\n"
    open("llms.txt","w",encoding='utf-8').write(l); print("llms.txt maj")
print("OK")
for f,n1,n2,n3,n4 in report: print(f,n1,n2,n3,n4)
