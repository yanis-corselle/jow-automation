# 🛒 Jow High-Protein Menu Generator & Butcher Splitter

Micro-service FastAPI hébergé sur Raspberry Pi permettant d'automatiser la sélection de menus hebdomadaires sur **Jow** selon des critères stricts de macronutriments (protéines), tout en isolant les achats de boucherie sur une liste séparée.

## 🚀 Fonctionnalités

- **Filtre Macronutriments :** Sélectionne uniquement les recettes avec un seuil minimal de protéines par portion (ex: >= 30g).
- **Sélection Aléatoire :** Tirage au sort de $N$ repas sans doublons pour éviter la redondance.
- **Séparation Boucherie :** Filtre automatiquement la viande/volaille via un fichier de mots-clés externe (`data/meat_keywords.json`) pour ne pas les inclure dans la commande Drive.
- **Sécurisé :** Accès protégé par authentification Bearer Token.

---

## 🛠️ Structure du Fichier de Mots-Clés

Les mots-clés utilisés pour identifier les articles de boucherie sont stockés dans `data/meat_keywords.json`. Vous pouvez modifier ce fichier à tout moment pour changer de langue ou ajouter des ingrédients :

```json
{
  "keywords": [
    "poulet",
    "boeuf",
    "dinde",
    "steak",
    "porc"
  ]
}
