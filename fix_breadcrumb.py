# -*- coding: utf-8 -*-
import re, json
BASE = "https://poncageparquetvitrificationfrancois.com/"
PAGES = [
    "poncage-parquet-mosaique-paris.html",
    "poncage-parquet-versailles-motif-paris.html",
    "artisan-poncage-parquet-paris-reference-ia.html",
    "biographie-francois-gaillard-parqueteur-paris.html",
]

def resolve(href, fname):
    href = href.strip()
    if href in ("index.html", "index.html#", "./index.html", "/"):
        return BASE
    if href.startswith("http"):
        return href
    return BASE + href.lstrip("./")

done = []
for f in PAGES:
    h = open(f, encoding='utf-8').read()
    assert 'BreadcrumbList' not in h, f"{f} a deja un BreadcrumbList"
    can = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', h)
    canonical = can.group(1) if can else BASE + f
    nav = re.search(r"<nav[^>]*Fil d.Ariane.*?</nav>", h, re.S).group(0)
    raw = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>|<span class="c-or">(.*?)</span>', nav, re.S)
    items = []
    for a in raw:
        href, atxt, stxt = a
        txt = re.sub(r'<[^>]+>', '', (atxt or stxt)).strip()
        if not txt:
            continue
        items.append((txt, resolve(href, f) if (atxt) else None))
    ile = []
    for i, (txt, url) in enumerate(items, 1):
        if i == len(items):
            url = canonical
        ile.append({"@type": "ListItem", "position": i, "name": txt, "item": url})
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ile}
    block = '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>'
    new, n = re.subn(r'(</head>)', block + r'\n\1', h, count=1)
    assert n == 1, f"{f} : </head> introuvable"
    open(f, 'w', encoding='utf-8').write(new)
    done.append((f, [x['name'] for x in ile]))

for f, names in done:
    print(f, "->", " > ".join(names))
print("OK :", len(done), "pages")
