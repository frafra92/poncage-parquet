#!/usr/bin/env python3
"""
Validateur SEO pour site parqueteur François Gaillard
Vérifie : JSON-LD, meta descriptions, canonical, images, accessibilité
Utilisation : python3 validator.py chemin/vers/dossier
"""

import os
import re
import sys
from pathlib import Path

class SEOValidator:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.issues = []
        self.warnings = []
        self.success = []

    def validate_file(self, filepath):
        """Valide un fichier HTML unique"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.issues.append(f"❌ {filepath}: Impossible de lire ({e})")
            return

        filename = filepath.name
        print(f"\n📄 Validation: {filename}")
        print("=" * 60)

        # 1. EMAIL VALIDE
        if "francoisgaillard92@outlook.fr.com" in content:
            self.issues.append(f"❌ {filename}: Email invalide (.fr.com)")
        elif "francoisgaillard92@outlook.fr" in content:
            self.success.append(f"✓ {filename}: Email correct (outlook.fr)")

        # 2. JSON-LD
        json_ld_count = content.count('type="application/ld+json"')
        if json_ld_count == 0:
            self.issues.append(f"❌ {filename}: Pas de JSON-LD trouvé")
        elif json_ld_count == 1:
            self.success.append(f"✓ {filename}: 1 JSON-LD détecté")
        else:
            self.warnings.append(f"⚠ {filename}: {json_ld_count} JSON-LD (considérer fusion)")

        # 3. META DESCRIPTION
        meta_desc = re.search(r'<meta name="description" content="([^"]+)"', content)
        if not meta_desc:
            self.issues.append(f"❌ {filename}: Meta description manquante")
        else:
            desc_len = len(meta_desc.group(1))
            if 120 <= desc_len <= 160:
                self.success.append(f"✓ {filename}: Meta description OK ({desc_len} chars)")
            else:
                self.warnings.append(f"⚠ {filename}: Description trop {'courte' if desc_len < 120 else 'longue'} ({desc_len} chars, viser 120-160)")

        # 4. CANONICAL
        if '<link rel="canonical"' in content:
            self.success.append(f"✓ {filename}: Canonical présent")
        else:
            self.warnings.append(f"⚠ {filename}: Canonical manquant")

        # 5. TITLE TAG
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if not title_match:
            self.issues.append(f"❌ {filename}: Title tag manquant")
        else:
            title_len = len(title_match.group(1))
            if 50 <= title_len <= 70:
                self.success.append(f"✓ {filename}: Title OK ({title_len} chars)")
            else:
                self.warnings.append(f"⚠ {filename}: Title trop {'court' if title_len < 50 else 'long'} ({title_len} chars, viser 50-70)")

        # 6. H1
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        if h1_count == 0:
            self.issues.append(f"❌ {filename}: H1 manquant")
        elif h1_count == 1:
            self.success.append(f"✓ {filename}: Un H1 présent")
        else:
            self.issues.append(f"❌ {filename}: {h1_count} H1 trouvés (max 1)")

        # 7. ALT TEXT
        img_tags = re.findall(r'<img[^>]+>', content)
        if img_tags:
            img_without_alt = [img for img in img_tags if 'alt=' not in img]
            if img_without_alt:
                self.issues.append(f"❌ {filename}: {len(img_without_alt)} images sans alt text")
            else:
                self.success.append(f"✓ {filename}: Tous les alt text présents ({len(img_tags)} images)")

        # 8. VIEWPORT
        if 'name="viewport"' in content:
            self.success.append(f"✓ {filename}: Viewport meta tag OK")
        else:
            self.issues.append(f"❌ {filename}: Viewport meta tag manquant (mobile)")

        # 9. OPEN GRAPH
        og_tags = re.findall(r'<meta property="og:', content)
        if og_tags:
            self.success.append(f"✓ {filename}: Open Graph tags ({len(og_tags)})")
        else:
            self.warnings.append(f"⚠ {filename}: Pas de balises Open Graph")

        # 10. BALISES MAL FERMÉES
        broken_tags = re.findall(r'<[a-z]+[^>]*>[^<]*</[^>]+>[^<]*</[a-z]+>', content, re.IGNORECASE)
        if broken_tags:
            self.issues.append(f"❌ {filename}: {len(broken_tags)} balises possiblement mal fermées détectées")

        # 11. STRUCTURED DATA (FAQPage, LocalBusiness)
        if '"@type": "FAQPage"' in content or '"@type":"FAQPage"' in content:
            self.success.append(f"✓ {filename}: FAQPage schema trouvé")
        if '"@type": "LocalBusiness"' in content or '"@type":"LocalBusiness"' in content:
            self.success.append(f"✓ {filename}: LocalBusiness schema trouvé")

        # 12. SITEMAP/ROBOTS
        if 'robots' not in filename:
            if 'meta name="robots"' not in content:
                self.warnings.append(f"⚠ {filename}: Robots meta tag manquant")

        # 13. FONTS - PRELOAD/PRECONNECT
        if 'rel="preconnect" href="https://fonts.googleapis.com"' in content:
            self.success.append(f"✓ {filename}: Preconnect fonts présent (perf)")
        else:
            self.warnings.append(f"⚠ {filename}: Pas de preconnect fonts (petite amélioration perf possible)")

        # 14. ENCODING
        if 'charset="UTF-8"' in content or "charset='UTF-8'" in content:
            self.success.append(f"✓ {filename}: Encoding UTF-8 spécifié")

        # 15. INTERNAL LINKS
        internal_links = len(re.findall(r'href="[a-z0-9-]+\.html', content))
        if internal_links > 0:
            self.success.append(f"✓ {filename}: {internal_links} liens internes trouvés")

    def validate_directory(self):
        """Valide tous les fichiers .html du répertoire"""
        html_files = list(self.directory.glob('*.html'))
        
        if not html_files:
            print(f"❌ Aucun fichier .html trouvé dans {self.directory}")
            return

        print(f"🔍 Validation de {len(html_files)} fichiers HTML")
        print("=" * 60)

        for html_file in sorted(html_files):
            self.validate_file(html_file)

    def report(self):
        """Affiche le rapport final"""
        print("\n" + "=" * 60)
        print("📋 RAPPORT FINAL")
        print("=" * 60)

        if self.success:
            print(f"\n✅ Succès ({len(self.success)}):")
            for item in self.success[:10]:
                print(f"  {item}")
            if len(self.success) > 10:
                print(f"  ... et {len(self.success) - 10} autres")

        if self.warnings:
            print(f"\n⚠️  Avertissements ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"  {item}")

        if self.issues:
            print(f"\n❌ Problèmes ({len(self.issues)}):")
            for item in self.issues:
                print(f"  {item}")

        # Résumé
        total = len(self.success) + len(self.warnings) + len(self.issues)
        score = (len(self.success) / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print(f"Score SEO: {score:.0f}%")
        if score >= 80:
            print("🎯 Très bon ! Site SEO-friendly")
        elif score >= 60:
            print("👍 Bon. Quelques améliorations recommandées")
        else:
            print("📌 À améliorer. Lire les recommandations ci-dessus")
        print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validator.py /chemin/vers/site")
        print("Exemple: python3 validator.py .")
        sys.exit(1)

    directory = sys.argv[1]
    validator = SEOValidator(directory)
    validator.validate_directory()
    validator.report()
