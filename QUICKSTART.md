# 🚀 Guide de Démarrage Rapide - Pokémon Predictor

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Git (optionnel)
- Docker & Docker Compose (optionnel, pour déploiement conteneurisé)

---

## ⚡ Démarrage Rapide (5 minutes)

### Étape 1: Cloner ou accéder au projet

```bash
cd ML-M2
```

### Étape 2: Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3: Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 4: Configurer l'environnement

```bash
# Copier le fichier example
cp .env.example .env

# Adapter .env selon vos besoins
# Les valeurs par défaut fonctionnent pour développement
```

### Étape 5: Lancer l'API

```bash
python main.py
```

**Sortie**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     ✅ Modèle chargé: modele/modele_pokemon.mod
```

### Étape 6: Tester l'API

**Documentation interactive**:
- 🌐 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc

**Première prédiction** (bash):
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "hp": 100,
    "attack": 120,
    "defense": 80,
    "sp_defense": 80,
    "speed": 95,
    "type_1": 1,
    "legendary": 0
  }'
```

**Réponse attendue**:
```json
{
  "victory_rate": 0.756,
  "victory_percentage": "75.6%",
  "recommendation": "FORT - Bon choix ⭐⭐",
  "confidence": "HAUTE (>85% ou <15%)",
  "pokemon_type": "Feu",
  "timestamp": "2026-04-17T10:30:45.123456"
}
```

---

## 🐳 Déploiement avec Docker

### Option 1: Docker Compose (Recommandée)

```bash
# Démarrer
docker-compose up -d

# Vérifier l'état
docker-compose ps

# Logs
docker-compose logs -f api

# Arrêter
docker-compose down
```

### Option 2: Docker manuelle

```bash
# Build image
docker build -t pokemon-api .

# Run
docker run -p 8000:8000 \
  -v $(pwd)/modele:/app/modele \
  -e ENVIRONMENT=production \
  pokemon-api

# ou avec docker run interactif
docker run -it -p 8000:8000 pokemon-api
```

---

## 📂 Structure du Projet

```
ML-M2/
│
├── 📄 README.md                      # 📖 Documentation complète du projet
├── 📄 DEPLOYMENT_GUIDE.md            # 🚀 Guide de déploiement détaillé
├── 📄 API_SPECIFICATION.md           # 📋 Spec technique de l'API
├── 📄 QUICKSTART.md                  # ⚡ Ce fichier
│
├── 📁 data/                          # 📊 Données
│   ├── pokedex.csv                   # Base Pokémon
│   ├── combats.csv                   # Historique batailles
│   ├── dataset.csv                   # Dataset fusionné
│   └── note.ipynb                    # Notebook pipeline complet
│
├── 📁 modele/                        # 🤖 Modèles entraînés
│   └── modele_pokemon.mod            # Random Forest (serialisé)
│
├── 📁 logs/                          # 📝 Logs d'exécution
│
├── 🔧 main.py                        # 🚀 API FastAPI principale
├── 📄 requirements.txt                # 📦 Dépendances Python
├── 📄 .env.example                   # ⚙️ Exemple configuration
├── 📄 Dockerfile                     # 🐳 Configuration Docker
├── 📄 docker-compose.yml             # 🐳 Docker Compose
│
└── 📁 .git/                          # Git repository
```

---

## 🔗 Accès aux Resources

### URLs Locales (Développement)

| Resource | URL |
|----------|-----|
| **API** | http://localhost:8000 |
| **Documentation Swagger** | http://localhost:8000/docs |
| **Documentation ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |
| **Types Pokémon** | http://localhost:8000/types |

### API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Info service |
| `GET` | `/health` | État du service |
| `POST` | `/predict` | Prédiction simple |
| `POST` | `/batch-predict` | Prédictions batch |
| `GET` | `/types` | Mapping types |
| `GET` | `/status` | Statut détaillé |

---

## 📚 Exemples d'Utilisation

### Python

