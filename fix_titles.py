# -*- coding: utf-8 -*-
"""Reecrit la balise <title> des 3 pages les plus visitees (regle : mot-cle +
chiffre au debut, marque a la fin, < 60 car)."""
CHANGES = [
    ("index.html",
     "<title>Ponçage parquet Paris — François Gaillard, artisan · 66 €/m²</title>",
     "<title>Ponçage parquet Paris 66 €/m² — François Gaillard</title>"),
    ("peinture-avant-ou-apres-poncage-parquet.html",
     "<title>Peinture avant ou après le ponçage de parquet ? La</title>",
     "<title>Peinture avant ou après ponçage du parquet ? Le bon ordre</title>"),
    ("reboucher-joints-parquet-paris-dtu-guide.html",
     "<title>Joints de parquet : faut-il les reboucher ? — Guide expert DTU</title>",
     "<title>Reboucher les joints d'un parquet ancien — Guide DTU</title>"),
]
for f, old, new in CHANGES:
    h = open(f, encoding='utf-8').read()
    assert old in h, f"{f}: title actuel introuvable"
    open(f, 'w', encoding='utf-8').write(h.replace(old, new, 1))
    print(f, "-> OK")
