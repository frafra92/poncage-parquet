# Fiche — prix-poncage-parquet-paris.html

> Fiche rétroactive (page déjà en ligne), créée le 2026-10-20 comme premier exemple du cadre Intention → Spéc → Plan → Revue.

## Intention
- Requête cible (une seule) : « prix ponçage parquet Paris au m² »
- Objectif prioritaire : être citée par les IA sur le coût + ranker Google + déclencher un SMS
- Public visé : particuliers parisiens/franciliens qui cherchent combien coûte un ponçage/vitrification

## Spécification (ce que la page doit contenir)
- Bloc réponse directe AEO : oui (« Le ponçage parquet à Paris coûte 66 € TTC/m²… »)
- Prix 66 € visible sans scroller : oui
- FAQ : 10 questions (dont « Combien coûte le ponçage d'un parquet à Paris au m² ? »)
- Schema.org : LocalBusiness, Service, FAQPage, HowTo, BreadcrumbList, Article, Organization, Person
- Maillage interne : 7 pages sœurs
- Formulation poussière : « dispersion très réduite… », jamais « sans poussière » dans le corps

## Plan (comment elle est fabriquée)
- Page squelette de référence : chrome standard du site (head, nav hamburger, CTA SMS collant, footer, CSS externes)
- Sections du corps : encart prix 66 € tout compris, détail de ce qui est inclus, « pourquoi certains sont moins chers », exemple 60 m² = 3 960 €, FAQ, CTA SMS
- Déploiement : commit sur GitHub (repo frafra92/poncage-parquet)

## Revue (état au 2026-10-20)
- [x] Schema.org valide (0 erreur JSON-LD)
- [x] 66 € TTC/m² visible sans scroller
- [x] Aucune affirmation « sans poussière » dans le corps
- [x] Liens internes valides (7 pages sœurs)
- [ ] CSS externe uniquement — **exception connue** : cette page contient encore du style inline (héritage, à migrer plus tard)
- [x] sitemap.xml + llms.txt à jour
- [x] miroir .md de la page créé (prix-poncage-parquet-paris.md)
