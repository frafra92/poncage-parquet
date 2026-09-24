# -*- coding: utf-8 -*-
"""Harmonise TOUTE la typo du site sur la charte (Cormorant Garamond + Jost).
- style-misc.css : polices hors-charte -> charte (par role)
- style-content.css : logo Georgia -> Cormorant ; body Georgia mort -> Jost
- style-page-phi.css : Georgia decoratif -> Cormorant
- pages hors-charte (5) + phi : <head> bascule sur les polices locales
- bump des cache-busters."""
import re, glob

CG = "'Cormorant Garamond',serif"
JO = "'Jost',sans-serif"

def must(h, old, new, atleast=1):
    n = h.count(old)
    assert n >= atleast, f"attendu >= {atleast}, trouve {n} : {old[:55]}"
    return h.replace(old, new)

# ================= 1) style-misc.css =================
css = open("style-misc.css", encoding='utf-8').read()
# 1a) Syne role bouton/tag -> Jost (avant le global Syne)
css = must(css, "border-radius:2px;margin-bottom:22px;font-family:'Syne',sans-serif",
                "border-radius:2px;margin-bottom:22px;font-family:'Jost',sans-serif")
css = must(css, "text-decoration:none;font-family:'Syne',sans-serif",
                "text-decoration:none;font-family:'Jost',sans-serif")
# 1b) corps -> Jost
for name, fb in [("DM Sans","sans-serif"),("Inter","sans-serif"),("Lato","sans-serif"),
                 ("Nunito","sans-serif"),("Source Sans 3","sans-serif"),("Georgia","serif")]:
    css = css.replace(f"'{name}',{fb}", JO)
# 1c) titres serif -> Cormorant
for name in ["Merriweather","Libre Baskerville","Playfair Display"]:
    css = css.replace(f"'{name}',serif", CG)
# 1d) Syne restant -> Cormorant
css = css.replace("'Syne',sans-serif", CG)
FOREIGN = ["DM Sans","Inter","Lato","Nunito","Source Sans 3","Merriweather",
           "Libre Baskerville","Playfair Display","Syne","Georgia"]
assert not [f for f in FOREIGN if f"'{f}'" in css], "misc.css: police hors-charte restante"
open("style-misc.css","w",encoding='utf-8').write(css)

# ================= 2) style-content.css =================
cc = open("style-content.css", encoding='utf-8').read()
cc = must(cc, ".logo{font-family:'Georgia',serif", ".logo{font-family:'Cormorant Garamond',serif")
cc = must(cc, "font-family:'Georgia',serif;line-height:1.7", "font-family:'Jost',sans-serif;line-height:1.7")
assert "'Georgia'" not in cc, "content.css: Georgia restant"
open("style-content.css","w",encoding='utf-8').write(cc)

# ================= 3) style-page-phi.css =================
pc = open("style-page-phi.css", encoding='utf-8').read()
pc = must(pc, "font-family: 'Georgia', serif;", "font-family: 'Cormorant Garamond', serif;", atleast=2)
assert "'Georgia'" not in pc, "phi.css: Georgia restant"
open("style-page-phi.css","w",encoding='utf-8').write(pc)

# ================= 4) inline Syne (h4) dans materiel -> Cormorant =========
mf = "materiel-professionnel-poncage-parquet-paris.html"
h = open(mf, encoding='utf-8').read()
h = h.replace("font-family:'Syne',sans-serif", CG)
open(mf,"w",encoding='utf-8').write(h)

# ================= 5) <head> -> polices locales (5 pages + phi) ==========
INJECT = ('<link rel="preload" as="font" type="font/woff2" href="fonts/cormorant-garamond-latin-600-normal.woff2" crossorigin>\n'
          '<link rel="preload" as="font" type="font/woff2" href="fonts/jost-latin-400-normal.woff2" crossorigin>\n'
          '<link rel="stylesheet" href="style-fonts.css?v=20260924">\n')
# 5 pages Google -> local
for f in ["a-propos.html","article2-questions-parqueteur-paris.html",
          "article3-artisan-independant-vs-entreprise-paris.html",
          "materiel-professionnel-poncage-parquet-paris.html",
          "peinture-avant-ou-apres-poncage-parquet.html"]:
    h = open(f, encoding='utf-8').read()
    h = re.sub(r'<noscript>\s*<link[^>]*fonts\.googleapis[^>]*>\s*</noscript>', '', h)
    h = re.sub(r'<link[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>', '', h)
    assert 'fonts.googleapis.com' not in h and 'fonts.gstatic.com' not in h, f"{f}: reste Google"
    h = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', h)
    m = re.search(r'<link[^>]*rel="stylesheet"[^>]*href="style-', h)
    open(f,"w",encoding='utf-8').write(h[:m.start()] + INJECT + h[m.start():])
# phi : n'a aucune police web -> lui donner les polices locales
ph = open("phi.html", encoding='utf-8').read()
if 'style-fonts.css' not in ph:
    m = re.search(r'<link[^>]*rel="stylesheet"[^>]*href="style-', ph)
    ph = ph[:m.start()] + INJECT + ph[m.start():]
    open("phi.html","w",encoding='utf-8').write(ph)

# ================= 6) cache-busters =================
def bump(old, new):
    c = 0
    for f in glob.glob("*.html"):
        h = open(f, encoding='utf-8').read()
        if old in h:
            open(f,"w",encoding='utf-8').write(h.replace(old, new)); c += 1
    return c
b_misc = bump("style-misc.css?v=20260804", "style-misc.css?v=20260924")
b_cont = bump("style-content.css?v=20260804", "style-content.css?v=20260924")
b_phi  = bump("style-page-phi.css?v=20260913", "style-page-phi.css?v=20260924")

print("misc.css bumpe:", b_misc, "| content.css bumpe:", b_cont, "| phi.css bumpe:", b_phi)
print("OK harmonisation")
