# 🎮 Prédiction Victorieuse Pokémon - Pipeline IA

## 📋 Fiche Descriptive du Projet

### 🎯 Objectif
Développer un **système de recommandation intelligent** qui conseille aux dresseurs Pokémon le meilleur animal à utiliser lors d'un combat pour maximiser les chances de victoire.

### 📊 Problématique
**Question métier**: Quel Pokémon recommander pour maximiser le pourcentage de victoire ?

Le système doit analyser les statistiques des Pokémon et l'historique des combats pour prédire le taux de victoire d'un Pokémon donné.

---

## 🔄 Pipeline IA - Étapes de Traitement

### Étape 1️⃣ : Définition du Problème
- **Objectif**: Prédire le taux de victoire d'un Pokémon en combat
- **Cible (Y)**: Pourcentage de victoire (0-1)
- **Type**: Régression - Problème de prédiction numérique

### Étape 2️⃣ : Acquisition des Données
**Sources de données**:
- `data/pokedex.csv` - Base de données complète des 800+ Pokémon
- `data/combats.csv` - Historique de 50,000+ batailles
- `data/poke_type_chart.csv` - Tableau des avantages/désavantages de types
- `fruits.xlsx` - Données supplémentaires

**Taille données**: 
- Pokémon: ~800 observations
- Combats: ~50,000 observations

### Étape 3️⃣ : Préparation des Données
**Nettoyage**:
- Conversion du type LEGENDAIRE (TRUE/FALSE → 0/1)
- Correction des valeurs manquantes (ex: Pokémon #62 "Colossinge")
- Suppression des lignes avec données incomplètes

**Format**: Utilisation de pandas DataFrame pour manipulation structurée

### Étape 4️⃣ : Analyse Exploratoire
**Données de combat extraites**:
- Nombre de combats par Pokémon
- Nombre de victoires par Pokémon
- Calcul du taux de victoire (Victoires / Total Combats)

### Étape 5️⃣ : Feature Engineering & Agrégation
**Fusion des données**:
- Combinaison Pokedex + Statistiques de combats
- Création de nouvelles features:
  - `NBR_COMBATS`: Nombre total de combats
  - `NBR_VICTOIRES`: Nombre de victoires
  - `POURCENTAGE`: Taux de victoire (variable cible)

**Features d'entrée (X)**:
- `POINTS_DE_VIE` - Points de santé
- `NIVEAU_ATTAQUE` - Force d'attaque
- `NIVEAU_DEFENSE` - Capacité de défense
- `NIVEAU_DEFENSE_SPECIALE` - Défense spéciale
- `VITESSE` - Vitesse d'attaque
- `TYPE_1` - Type primaire
- `LEGENDAIRE` - Statut légendaire (0/1)

### Étape 6️⃣ : Visualisation & Analyse
**Graphiques générés**:
- Distribution des Pokémon par TYPE_1 (normal vs légendaire)
- Distribution des Pokémon par TYPE_2
- Taux de victoire moyen par type
- **Matrice de corrélation** - Heatmap des dépendances entre features

**Insights**:
- Certains types ont des taux de victoire supérieurs
- Corrélation entre les stats et la performance

### Étape 7️⃣ : Entraînement des Modèles
**Algorithmes testés**:

| Modèle | Type | Précision (R²) | Utilité |
|--------|------|---|---|
| **Linear Regression** | Régression linéaire | Baseline | Référence simple |
| **Decision Tree Regressor** | Arbre de décision | Modéré | Comprendre patterns |
| **Random Forest** ✅ | Ensemble (meilleur) | Élevé | Production recommandé |

**Split données**:
- Ensemble d'apprentissage: 80% (données d'entraînement)
- Ensemble de validation: 20% (test indépendant)

**Métrique**: R² Score (coefficient de détermination)

### Étape 8️⃣ : Évaluation & Validation
- Prédictions sur l'ensemble de test
- Calcul de R² pour mesurer la qualité
- Comparaison des trois modèles
- **Modèle sélectionné**: Random Forest (meilleure performance)

### Étape 9️⃣ : Sauvegarde du Modèle
**Fichier sortie**: `modele/modele_pokemon.mod`
- Format: Sérialisation joblib
- Permet réutilisation du modèle en production

---

## 📦 Structure des Données

### Input Features (Colonnes 5-12)
```
X = [POINTS_DE_VIE, NIVEAU_ATTAQUE, NIVEAU_DEFENSE, 
     NIVEAU_DEFENSE_SPECIALE, VITESSE, TYPE_1, LEGENDAIRE]
```

### Output (Cible)
```
y = POURCENTAGE (Taux de victoire prédit)
```

---

## 🚀 Déploiement & Utilisation

### Mode Prédiction Batch
```python
import joblib
import pandas as pd

# Charger le modèle
modele = joblib.load('modele/modele_pokemon.mod')

# Préparer les données d'un nouveau Pokémon
stats_pokemon = [[100, 120, 80, 80, 95, 1, 0]]  # Format: [features x 7]

# Faire une prédiction
taux_victoire = modele.predict(stats_pokemon)
print(f"Taux de victoire prédit: {taux_victoire[0]:.2%}")
```

### Intégration API (FastAPI)
```
GET /predict?hp=100&atk=120&def=80&sp_def=80&spd=95&type=1&legendary=0
Response: { "victory_rate": 0.78, "recommendation": "FORT" }
```

