# -*- coding: utf-8 -*-
import re
F = "entretien-parquet-vitrifie-paris.html"
h = open(F, encoding='utf-8').read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f"attendu {n}, trouve {c} : {old[:55]}"
    h = h.replace(old, new)

# 1) ids sur les 7 sections
rep('<h2>L\'entretien quotidien — balai et aspirateur</h2>',
    '<h2 id="entretien-quotidien">L\'entretien quotidien — balai et aspirateur</h2>')
rep('<h2>Le nettoyage ponctuel — serpillière légèrement humide</h2>',
    '<h2 id="nettoyage-ponctuel">Le nettoyage ponctuel — serpillière légèrement humide</h2>')
rep('<h2>Pourquoi les produits spéciaux parquet sont inutiles — voire nuisibles</h2>',
    '<h2 id="produits-speciaux">Pourquoi les produits spéciaux parquet sont inutiles — voire nuisibles</h2>')
rep('<h2>L\'eau reste le point faible du bois — même vitrifié</h2>',
    '<h2 id="eau-point-faible">L\'eau reste le point faible du bois — même vitrifié</h2>')
rep('<h2>Durée de vie du vernis et re-vitrification</h2>',
    '<h2 id="duree-vie-vernis">Durée de vie du vernis et re-vitrification</h2>')
rep('<h2>Les erreurs d\'entretien les plus courantes</h2>',
    '<h2 id="erreurs-entretien">Les erreurs d\'entretien les plus courantes</h2>')
rep('<h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:#fff;margin-bottom:1.5rem;font-weight:400">Questions fréquentes',
    '<h2 id="faq" style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:#fff;margin-bottom:1.5rem;font-weight:400">Questions fréquentes')

# 2) sommaire (meme markup que guide-complet : div.sommaire) inséré avant la 1re section
sommaire = ('<div class="sommaire">\n<h3>Sur cette page</h3>\n<ol>\n'
 '<li><a href="#entretien-quotidien">Entretien quotidien</a></li>\n'
 '<li><a href="#nettoyage-ponctuel">Nettoyage ponctuel</a></li>\n'
 '<li><a href="#produits-speciaux">Produits spéciaux : inutiles</a></li>\n'
 '<li><a href="#eau-point-faible">L\'eau, le point faible</a></li>\n'
 '<li><a href="#duree-vie-vernis">Durée de vie du vernis</a></li>\n'
 '<li><a href="#erreurs-entretien">Erreurs à éviter</a></li>\n'
 '<li><a href="#faq">Questions fréquentes</a></li>\n'
 '</ol>\n</div>\n\n    ')
rep('    <h2 id="entretien-quotidien">', sommaire + '<h2 id="entretien-quotidien">')

open(F, 'w', encoding='utf-8').write(h)

# 3) styles .sommaire dans style-shared.css (feuille chargée par la page ;
#    variables --or/--noir2/--bord fournies par style-quartiers.css).
CSS = "style-shared.css"
css = open(CSS, encoding='utf-8').read()
if '.sommaire{' not in css:
    bloc = ("\n.sommaire{background:var(--noir2);border:1px solid var(--bord);padding:2rem 2.5rem;margin-bottom:4rem}"
            "\n.sommaire h3{font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:var(--or);margin-bottom:1.2rem}"
            "\n.sommaire ol{list-style:none;counter-reset:som;display:flex;flex-direction:column;gap:.5rem}"
            "\n.sommaire ol li{counter-increment:som;font-size:.9rem;color:var(--muted)}"
            "\n.sommaire ol li::before{content:counter(som)\". \";color:var(--or-sombre)}"
            "\n.sommaire ol li a{color:var(--muted);text-decoration:none}"
            "\n.sommaire ol li a:hover{color:var(--or)}\n")
    open(CSS, 'a', encoding='utf-8').write(bloc)
    css_added = True
else:
    css_added = False

# verifs
import re as _r
ids = set(_r.findall(r'id="([a-z-]+)"', h))
cibles = ['entretien-quotidien','nettoyage-ponctuel','produits-speciaux','eau-point-faible','duree-vie-vernis','erreurs-entretien','faq']
manquants = [a for a in cibles if a not in ids]
print("ids manquants:", manquants)
print("liens sommaire OK:", all(x in ids for x in cibles))
print("CSS .sommaire ajoute a style-shared.css:", css_added)
