# 🔴 BONUS : Corrections à faire dans index.html (Journal Site)

D'après votre journal `JOURNAL_SITE.md`, voici les 5 erreurs à corriger dans votre `index.html` actuel :

---

## Erreur 1 : Déplacer les JSON-LD
**Problème** : Les 3 blocs JSON-LD sont au début avant `<head>` (position invalide)

**À faire** :
- Couper les 3 blocs `<script type="application/ld+json">...</script>`
- Les coller juste **avant** `</head>` (dernière ligne de la section HEAD)

---

## Erreur 2 : Corriger l'adresse postale
**Problème** : `"streetAddress": "Montrouge"` est incomplète

**À remplacer** :
```json
"streetAddress": "Montrouge"
```

**Par** :
```json
"streetAddress": "150 Avenue de la République"
```

---

## Erreur 3 : Supprimer la balise de fermeture dupliquée
**Problème** : `</noscript></noscript>` — fermeture en doublon

**À trouver** et **à remplacer** :
```html
</noscript></noscript>
```

**Par** :
```html
</noscript>
```

---

## Erreur 4 : Corriger le lien cassé dans le H3
**Problème** : `</a></a></h3>` — lien fermé deux fois (malformé)

**Cherchez** :
```html
<h3>... Vitrification Bona ... </a></a></h3>
```

**Simplifiez en** :
```html
<h3><a href="...">Vitrification Bona Mega Evo</a></h3>
```

---

## Erreur 5 : Corriger l'Open Graph URL
**Problème** : `og:url` pointe vers `.com/index.html"` (inutile)

**À remplacer** :
```html
<meta property="og:url" content="https://poncageparquetvitrificationfrancois.com/index.html">
```

**Par** :
```html
<meta property="og:url" content="https://poncageparquetvitrificationfrancois.com/">
```

---

## 📋 Checklist des 5 corrections

- [ ] Erreur 1 : Déplacer JSON-LD avant `</head>`
- [ ] Erreur 2 : Corriger `"streetAddress": "150 Avenue de la République"`
- [ ] Erreur 3 : Supprimer doublon `</noscript>`
- [ ] Erreur 4 : Corriger lien Bona cassé
- [ ] Erreur 5 : Corriger `og:url` sans `/index.html`

---

**Conseil** : Validez avec https://validator.w3.org/ après corrections ✅