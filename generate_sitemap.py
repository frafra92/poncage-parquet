#!/usr/bin/env python3
"""
Génère sitemap.xml automatiquement à partir des pages .html du dépôt.

Principes :
- Scanne tous les .html à la racine.
- EXCLUT automatiquement : les pages techniques (404, vérif Google, noms UUID),
  les REDIRECTIONS (meta http-equiv="refresh"), les pages NOINDEX (meta robots),
  et les pages NON-CANONIQUES (canonical pointant vers une autre URL) — donc les
  pages regroupées/redirigées/dupliquées ne polluent jamais le sitemap.
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
# Détection noindex : <meta name="robots" ... noindex ...>
NOINDEX_RE = re.compile(r"<meta[^>]*name=[\"']robots[\"'][^>]*noindex", re.I)
# Détection du lien canonique.
CANONICAL_RE = re.compile(r"<link[^>]*rel=[\"']canonical[\"'][^>]*>", re.I)
HREF_RE = re.compile(r"href=[\"'](.*?)[\"']", re.I)
# --------------------------------------------------------------------------


def _head(name):
    try:
        with open(name, encoding="utf-8", errors="ignore") as fh:
            return fh.read(8000)  # <head> complet (meta refresh, robots, canonical)
    except OSError:
        return ""


def is_excluded(name):
    if name in EXCLUDE_FILES:
        return True
    return any(p.match(name) for p in EXCLUDE_PATTERNS)


def is_redirect(name):
    return bool(REDIRECT_RE.search(_head(name)))


def is_noindex(name):
    return bool(NOINDEX_RE.search(_head(name)))


def _norm_url(u):
    """Normalise pour comparer : enlève le slash final et un éventuel /index.html."""
    n = u.strip().rstrip("/")
    if n.endswith("/index.html"):
        n = n[: -len("/index.html")]
    return n


def is_non_canonical(name, own_url):
    """Vrai si la page déclare un canonical vers une AUTRE URL qu'elle-même."""
    m = CANONICAL_RE.search(_head(name))
    if not m:
        return False
    h = HREF_RE.search(m.group(0))
    if not h:
        return False
    return _norm_url(h.group(1)) != _norm_url(own_url)


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


def magazine_loc(path):
    """Chemin de fichier -> URL répertoire (trailing slash), index.html retiré."""
    rel = path[:-len("index.html")] if path.endswith("index.html") else path
    rel = rel.strip("/")
    return f"{BASE_URL}/{rel}/" if rel else f"{BASE_URL}/"


def main():
    existing = load_existing("sitemap.xml")

    # Pages à la racine (comportement historique : .../page.html)
    root_files = sorted(
        f for f in glob.glob("*.html")
        if not is_excluded(f)
        and not is_redirect(f)
        and not is_noindex(f)
        and not is_non_canonical(f, f"{BASE_URL}/{f}")
    )
    # Rubrique éditoriale "Les Secrets du Parquet" : URLs répertoire (.../.../).
    mag_files = sorted(
        f for f in glob.glob("les-secrets-du-parquet/**/index.html", recursive=True)
        if not is_redirect(f)
        and not is_noindex(f)
        and not is_non_canonical(f, magazine_loc(f))
    )

    # (loc, fichier_pour_lastmod, priorité_defaut, changefreq_defaut)
    entries = []
    for name in root_files:
        sp = SPECIAL.get(name, {})
        entries.append((f"{BASE_URL}/{name}", name,
                        sp.get("priority", DEFAULT_PRIORITY),
                        sp.get("changefreq", DEFAULT_CHANGEFREQ)))
    for path in mag_files:
        pr = "0.8" if path == "les-secrets-du-parquet/index.html" else "0.7"
        entries.append((magazine_loc(path), path, pr, "monthly"))

    lines = [
        "<?xml version='1.0' encoding='utf-8'?>",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:ns1="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    added = []
    for loc, fname, def_priority, def_changefreq in entries:
        prev = existing.get(loc)
        if prev:
            priority = prev[0] or def_priority
            changefreq = prev[1] or def_changefreq
        else:
            priority = def_priority
            changefreq = def_changefreq
            added.append(loc)

        lastmod = git_lastmod(fname)
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

    print(f"Sitemap généré : {len(entries)} pages ({len(mag_files)} magazine).")
    if added:
        print(f"{len(added)} nouvelle(s) page(s) ajoutée(s) :")
        for n in added:
            print(f"  + {n}")


if __name__ == "__main__":
    main()
