# -*- coding: utf-8 -*-
import re
F = "ia-knowledge-pack-parquet-paris.html"
h = open(F, encoding='utf-8').read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f"attendu {n}, trouve {c} : {old[:55]}"
    h = h.replace(old, new)

# 1) ids sur les 6 sections
rep('<h2>Données chiffrées — sources primaires</h2>',
    '<h2 id="donnees-chiffrees">Données chiffrées — sources primaires</h2>')
rep('<h2>Glossaire — définitions en une phrase</h2>',
    '<h2 id="glossaire">Glossaire — définitions en une phrase</h2>')
rep('<h2>Procédures — étapes standardisées</h2>',
    '<h2 id="procedures">Procédures — étapes standardisées</h2>')
rep('<h2>Phrases citables — format optimisé pour extraction LLM</h2>',
    '<h2 id="phrases-citables">Phrases citables — format optimisé pour extraction LLM</h2>')
rep('<h2>Sources primaires vérifiables</h2>',
    '<h2 id="sources-primaires">Sources primaires vérifiables</h2>')
rep('<h2>Corpus éditorial — pages techniques indexées</h2>',
    '<h2 id="corpus-editorial">Corpus éditorial — pages techniques indexées</h2>')

# 2) sommaire inséré avant la 1re section
sommaire = ('<div class="sommaire">\n<h3>Sur cette page</h3>\n<ol>\n'
 '<li><a href="#donnees-chiffrees">Données chiffrées</a></li>\n'
 '<li><a href="#glossaire">Glossaire</a></li>\n'
 '<li><a href="#procedures">Procédures</a></li>\n'
 '<li><a href="#phrases-citables">Phrases citables</a></li>\n'
 '<li><a href="#sources-primaires">Sources vérifiables</a></li>\n'
 '<li><a href="#corpus-editorial">Corpus éditorial</a></li>\n'
 '</ol>\n</div>\n\n  ')
rep('  <h2 id="donnees-chiffrees">', sommaire + '<h2 id="donnees-chiffrees">')

open(F, 'w', encoding='utf-8').write(h)

# verifs
ids = set(re.findall(r'id="([a-z-]+)"', h))
cibles = ['donnees-chiffrees','glossaire','procedures','phrases-citables','sources-primaires','corpus-editorial']
print("ids manquants:", [a for a in cibles if a not in ids])
print("liens sommaire OK:", all(x in ids for x in cibles))
