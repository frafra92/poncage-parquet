# -*- coding: utf-8 -*-
"""Genere poncage-parquet-ile-de-france.html : page pilier regionale + hub
listant toutes les communes par departement. Chrome repris de grand-paris."""
import os

BASE = "https://poncageparquetvitrificationfrancois.com/"

# (nom affiche, slug fichier) par departement — pages canoniques verifiees
PARIS = [(f"Paris {n}{'er' if n==1 else 'e'}", f"poncage-parquet-paris-{n}.html") for n in range(1,21)]
D92 = [("Antony","antony"),("Asnières-sur-Seine","asnieres-sur-seine"),("Bagneux","bagneux"),
("Bois-Colombes","bois-colombes"),("Boulogne-Billancourt","boulogne-billancourt"),("Bourg-la-Reine","bourg-la-reine"),
("Châtenay-Malabry","chatenay-malabry"),("Châtillon","chatillon"),("Chaville","chaville"),("Clamart","clamart"),
("Clichy","clichy"),("Colombes","colombes"),("Courbevoie","courbevoie"),("Fontenay-aux-Roses","fontenay-aux-roses"),
("Garches","garches"),("Issy-les-Moulineaux","issy-les-moulineaux"),("La Garenne-Colombes","la-garenne-colombes"),
("Le Plessis-Robinson","le-plessis-robinson"),("Levallois-Perret","levallois-perret"),("Malakoff","malakoff"),
("Marnes-la-Coquette","marnes-la-coquette"),("Meudon","meudon"),("Meudon-la-Forêt","meudon-la-foret"),
("Montrouge","montrouge"),("Nanterre","nanterre"),("Neuilly-sur-Seine","neuilly-sur-seine"),("Puteaux","puteaux"),
("Rueil-Malmaison","rueil-malmaison"),("Saint-Cloud","saint-cloud"),("Sceaux","sceaux"),("Sèvres","sevres"),
("Suresnes","suresnes"),("Vanves","vanves"),("Vaucresson","vaucresson"),("Ville-d'Avray","ville-davray")]
D94 = [("Alfortville","alfortville"),("Arcueil","arcueil"),("Boissy-Saint-Léger","boissy-saint-leger"),("Cachan","cachan"),
("Champigny-sur-Marne","champigny-sur-marne"),("Charenton-le-Pont","charenton-le-pont"),("Chevilly-Larue","chevilly-larue"),
("Choisy-le-Roi","choisy-le-roi"),("Créteil","creteil"),("Fontenay-sous-Bois","fontenay-sous-bois"),("Gentilly","gentilly"),
("Ivry-sur-Seine","ivry-sur-seine"),("Joinville-le-Pont","joinville-le-pont"),("L'Haÿ-les-Roses","l-hay-les-roses"),
("Le Kremlin-Bicêtre","le-kremlin-bicetre"),("Le Perreux-sur-Marne","le-perreux-sur-marne"),("Maisons-Alfort","maisons-alfort"),
("Nogent-sur-Marne","nogent-sur-marne"),("Orly","orly"),("Rungis","rungis"),("Saint-Mandé","saint-mande"),
("Saint-Maur-des-Fossés","saint-maur-des-fosses"),("Saint-Maurice","saint-maurice"),("Thiais","thiais"),
("Villejuif","villejuif"),("Vincennes","vincennes"),("Vitry-sur-Seine","vitry-sur-seine")]
D93 = [("Pantin","pantin")]
D78 = [("Boissy-sans-Avoir","boissy-sans-avoir"),("Bougival","bougival"),("Chatou","chatou"),
("Croissy-sur-Seine","croissy-sur-seine"),("Le Chesnay-Rocquencourt","le-chesnay-rocquencourt"),("Le Vésinet","le-vesinet"),
("Marly-le-Roi","marly-le-roi"),("Méré","mere"),("Montfort-l'Amaury","montfort-l-amaury"),("Plaisir","plaisir"),
("Saint-Germain-en-Laye","saint-germain-en-laye"),("Versailles","versailles"),("Vélizy-Villacoublay","velizy-villacoublay"),
("Viroflay","viroflay")]
D91 = [("Athis-Mons","athis-mons"),("Bures-sur-Yvette","bures-sur-yvette"),("Chilly-Mazarin","chilly-mazarin"),
("Gif-sur-Yvette","gif-sur-yvette"),("Juvisy-sur-Orge","juvisy-sur-orge"),("Longjumeau","longjumeau"),("Massy","massy"),
("Orsay","orsay"),("Palaiseau","palaiseau"),("Savigny-sur-Orge","savigny-sur-orge"),("Wissous","wissous")]

