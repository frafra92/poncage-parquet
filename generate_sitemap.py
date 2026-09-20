#!/usr/bin/env python3
"""
Génère sitemap.xml automatiquement à partir des pages .html du dépôt.

Principes :
- Scanne tous les .html à la racine.
- EXCLUT automatiquement : les pages techniques (404, vérif Google, noms UUID)
  ET toute page de REDIRECTION (meta http-equiv="refresh") — donc les pages
  regroupées/redirigées ne polluent jamais le sitemap, sans liste à tenir.
- PRÉSERVE la priority et la changefreq déjà définies pour chaque URL dans
  l'ancien sitemap (ta pondération SEO n'est jamais écrasée).
- Les nouvelles pages arrivent avec des valeurs par défaut (modifiables plus bas).
- lastmod = date du dernier commit git qui a touché le fichier. Repli sur la
  date du jour si le fichier n'est pas encore suivi par git.
- La home (index.html) garde sa forme actuelle (.../index.html).

Pour forcer l'exclusion d'une page : ajouter son nom dans EXCLUDE_FILES.
"""

import glob
import re
import subprocess
from datetime import date
from xml.dom import minidom

# ------------------------------------------------------------------ réglages
BASE_URL = "https://poncageparquetvitrificationfrancois.com"

# Exclusions explicites (en plus de la détection auto des redirections).
EXCLUDE_FILES = {
    "404.html",
}

# Motifs exclus : vérification Search Console (google….html) et noms techniques (UUID).
EXCLUDE_PATTERNS = [
    re.compile(r"^google[0-9a-f]+\.html$", re.I),
    re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.html$", re.I),
]

# Valeurs par défaut pour toute NOUVELLE page.
DEFAULT_PRIORITY = "0.7"
DEFAULT_CHANGEFREQ = "monthly"

# Cas particuliers (appliqués si la page n'est pas déjà dans l'ancien sitemap).
SPECIAL = {
    "index.html": {"priority": "1.0", "changefreq": "weekly"},
}

# Détection de redirection : meta refresh (insensible à la casse, espaces variables).
REDIRECT_RE = re.compile(r"http-equiv\s*=\s*[\"']?refresh", re.I)
# --------------------------------------------------------------------------


def is_excluded(name):
    if name in EXCLUDE_FILES:
        return True
    return any(p.match(name) for p in EXCLUDE_PATTERNS)


def is_redirect(name):
    try:
        with open(name, encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4000)  # le meta refresh est toujours dans le <head>
        return bool(REDIRECT_RE.search(head))
    except OSError:
        return False


def load_existing(path):
    """Renvoie {url: (priority, changefreq)} depuis l'ancien sitemap."""
    prev = {}
    try:
        doc = minidom.parse(path)
    except Exception:
        return prev
    for url in doc.getElementsByTagName("url"):
        def txt(tag):
            n = url.getElementsByTagName(tag)
            return n[0].firstChild.nodeValue.strip() if n and n[0].firstChild else None
        loc = txt("loc")
        if loc:
            prev[loc] = (txt("priority"), txt("changefreq"))
    return prev


def git_lastmod(name):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", name],
            capture_output=True, text=True, timeout=15,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return date.today().isoformat()


def main():
    existing = load_existing("sitemap.xml")
    files = sorted(
        f for f in glob.glob("*.html")
        if not is_excluded(f) and not is_redirect(f)
    )

    lines = [
        "<?xml version='1.0' encoding='utf-8'?>",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:ns1="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    added = []
    for name in files:
        loc = f"{BASE_URL}/{name}"
        prev = existing.get(loc)
        if prev:
            priority = prev[0] or DEFAULT_PRIORITY
            changefreq = prev[1] or DEFAULT_CHANGEFREQ
        else:
            sp = SPECIAL.get(name, {})
            priority = sp.get("priority", DEFAULT_PRIORITY)
            changefreq = sp.get("changefreq", DEFAULT_CHANGEFREQ)
            added.append(name)

        lastmod = git_lastmod(name)
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{changefreq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]

    lines.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"Sitemap généré : {len(files)} pages.")
    if added:
        print(f"{len(added)} nouvelle(s) page(s) ajoutée(s) :")
        for n in added:
            print(f"  + {n}")


if __name__ == "__main__":
    main()