```python
import requests

api = "http://localhost:8000"

# Prédiction
response = requests.post(f"{api}/predict", json={
    "hp": 100,
    "attack": 120,
    "defense": 80,
    "sp_defense": 80,
    "speed": 95,
    "type_1": 1,
    "legendary": 0
})

result = response.json()
print(f"Taux: {result['victory_percentage']}")
print(f"Recommandation: {result['recommendation']}")
```

### JavaScript/Node.js

```javascript
const api = "http://localhost:8000";

const pokemon = {
  hp: 100,
  attack: 120,
  defense: 80,
  sp_defense: 80,
  speed: 95,
  type_1: 1,
  legendary: 0
};

fetch(`${api}/predict`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(pokemon)
})
.then(r => r.json())
.then(d => console.log(`${d.victory_percentage} - ${d.recommendation}`));
```

### Bash/cURL

```bash
# Simple
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"hp":100,"attack":120,"defense":80,"sp_defense":80,"speed":95,"type_1":1,"legendary":0}'

# Avec API Key (si activée)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"hp":100,"attack":120,"defense":80,"sp_defense":80,"speed":95,"type_1":1,"legendary":0}'

# Batch prediction
curl -X POST "http://localhost:8000/batch-predict" \
  -H "Content-Type: application/json" \
  -d '[
    {"hp":100,"attack":120,"defense":80,"sp_defense":80,"speed":95,"type_1":1,"legendary":0},
    {"hp":80,"attack":100,"defense":90,"sp_defense":70,"speed":110,"type_1":4,"legendary":0}
  ]'
```

---

## 🔧 Troubleshooting

### Problem: "Modèle non trouvé"

```
Erreur: Modèle non trouvé: modele/modele_pokemon.mod
```

**Solution**:
```bash
# Vérifier que le fichier existe
ls modele/modele_pokemon.mod

# Ou exécuter le notebook pour entraîner
python -m jupyter notebook data/note.ipynb
```

### Problem: Port 8000 déjà utilisé

```
ERROR: Address already in use
```

**Solution**:
```bash
# Utiliser autre port
python main.py --port 8001

# Ou tuer le processus
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Problem: Erreur dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Réinstaller dépendances
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Types Pokémon (Référence)

```
0  = Normal      9  = Eau
1  = Feu        10  = Électrique
2  = Herbe      11  = Glace
3  = Poison     12  = Combat
4  = Vol        13  = Psy
5  = Insecte    14  = Roche
6  = Sol        15  = Spectre
7  = Roche      16  = Dragon
8  = Acier      17  = Fée
```

---

## 📖 Documentation Complète

Pour plus de détails:
- **Pipeline IA**: Voir [README.md](README.md)
- **Déploiement avancé**: Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Spec API complète**: Voir [API_SPECIFICATION.md](API_SPECIFICATION.md)

---

## 🔒 Sécurité

### En Développement
- `DEBUG=True` (ne pas utiliser en production)
- Pas d'authentification requise

### En Production
Voir [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#-sécurité) pour:
- Activation API Key
- Configuration CORS
- SSL/HTTPS
- Rate Limiting

---

## 📈 Monitoring

### Logs en temps réel

```bash
# Avec docker-compose
docker-compose logs -f api

# Fichier log
tail -f logs/api.log
```

### Health Check

```bash
# Simple
curl http://localhost:8000/health

# Status complet
curl http://localhost:8000/status
```

---

## 🎯 Prochaines Étapes

- [ ] Exécuter le notebook pour générer/actualiser le modèle
- [ ] Configurer la sécurité (API Keys, CORS)
- [ ] Déployer sur serveur cloud
- [ ] Mettre en place monitoring/alertes
- [ ] Créer interface frontend
- [ ] Intégrer avec base de données

---

## 📞 Support

- 📖 Documentation: `/docs` (Swagger UI)
- 🔧 Issues: Check logs in `logs/api.log`
- 💬 Questions: Voir [README.md](README.md)

---

**Statut**: ✅ Ready to Deploy
**Version**: 1.0.0
**Dernière mise à jour**: 2026-04-17

Happy coding! 🎉
