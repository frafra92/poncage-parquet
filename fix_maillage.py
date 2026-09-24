# -*- coding: utf-8 -*-
"""Renforce le maillage vers les 2 pages piliers (termes generiques page 2) :
ajoute des liens 'Poncage parquet Paris' et 'Vitrification parquet Paris' au
bloc de pied existant (Accueil · FAQ · Tarifs), present a l'identique sur ~124
pages. Spokes (communes/arrondissements) -> hubs. Sans doublon, sans auto-lien."""
import glob

OLD = '<a href="prix-poncage-parquet-paris.html" class="c-muted">Tarifs</a></p>'
ADD = (' · <a href="poncage-parquet-paris.html" class="c-muted">Ponçage parquet Paris</a>'
       ' · <a href="vitrification-parquet-paris.html" class="c-muted">Vitrification parquet Paris</a>')
NEW = '<a href="prix-poncage-parquet-paris.html" class="c-muted">Tarifs</a>' + ADD + '</p>'

SKIP = {"poncage-parquet-paris.html", "vitrification-parquet-paris.html"}

done = []
for f in sorted(glob.glob("*.html")):
    if f in SKIP:
        continue
    h = open(f, encoding='utf-8').read()
    if OLD not in h:
        continue
    if 'href="poncage-parquet-paris.html"' in h and 'href="vitrification-parquet-paris.html"' in h:
        continue
    h = h.replace(OLD, NEW, 1)
    open(f, 'w', encoding='utf-8').write(h)
    done.append(f)

print("pages maillees vers les piliers :", len(done))