DEPTS = [("Paris (75)","dep-75",PARIS,True),
         ("Hauts-de-Seine (92)","dep-92",D92,False),
         ("Val-de-Marne (94)","dep-94",D94,False),
         ("Seine-Saint-Denis (93)","dep-93",D93,False),
         ("Yvelines (78)","dep-78",D78,False),
         ("Essonne (91)","dep-91",D91,False)]

missing = []
def href(slug):
    fn = slug if slug.endswith('.html') else f"poncage-parquet-{slug}.html"
    if not os.path.exists(fn): missing.append(fn)
    return fn

sections = []
somm = []
total = 0
for title, anchor, lst, is_paris in DEPTS:
    somm.append(f'<li><a href="#{anchor}">{title}</a></li>')
    items = []
    for name, slug in lst:
        fn = href(slug)
        total += 1
        items.append(f'    <li><a href="{fn}">Ponçage parquet {name}</a></li>')
    sections.append(f'  <h3 id="{anchor}">{title}</h3>\n  <ul>\n' + "\n".join(items) + "\n  </ul>")

sommaire_html = ('<div class="sommaire">\n<h3>Sur cette page</h3>\n<ol>\n' + "\n".join(somm) + "\n</ol>\n</div>")
sections_html = "\n\n".join(sections)

if missing:
    print("FICHIERS CIBLES MANQUANTS:", missing)
else:
    print("Tous les liens communes resolvent. Total:", total)

