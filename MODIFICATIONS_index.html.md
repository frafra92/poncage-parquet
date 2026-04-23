# 📝 MODIFICATIONS À FAIRE DANS index.html

## Ajouter une section "Cas d'études prestigieux" ou "Châteaux historiques"

Cherchez une section convenable (après les services ou avant le footer) et ajoutez ceci :

```html
<!-- Section : Cas d'étude - Château de Bazens -->
<section style="background-color: var(--gris-moyen); padding: 3rem 2rem; margin: 3rem 0; border-left: 4px solid var(--or);">
    <div style="max-width: 900px; margin: 0 auto;">
        <h2 style="font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; color: var(--or); margin-bottom: 1.5rem;">
            🏰 Nos Cas d'Études
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
            
            <!-- Château de Bazens -->
            <a href="/chateau-bazens-poncage-parquet-agen.html" style="text-decoration: none; color: inherit;">
                <div style="background-color: var(--noir); padding: 1.5rem; border: 2px solid var(--or); border-radius: 4px; transition: all 0.3s ease; cursor: pointer;" 
                     onmouseover="this.style.backgroundColor='var(--gris-clair)'; this.style.transform='translateY(-5px)'" 
                     onmouseout="this.style.backgroundColor='var(--noir)'; this.style.transform='translateY(0)'">
                    <h3 style="font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; color: var(--or); margin-bottom: 0.8rem;">
                        Château de Bazens
                    </h3>
                    <p style="color: var(--texte); font-size: 0.95rem; margin-bottom: 0.8rem;">
                        <strong>350 m²</strong> de peuplier séculaire (300 ans)
                    </p>
                    <p style="color: #999; font-size: 0.9rem; margin-bottom: 1rem;">
                        Légende romantique | Agen
                    </p>
                    <p style="color: var(--or); font-size: 0.9rem;">
                        Voir le chantier → <span style="font-weight: bold;">▶</span>
                    </p>
                </div>
            </a>

        </div>

        <p style="color: #999; font-size: 0.9rem; margin-top: 2rem; text-align: center;">
            Découvrez nos réalisations majeures en parqueterie historique.
        </p>
    </div>
</section>
```

---

## Alternative : Ajouter un lien simple dans la navigation ou le menu

Si vous préférez une approche plus minimaliste, ajoutez simplement ceci dans votre menu de navigation :

```html
<li>
    <a href="/chateau-bazens-poncage-parquet-agen.html" style="color: var(--or);">
        🏰 Château de Bazens
    </a>
</li>
```

---

## ✅ Checklist après modifications

- [ ] Ajouter le lien/section à `index.html`
- [ ] Uploader `sitemap.xml` mis à jour
- [ ] Uploader `chateau-bazens-poncage-parquet-agen.html`
- [ ] Valider le sitemap dans Google Search Console
- [ ] Tester les 4 vidéos YouTube (responsive)
- [ ] Vérifier que l'URL `.com/chateau-bazens...` fonctionne correctement