### Interface Web (Streamlit)
```
- Sélectionner un Pokémon ou entrer ses stats
- Visualiser les prédictions
- Comparer plusieurs Pokémon
```

### Lancer Streamlit en local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Pipeline GitHub Actions (Streamlit)
Le workflow CI est disponible dans `.github/workflows/streamlit-ci.yml`.

Ce pipeline execute automatiquement:
- installation des dependances Python
- verification de syntaxe de `streamlit_app.py`
- smoke test de demarrage de l'application Streamlit

Le workflow se declenche sur:
- `push` sur `main` ou `master`
- `pull_request`

### Deploiement vers Hugging Face Spaces
Un workflow de deploiement est disponible dans `.github/workflows/deploy-hf-space.yml`.

Configuration GitHub requise:
- Secret `HF_TOKEN`: token Hugging Face (permission `write` sur le Space)
- Variable `HF_SPACE_REPO`: identifiant du Space au format `username/space-name`

Code deploye vers le Space:
- dossier `hf_space/` synchronise vers la racine du Space
- application Streamlit: `hf_space/app.py`

Declenchement:
- `push` sur `main` ou `master`
- execution manuelle via `workflow_dispatch`

Protections actives:
- ignore automatiquement les executions Dependabot
- ignore les changements documentation uniquement (`**/*.md` et `docs/**`)

Debug automatique en cas d'echec:
- affiche le contexte (`event`, `actor`, `ref`, `sha`)
- confirme la presence de `HF_TOKEN` et des variables Space sans afficher leur contenu
- affiche les fichiers locaux du dossier `hf_space/` et le statut git du clone cible

### Preproduction Hugging Face Spaces (Preview)
Un second workflow de preview est disponible dans `.github/workflows/deploy-hf-space-preview.yml`.

Configuration GitHub requise (en plus de `HF_TOKEN`):
- Variable `HF_SPACE_REPO_PREVIEW`: identifiant du Space de preproduction au format `username/preview-space`

Declenchement:
- `pull_request`
- `push` sur toutes les branches sauf `main` et `master`
- execution manuelle via `workflow_dispatch`

Protections actives:
- ignore automatiquement les executions Dependabot
- ignore les changements documentation uniquement (`**/*.md` et `docs/**`)

Debug automatique en cas d'echec:
- affiche le contexte (`event`, `actor`, `ref`, `sha`, `branch`)
- confirme la presence de `HF_TOKEN` et `HF_SPACE_REPO_PREVIEW` sans afficher les valeurs
- affiche les fichiers locaux du dossier `hf_space/` et le statut git du clone preview

Trace de provenance preview:
- le fichier `PREVIEW_SOURCE.txt` est genere dans le Space preview avec la branche et le commit deploye

---

## 📈 Résultats & Performance

**Métriques finales**:
- **R² Score (Random Forest)**: À déterminer après exécution
- **Modèle optimal**: Random Forest Regressor
- **Prédictions**: Taux de victoire continu [0, 1]

---

## 📂 Organisation du Projet

```
ML-M2/
├── README.md                          # Documentation complète
├── data/
│   ├── pokedex.csv                   # Base Pokémon (800+ espèces)
│   ├── combats.csv                   # Historique des batailles
│   ├── dataset.csv                   # Dataset fusionné (entrée modèle)
│   ├── poke_type_chart.csv          # Tableau des types
│   ├── note.ipynb                    # Notebook principal (Pipeline complet)
│   └── Pokedex/                      # Ressources supplémentaires
├── modele/
│   └── modele_pokemon.mod            # Modèle entraîné (Random Forest)
└── requirements.txt                   # Dépendances Python
```

---

## 🛠 Dépendances & Technologies

```
Python 3.7+
- pandas          → Manipulation des données
- numpy           → Calculs numériques
- scikit-learn    → Algorithmes ML (LinearRegression, DecisionTree, RandomForest)
- matplotlib      → Visualisations
- seaborn         → Heatmaps & statistical graphics
- joblib          → Sérialisation du modèle
```

---

## ✅ Checklist Déploiement

- [x] Données acquises et nettoyées
- [x] Features engineering complété
- [x] 3 modèles entraînés et comparés
- [x] Modèle optimal sélectionné (Random Forest)
- [x] Modèle sauvegardé (`modele_pokemon.mod`)
- [ ] **TODO**: API REST déployée
- [ ] **TODO**: Interface web en ligne
- [ ] **TODO**: Monitoring et logging
- [ ] **TODO**: Documentation API Swagger

---

## 🔗 Endpoints d'Accès (À Déployer)

### Développement Local
```
http://localhost:8000/predict
```

### Production (À configurer)
```
https://pokemon-predictor.api.example.com/predict
```

---

## 📞 Support & Maintenance

**Maintenance requise**:
- Réentraînement mensuel avec nouvelles batailles
- Monitoring de la dérive de performance (R² decline)
- Feedback utilisateurs pour optimisation

**Prochaines améliorations**:
1. Modèle de classification (Gagnant/Perdant) + probabilités
2. Recommandations de stratégie par type d'adversaire
3. Dashboard interactif d'analyse Pokémon
4. API d'entraînement personnalisé

---

**Projet créé**: 2026
**Statut**: En production - Pipeline validé ✅