html = f'''<!DOCTYPE html>
<html lang="fr">
 <head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ponçage parquet Île-de-France — 66 €/m² | François Gaillard</title>
<meta name="description" content="Ponçage et vitrification de parquet en Île-de-France : 66 € TTC/m² tout compris. François Gaillard, artisan parqueteur indépendant, intervient à Paris et dans toute l'Île-de-France. Devis par SMS.">
<meta name="keywords" content="ponçage parquet Île-de-France, vitrification parquet Île-de-France, artisan parqueteur Île-de-France, rénovation parquet IDF, ponçage parquet région parisienne">
<meta name="author" content="François Gaillard">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Ponçage Parquet Vitrification François">
<meta property="og:url" content="{BASE}poncage-parquet-ile-de-france.html">
<meta property="og:title" content="Ponçage parquet Île-de-France — 66 €/m² | François Gaillard">
<meta property="og:description" content="Ponçage et vitrification de parquet en Île-de-France : 66 € TTC/m² tout compris. Artisan parqueteur indépendant, 220+ avis 5 étoiles. Devis par SMS.">
<meta property="og:image" content="{BASE}artisan-poncage-parquet-paris-francois-gaillard.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="1064">
<meta property="og:image:alt" content="François Gaillard, artisan parqueteur Île-de-France">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Ponçage parquet Île-de-France — 66 €/m² | François Gaillard">
<meta name="twitter:description" content="Ponçage et vitrification de parquet dans toute l'Île-de-France. Tarif fixe 66 € TTC/m² tout compris. Artisan indépendant, 220+ avis 5 étoiles.">
<meta name="twitter:image" content="{BASE}artisan-poncage-parquet-paris-francois-gaillard.webp">
<link rel="canonical" href="{BASE}poncage-parquet-ile-de-france.html">
<link rel="preload" as="font" type="font/woff2" href="fonts/cormorant-garamond-latin-600-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/jost-latin-400-normal.woff2" crossorigin>
<link rel="stylesheet" href="style-fonts.css?v=20260924">
<link rel="preload" as="style" href="style-misc.css?v=20260924">
<link rel="stylesheet" href="style-misc.css?v=20260924">
<link rel="stylesheet" href="style-utilities.css?v=20260804">
<link rel="stylesheet" href="style-shared.css?v=20260804">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2WFFQHC680"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-2WFFQHC680');
  </script>
</head>
<body>

<header>
  <article>
<h1>Ponçage parquet en Île-de-France</h1>
  <p>Paris et toute l'Île-de-France — par François Gaillard, artisan parqueteur indépendant</p>
</article>
</header>
<main id="main">
<nav aria-label="Fil d'Ariane" class="breadcrumb-std">
  <a href="index.html" class="c-muted-link">Accueil</a><span class="bc-sep">›</span><span class="c-or">Ponçage parquet Île-de-France</span>
</nav>

<div class="container">

  <p class="def-locale">Le ponçage et la vitrification d'un parquet en <strong>Île-de-France</strong> coûtent <strong>66 € TTC/m², tout compris</strong> (ponçage, vitrification Bona Mega Evo 3 couches et déplacement). François Gaillard, artisan parqueteur indépendant basé à Montrouge, intervient à Paris et dans toute l'Île-de-France — <strong>Hauts-de-Seine (92), Val-de-Marne (94), Seine-Saint-Denis (93), Yvelines (78) et Essonne (91)</strong>. Devis par SMS au 07 83 92 58 94, sur photos, sans déplacement.</p>

  <div class="avis-box">
    <div class="stars">⭐⭐⭐⭐⭐</div>
    <strong>220+ avis Google 5 étoiles</strong>
    <p>La confiance de centaines de clients à Paris et en Île-de-France</p>
</div>

  {sommaire_html}

  <h2>Un artisan indépendant pour toute l'Île-de-France</h2>

  <p>François Gaillard ponce et vitrifie les parquets de <strong>Paris et de toute l'Île-de-France</strong> depuis Montrouge. Là où beaucoup d'entreprises sous-traitent ou facturent le déplacement, ici c'est un <strong>seul artisan</strong> qui répond, qui devise et qui intervient — au <strong>même tarif partout : 66 € TTC/m², tout compris</strong>, de Paris intra-muros aux Yvelines.</p>

  <h2>Ce que comprend le tarif de 66 € TTC/m²</h2>

  <p>Un seul prix, affiché, sans surprise à la facture :</p>

  <table class="prix-table">
    <thead>
      <tr>
        <th>Inclus dans le 66 € TTC/m²</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Ponçage machine planétaire HTC (3 disques)</td><td><strong>✓</strong></td></tr>
      <tr><td>Aspiration intégrée — chantier sans poussière</td><td><strong>✓</strong></td></tr>
      <tr><td>Vitrification Bona Mega Evo, 3 couches avec égrenage</td><td><strong>✓</strong></td></tr>
      <tr><td>Déplacement dans toute l'Île-de-France</td><td><strong>✓</strong></td></tr>
    </tbody>
  </table>

  <p>Le Bona Mega Evo est certifié <strong>EMICODE EC1PLUS</strong> et <strong>GREENGUARD Gold</strong>, sans <strong>PFAS</strong> — un air intérieur sain, disponible en finition mat, satiné ou brillant.</p>

  <h2>Ponçage parquet par département</h2>

  <p>Une page dédiée existe pour chaque commune. Trouvez la vôtre ci-dessous.</p>

{sections_html}

  <p><em>Vous ne trouvez pas votre commune ? François intervient dans toute l'Île-de-France : précisez votre ville lors du devis SMS, le tarif reste de 66 € TTC/m² tout compris. Voir aussi la page <a href="poncage-parquet-grand-paris.html">Ponçage parquet Grand Paris</a>.</em></p>

  <div class="cta-box">
    <h2>Demandez votre devis en Île-de-France</h2>
    <p>Tarif fixe 66 € TTC/m² tout compris — devis par SMS sur photos, sans déplacement.<br>Artisan indépendant : c'est moi qui réponds, c'est moi qui interviens.</p>
    <a class="cta-btn" href="sms:+33783925894">📲 Devis par SMS — 07 83 92 58 94</a>
</div>

</div>

<div class="faq-list">
  <div class="faq-item"><button class="faq-q" onclick="tog(this)">Combien coûte le ponçage d'un parquet en Île-de-France ?<span class="faq-icon">+</span></button><div class="faq-a">66 € TTC/m², tarif fixe tout compris : ponçage machine planétaire HTC, aspiration intégrée, vitrification Bona Mega Evo 3 couches et déplacement. Le prix est identique dans tout Paris et toute l'Île-de-France. Devis par SMS au 07 83 92 58 94.</div></div>
  <div class="faq-item"><button class="faq-q" onclick="tog(this)">Quels départements d'Île-de-France sont couverts ?<span class="faq-icon">+</span></button><div class="faq-a">François Gaillard intervient à Paris (75) et dans les Hauts-de-Seine (92), le Val-de-Marne (94), la Seine-Saint-Denis (93), les Yvelines (78) et l'Essonne (91). Une page dédiée existe pour chaque commune couverte.</div></div>
  <div class="faq-item"><button class="faq-q" onclick="tog(this)">Le déplacement est-il facturé en Île-de-France ?<span class="faq-icon">+</span></button><div class="faq-a">Non. Le déplacement est inclus dans le tarif de 66 € TTC/m², partout en Île-de-France, de Paris aux Yvelines. Aucun supplément à la facture.</div></div>
  <div class="faq-item"><button class="faq-q" onclick="tog(this)">Comment obtenir un devis pour ma commune ?<span class="faq-icon">+</span></button><div class="faq-a">Envoyez un SMS au 07 83 92 58 94 avec 3 ou 4 photos de votre parquet et la surface approximative. François répond avec un devis ferme, sans visite préalable ni déplacement.</div></div>
</div>
</main>
<footer>
  <p>© 2026 François Gaillard — Poncage Parquet Vitrification | Montrouge (92120) | 📞 07 83 92 58 94</p>
  <p style="margin-top:8px;">
    <a href="{BASE}" style="color:#f0c040;">← Retour au site</a>
</p>

  <p class="footer-meta-sm">150 avenue de la République · 92120 Montrouge · <a href="sms:+33783925894" class="c-muted">07 83 92 58 94</a> · SIRET 81182012500011</p>

  <p class="footer-meta-sm"><time datetime="2026-09-24">Mis à jour le 24 septembre 2026</time></p>
</footer>
<div id="cta-sticky" style="position:fixed;bottom:0;left:0;right:0;z-index:999;background:#1a1710;border-top:1px solid rgba(201,168,76,0.35);padding:10px 20px;display:none;align-items:center;justify-content:space-between;gap:12px;box-shadow:0 -4px 20px rgba(0,0,0,0.4);">
  <div class="flex-shrink-row">
    <span class="dot-dispo-lg"></span>
    <span class="brand-sm">Disponible · 66 € TTC/m²</span>
</div>
  <a href="sms:+33783925894" class="btn-or-inline" aria-label="Demander un devis par SMS">
    Devis par SMS · 07 83 92 58 94
</a>
  <button onclick="document.getElementById('cta-sticky').style.display='none';sessionStorage.setItem('ctaClosed','1')" class="btn-nav-close" aria-label="Fermer">×</button>
</div>

<div id="cta-sticky-mobile" style="position:fixed;bottom:0;left:0;right:0;z-index:999;background:#1a1710;border-top:1px solid rgba(201,168,76,0.35);padding:10px 16px 16px;display:none;flex-direction:column;gap:8px;box-shadow:0 -4px 20px rgba(0,0,0,0.4);">
  <div class="flex-row-between">
    <div class="flex-row-8">
      <span class="dot-dispo-sm"></span>
      <span class="brand-xs">Disponible · Lun–Sam 6h–22h · 66 € TTC/m²</span>
</div>
    <button onclick="document.getElementById('cta-sticky-mobile').style.display='none';sessionStorage.setItem('ctaClosed','1')" class="btn-nav-close" aria-label="Fermer">×</button>
</div>
  <a href="sms:+33783925894" class="btn-or-block" aria-label="Demander un devis par SMS">
    Devis par SMS — 07 83 92 58 94
</a>
</div>

<script>
(function(){{
  if(sessionStorage.getItem('ctaClosed')) return;
  var isMobile = window.innerWidth < 768;
  var sticky = document.getElementById(isMobile ? 'cta-sticky-mobile' : 'cta-sticky');
  var shown = false;
  function getFooterTop(){{
    var footer = document.querySelector('footer');
    return footer ? footer.getBoundingClientRect().top + window.scrollY - window.innerHeight - 60 : Infinity;
  }}
  function onScroll(){{
    var scrollY = window.scrollY;
    var nearFooter = scrollY > getFooterTop();
    if(!shown && scrollY > 300 && !nearFooter){{ sticky.style.display = 'flex'; shown = true; }}
    if(shown && nearFooter){{ sticky.style.display = 'none'; }}
    if(shown && !nearFooter && scrollY > 300){{ sticky.style.display = 'flex'; }}
  }}
  window.addEventListener('scroll', onScroll, {{passive:true}});
}})();
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","serviceType":"Ponçage et vitrification de parquet","provider":{{"@type":"HomeAndConstructionBusiness","name":"Ponçage Parquet Vitrification François","@id":"{BASE}#francois-gaillard"}},"areaServed":{{"@type":"AdministrativeArea","name":"Île-de-France"}},"offers":{{"@type":"Offer","price":"66","priceCurrency":"EUR","priceSpecification":{{"@type":"UnitPriceSpecification","price":"66","priceCurrency":"EUR","unitText":"m²","valueAddedTaxIncluded":true}}}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Accueil","item":"{BASE}"}},{{"@type":"ListItem","position":2,"name":"Ponçage parquet Île-de-France","item":"{BASE}poncage-parquet-ile-de-france.html"}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","url":"{BASE}poncage-parquet-ile-de-france.html","speakable":{{"@type":"SpeakableSpecification","cssSelector":["h1",".def-locale",".faq-a","h2"]}},"author":{{"@type":"Person","@id":"{BASE}#francois-gaillard","name":"François Gaillard"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Combien coûte le ponçage d'un parquet en Île-de-France ?","acceptedAnswer":{{"@type":"Answer","text":"66 € TTC/m², tarif fixe tout compris : ponçage machine planétaire HTC, aspiration intégrée, vitrification Bona Mega Evo 3 couches et déplacement. Le prix est identique dans tout Paris et toute l'Île-de-France. Devis par SMS au 07 83 92 58 94."}}}},{{"@type":"Question","name":"Quels départements d'Île-de-France sont couverts ?","acceptedAnswer":{{"@type":"Answer","text":"François Gaillard intervient à Paris (75) et dans les Hauts-de-Seine (92), le Val-de-Marne (94), la Seine-Saint-Denis (93), les Yvelines (78) et l'Essonne (91). Une page dédiée existe pour chaque commune couverte."}}}},{{"@type":"Question","name":"Le déplacement est-il facturé en Île-de-France ?","acceptedAnswer":{{"@type":"Answer","text":"Non. Le déplacement est inclus dans le tarif de 66 € TTC/m², partout en Île-de-France, de Paris aux Yvelines. Aucun supplément à la facture."}}}},{{"@type":"Question","name":"Comment obtenir un devis pour ma commune ?","acceptedAnswer":{{"@type":"Answer","text":"Envoyez un SMS au 07 83 92 58 94 avec 3 ou 4 photos de votre parquet et la surface approximative. François répond avec un devis ferme, sans visite préalable ni déplacement."}}}}]}}
</script>
<script>function tog(b){{var a=b.nextElementSibling;var o=b.classList.contains("open");document.querySelectorAll(".faq-q.open").forEach(function(x){{x.classList.remove("open");x.nextElementSibling.style.maxHeight="0"}});if(!o){{b.classList.add("open");a.style.maxHeight=a.scrollHeight+"px"}}}}</script>
</body>
</html>
'''

