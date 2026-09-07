#!/usr/bin/env python3
"""Régénère sitemap.xml à partir des pages HTML présentes à la racine du site.

Règles :
- Une page déjà présente dans sitemap.xml garde sa priorité, son changefreq
  et ses éventuelles images (extension sitemap-image) : ce sont des réglages
  éditoriaux, le script ne les écrase jamais.
- Le lastmod de chaque page est recalculé à partir de la date du dernier
  commit git qui la touche (nécessite un historique complet, voir workflow).
- Une nouvelle page (jamais vue dans sitemap.xml) est ajoutée automatiquement
  avec une priorité/changefreq par défaut déduite du nom de fichier.
- Une page qui disparaît du dépôt est retirée du sitemap.
- Les fichiers techniques (404, vérifications moteurs de recherche, pages de
  test/brouillon) sont exclus, voir EXCLUDED_FILES et les motifs ci-dessous.
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

DOMAIN = "https://poncageparquetvitrificationfrancois.com"
SITEMAP_PATH = Path("sitemap.xml")
ROOT = Path(__file__).resolve().parent

# Fichiers techniques ou brouillons/superseded qui ne doivent jamais
# apparaître dans le sitemap, même s'ils existent à la racine.
EXCLUDED_FILES = {
    "404.html",
    "apercu-sable.html",  # outil de prévisualisation interne
    "article1-choisir-parqueteur-paris.html",  # remplacé par choisir-artisan-poncage-parquet-paris.html
    "badge-partenaire-parquet-paris.html",  # widget d'intégration, pas une page de contenu
    "blog-entretien-parquet-paris.html",  # remplacé par entretien-parquet-vitrifie-paris.html
    "blog-huilage-vs-vitrification.html",  # remplacé par comparatif-vitrification-huilage-cire-parquet.html
    "comparatif-artisan-independant-vs-entreprise-parquet.html",  # remplacé par article3-artisan-independant-vs-entreprise-paris.html
    "comparatif-machine-planetaire-vs-tambour-parquet.html",  # remplacé par machine-planetaire-vs-tambour-parquet.html
    "comparatif-poncer-vs-remplacer-parquet-paris.html",  # brouillon
    "fanout-parquet-ancien-paris-ia.html",  # page de test GEO/AEO
    "query-fanout-parquet-paris-ia.html",  # page de test GEO/AEO
    "guide-choisir-artisan-parqueteur-paris.html",  # remplacé par choisir-artisan-poncage-parquet-paris.html
    "guide-entretien-parquet-vitrifie.html",  # remplacé par entretien-parquet-vitrifie-paris.html
    "machine-planetaire-poncage-parquet.html",  # remplacé par machine-planetaire-vs-tambour-parquet.html
    "parquet-heritage-louis-xiv-haussmann.html",  # remplacé par parquet-haussmannien-heritage-louis-xiv.html
    "peinture-avant-apres-poncage-parquet.html",  # remplacé par peinture-avant-ou-apres-poncage-parquet.html
    "phi.html",  # page de test technique
    "poncage-parquet-grand-paris.html",  # remplacé par les pages par arrondissement/commune
    "poncage-parquet-vitrification-mat-satine-brillant-paris.html",  # remplacé par comparatif-finition-parquet-mat-satine-brillant.html
    "redirect-ipfs.html",  # redirection technique, Disallow dans robots.txt
    "reparation-parquet-degat-des-eaux-paris.html",  # remplacé par reparation-parquet-paris.html
    "restaurer-parquet-ancien-paris.html",  # remplacé par specialiste-parquet-ancien-paris.html
    "vitrificateur-parquet-paris.html",  # remplacé par vitrification-parquet-paris.html
}

# Motifs de fichiers techniques génériques (vérifications de propriété de
# domaine ajoutées par Google/Bing/Pinterest/etc., toujours à la racine).
EXCLUDED_PATTERNS = [
    re.compile(r"^google[0-9a-f]+\.html$"),
    re.compile(r"^yandex_[0-9a-f]+\.html$"),
    re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.html$"),  # UUID de vérification
    re.compile(r"^[0-9a-f]{32}\.html$"),  # jeton de vérification hexadécimal
]

URL_BLOCK_RE = re.compile(r"[ \t]*<url>.*?</url>\s*", re.DOTALL)
LOC_RE = re.compile(r"<loc>(.*?)</loc>")
CHANGEFREQ_RE = re.compile(r"<changefreq>(.*?)</changefreq>")
PRIORITY_RE = re.compile(r"<priority>(.*?)</priority>")
IMAGE_BLOCK_RE = re.compile(r"[ \t]*<ns1:image>.*?</ns1:image>\s*", re.DOTALL)


def is_excluded(filename: str) -> bool:
    if filename in EXCLUDED_FILES:
        return True
    return any(p.match(filename) for p in EXCLUDED_PATTERNS)


def default_priority_changefreq(filename: str) -> tuple[str, str]:
    """Valeurs par défaut pour une page jamais encore vue dans le sitemap."""
    if filename == "index.html":
        return "1.0", "weekly"
    if filename == "poncage-parquet-montrouge.html":
        return "0.9", "weekly"  # base de l'artisan
    if filename == "blog.html":
        return "0.8", "monthly"
    if filename == "mentions-legales.html":
        return "0.3", "yearly"
    if filename == "plan-du-site.html":
        return "0.4", "monthly"
    if re.match(r"^poncage-parquet-paris-\d+\.html$", filename):
        return "0.8", "monthly"  # pages arrondissement
    if re.search(r"\b(devis|prix|expert|specialiste)\b", filename):
        return "0.9", "weekly"  # pages à forte intention commerciale
    if filename.startswith("poncage-parquet-"):
        return "0.7", "monthly"  # pages commune/quartier
    if filename.startswith("blog-"):
        return "0.7", "monthly"
    return "0.6", "monthly"


def git_lastmod(filename: str) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", filename],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        out = ""
    return out or date.today().isoformat()


def parse_existing_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for match in URL_BLOCK_RE.finditer(text):
        block = match.group(0)
        loc_match = LOC_RE.search(block)
        if not loc_match:
            continue
        filename = loc_match.group(1).rsplit("/", 1)[-1]
        blocks[filename] = block
    return blocks


def build_block(filename: str, lastmod: str, changefreq: str, priority: str, images_xml: str) -> str:
    return (
        "  <url>\n"
        f"    <loc>{DOMAIN}/{filename}</loc>\n"
        f"{images_xml}"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def main() -> None:
    existing_text = SITEMAP_PATH.read_text(encoding="utf-8") if SITEMAP_PATH.exists() else ""
    existing_blocks = parse_existing_blocks(existing_text)

    html_files = sorted(
        f.name for f in ROOT.iterdir() if f.is_file() and f.suffix == ".html"
    )
    included_files = [f for f in html_files if not is_excluded(f)]

    added, removed, updated = [], [], []

    stale = set(existing_blocks) - set(included_files)
    removed.extend(sorted(stale))

    entries = []
    for filename in included_files:
        lastmod = git_lastmod(filename)
        old_block = existing_blocks.get(filename)
        if old_block is None:
            priority, changefreq = default_priority_changefreq(filename)
            images_xml = ""
            added.append(filename)
        else:
            changefreq_match = CHANGEFREQ_RE.search(old_block)
            priority_match = PRIORITY_RE.search(old_block)
            changefreq = changefreq_match.group(1) if changefreq_match else "monthly"
            priority = priority_match.group(1) if priority_match else "0.6"
            images_xml = "".join(m.group(0) for m in IMAGE_BLOCK_RE.finditer(old_block))
            old_lastmod_match = re.search(r"<lastmod>(.*?)</lastmod>", old_block)
            if old_lastmod_match and old_lastmod_match.group(1) != lastmod:
                updated.append(filename)
        entries.append((filename, build_block(filename, lastmod, changefreq, priority, images_xml)))

    # index.html en tête, puis ordre alphabétique.
    entries.sort(key=lambda item: (item[0] != "index.html", item[0]))

    lines = [
        "<?xml version='1.0' encoding='utf-8'?>\n",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:ns1="http://www.google.com/schemas/sitemap-image/1.1">\n',
    ]
    lines.extend(block for _, block in entries)
    lines.append("</urlset>\n")

    new_text = "".join(lines)
    changed = new_text != existing_text
    SITEMAP_PATH.write_text(new_text, encoding="utf-8")

    print(f"Pages dans le sitemap : {len(entries)}")
    if added:
        print(f"Ajoutées ({len(added)}) : {', '.join(added)}")
    if removed:
        print(f"Retirées ({len(removed)}) : {', '.join(removed)}")
    if updated:
        print(f"Lastmod mis à jour ({len(updated)}) : {', '.join(updated)}")
    if not (added or removed or updated):
        print("Aucun changement de contenu (lastmod inclus).")
    print("sitemap.xml modifié." if changed else "sitemap.xml déjà à jour.")


if __name__ == "__main__":
    sys.exit(main())
