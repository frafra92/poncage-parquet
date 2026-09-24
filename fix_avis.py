# -*- coding: utf-8 -*-
"""Corrige l'erreur Search Console "L'avis contient plusieurs notes cumulees".
Certaines pages declarent aggregateRating dans plusieurs blocs JSON-LD (entites
LocalBusiness repetees). Google n'accepte qu'UNE note par entite.
-> on garde la 1re note et on retire aggregateRating des blocs suivants.
On normalise aussi la note conservee sur la valeur canonique 4,9 / 220."""
import re, json

PAGES = ["poncage-parquet-montrouge.html",
         "specialiste-parquet-ancien-paris.html",
         "prix-poncage-parquet-paris.html",
         "a-propos-francois-gaillard-parqueteur-paris.html"]

CANON = {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "220",
         "bestRating": "5", "worstRating": "1"}

def strip_rating(o):
    if isinstance(o, dict):
        o.pop('aggregateRating', None)
        for v in o.values(): strip_rating(v)
    elif isinstance(o, list):
        for v in o: strip_rating(v)

def set_canon_first(o, state):
    if state['done']: return
    if isinstance(o, dict):
        if 'aggregateRating' in o and not state['done']:
            o['aggregateRating'] = dict(CANON); state['done'] = True; return
        for v in o.values(): set_canon_first(v, state)
    elif isinstance(o, list):
        for v in o: set_canon_first(v, state)

for f in PAGES:
    h = open(f, encoding='utf-8').read()
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', h, re.S))
    seen = False
    repls = []
    for m in blocks:
        content = m.group(2)
        if 'aggregateRating' not in content:
            continue
        d = json.loads(content)
        if not seen:
            seen = True
            set_canon_first(d, {'done': False})
        else:
            strip_rating(d)
        repls.append((m.start(2), m.end(2), json.dumps(d, ensure_ascii=False, separators=(',', ':'))))
    for start, end, rep in sorted(repls, reverse=True):
        h = h[:start] + rep + h[end:]
    open(f, 'w', encoding='utf-8').write(h)
    print(f, "-> aggregateRating restants:", h.count('aggregateRating'))