open("poncage-parquet-ile-de-france.html","w",encoding='utf-8').write(html)
print("Page ecrite:", len(html), "octets")

# ------ MAILLAGE RETOUR ------
import glob as _glob
SELF = "poncage-parquet-ile-de-france.html"
OLD = '<a href="vitrification-parquet-paris.html" class="c-muted">Vitrification parquet Paris</a></p>'
NEW = OLD[:-4] + ' · <a href="poncage-parquet-ile-de-france.html" class="c-muted">Île-de-France</a></p>'
nfoot = 0
for f in _glob.glob("*.html"):
    if f == SELF: continue
    h = open(f, encoding='utf-8').read()
    if OLD in h and 'class="c-muted">Île-de-France</a>' not in h:
        open(f,'w',encoding='utf-8').write(h.replace(OLD, NEW, 1)); nfoot += 1
gp = "poncage-parquet-grand-paris.html"
if os.path.exists(gp):
    h = open(gp, encoding='utf-8').read()
    old_gp = '<a href="index.html">Voir toute la zone d\'intervention →</a>'
    new_gp = '<a href="poncage-parquet-ile-de-france.html">Voir toute la zone d\'intervention en Île-de-France →</a>'
    if old_gp in h:
        open(gp,'w',encoding='utf-8').write(h.replace(old_gp, new_gp, 1)); print("backlink grand-paris: OK")
print("footer backlinks ajoutes:", nfoot)
