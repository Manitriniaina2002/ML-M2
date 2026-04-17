# 🚀 Guide de Déploiement - Pokémon Predictor API

## 📋 Vue d'ensemble

Ce guide explique comment déployer le modèle de prédiction Pokémon en tant qu'API REST pour permettre aux clients d'obtenir des prédictions en temps réel.

---

## 🎯 Architecture de Déploiement

```
┌─────────────────────────────────────────────────────┐
│                   CLIENT                            │
│            (Web App / Mobile / CLI)                 │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Request
                   ▼
┌─────────────────────────────────────────────────────┐
│        FastAPI / Flask Web Server                   │
│     (Pokemon Predictor Endpoint)                    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│      Modèle Entraîné (Random Forest)                │
│         modele_pokemon.mod                          │
│     - Prédictions du taux de victoire               │
│     - Recommandations stratégiques                  │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ Option 1 : API FastAPI (Recommandée)

### Installation

```bash
# Créer environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Installer dépendances
pip install fastapi uvicorn pandas numpy scikit-learn joblib pydantic
```

### Code API (`main.py`)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Optional

app = FastAPI(
    title="Pokémon Battle Predictor API",
    description="Prédiction du taux de victoire Pokémon basée sur les stats",
    version="1.0.0"
)

# Charger le modèle
try:
    modele = joblib.load('modele/modele_pokemon.mod')
except FileNotFoundError:
    raise Exception("Modèle non trouvé: modele/modele_pokemon.mod")

# Définir les schémas Pydantic
class PokemonStats(BaseModel):
    """Statistiques d'un Pokémon"""
    hp: int = 100  # Points de vie
    attack: int = 120  # Niveau d'attaque
    defense: int = 80  # Niveau de défense
    sp_defense: int = 80  # Défense spéciale
    speed: int = 95  # Vitesse
    type_1: int = 1  # Type primaire (encoded 0-17)
    legendary: int = 0  # Statut légendaire (0=non, 1=oui)

class PredictionResponse(BaseModel):
    """Réponse de prédiction"""
    victory_rate: float
    victory_percentage: str
    recommendation: str
    confidence: str

# Fonctions utilitaires
def get_recommendation(victory_rate: float) -> str:
    """Convertir taux victoire en recommandation"""
    if victory_rate >= 0.8:
        return "TRÈS FORT - Recommandé ⭐⭐⭐"
    elif victory_rate >= 0.7:
        return "FORT - Bon choix ⭐⭐"
    elif victory_rate >= 0.5:
        return "MOYEN - À considérer ⭐"
    else:
        return "FAIBLE - Éviter ❌"

def get_confidence(victory_rate: float) -> str:
    """Évaluer la confiance du modèle"""
    if victory_rate > 0.95 or victory_rate < 0.05:
        return "TRÈS HAUTE"
    elif victory_rate > 0.85 or victory_rate < 0.15:
        return "HAUTE"
    else:
        return "MOYENNE"

# Routes API

@app.get("/", tags=["Info"])
async def root():
    """Endpoint racine"""
    return {
        "service": "Pokémon Battle Predictor",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs (Swagger UI)"
        }
    }

@app.get("/health", tags=["Info"])
async def health_check():
    """Vérifier l'état du service"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "timestamp": "2026-04-17"
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_victory_rate(pokemon: PokemonStats):
    """
    Prédire le taux de victoire d'un Pokémon
    
    **Paramètres**:
    - hp: Points de vie (50-200)
    - attack: Niveau d'attaque (20-200)
    - defense: Niveau de défense (20-200)
    - sp_defense: Défense spéciale (20-200)
    - speed: Vitesse (20-200)
    - type_1: Type primaire (0-17)
    - legendary: Statut légendaire (0 ou 1)
    
    **Retour**: Taux de victoire prédit (0.0 à 1.0)
    """
    try:
        # Préparer les données
        features = np.array([
            [pokemon.hp, pokemon.attack, pokemon.defense,
             pokemon.sp_defense, pokemon.speed, pokemon.type_1,
             pokemon.legendary]
        ])
        
        # Faire la prédiction
        victory_rate = float(modele.predict(features)[0])
        
        # Limiter entre 0 et 1
        victory_rate = max(0.0, min(1.0, victory_rate))
        
        # Générer recommandation
        recommendation = get_recommendation(victory_rate)
        confidence = get_confidence(victory_rate)
        
        return PredictionResponse(
            victory_rate=round(victory_rate, 3),
            victory_percentage=f"{victory_rate*100:.1f}%",
            recommendation=recommendation,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur prédiction: {str(e)}")

@app.post("/batch-predict", tags=["Prediction"])
async def batch_predict(pokemons: list[PokemonStats]):
    """Prédictions en batch pour plusieurs Pokémon"""
    results = []
    for pokemon in pokemons:
        result = await predict_victory_rate(pokemon)
        results.append(result)
    return {"predictions": results, "count": len(results)}

@app.get("/compare", tags=["Analysis"])
async def compare_types():
    """Comparer les taux de victoire par type"""
    # Placeholder pour analyse comparative
    return {
        "message": "Endpoint de comparaison (à implémenter)"
    }

# Gestion des erreurs
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {
        "error": str(exc),
        "status": "error"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Lancer l'API

```bash
# Démarrage simple
python main.py

# Ou avec uvicorn directement
uvicorn main:app --reload --port 8000

# Production (sans reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Accéder à la documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Exemples d'utilisation

### cURL - Simple Prediction

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

**Réponse**:
```json
{
  "victory_rate": 0.756,
  "victory_percentage": "75.6%",
  "recommendation": "FORT - Bon choix ⭐⭐",
  "confidence": "HAUTE"
}
```

### Python Client

```python
import requests

API_URL = "http://localhost:8000"

# Prédiction simple
pokemon_stats = {
    "hp": 100,
    "attack": 120,
    "defense": 80,
    "sp_defense": 80,
    "speed": 95,
    "type_1": 1,
    "legendary": 0
}

response = requests.post(f"{API_URL}/predict", json=pokemon_stats)
prediction = response.json()

print(f"Taux de victoire: {prediction['victory_percentage']}")
print(f"Recommandation: {prediction['recommendation']}")
```

### JavaScript/Fetch

```javascript
const apiUrl = "http://localhost:8000";

const pokemonStats = {
  hp: 100,
  attack: 120,
  defense: 80,
  sp_defense: 80,
  speed: 95,
  type_1: 1,
  legendary: 0
};

fetch(`${apiUrl}/predict`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(pokemonStats)
})
.then(res => res.json())
.then(data => {
  console.log(`Victory Rate: ${data.victory_percentage}`);
  console.log(`Recommendation: ${data.recommendation}`);
});
```

---

## 🌐 Déploiement Cloud

### Option A: Heroku

```bash
# 1. Créer app
heroku create pokemon-predictor

# 2. Ajouter Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=${PORT}" > Procfile

# 3. Déployer
git push heroku main
```

**URL**: https://pokemon-predictor.herokuapp.com

### Option B: AWS Lambda + API Gateway

```bash
# Packager avec serverless framework
serverless deploy
```

**URL**: https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev

### Option C: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t pokemon-predictor .

# Run
docker run -p 8000:8000 pokemon-predictor

# Push à registry
docker push username/pokemon-predictor:latest
```

---

## 📊 Monitoring & Logging

### Ajouter Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/predict")
async def predict_victory_rate(pokemon: PokemonStats):
    logger.info(f"Prédiction reçue pour: {pokemon}")
    # ... rest of code
    logger.info(f"Résultat: {victory_rate}")
```

### Métriques (Prometheus)

```python
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_time = Histogram('prediction_duration_seconds', 'Prediction duration')

@prediction_time.time()
async def predict_victory_rate(pokemon: PokemonStats):
    prediction_counter.inc()
    # ...
```

---

## 🔐 Sécurité

### API Key

```python
from fastapi.security import APIKey, APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
async def predict_victory_rate(pokemon: PokemonStats, api_key: str = Depends(api_key_header)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ...
```

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Performance & Optimisation

| Aspect | Optimisation |
|--------|-------------|
| **Caching** | Redis pour cachage réponses |
| **Compression** | gzip pour réponses >1KB |
| **Async** | FastAPI utilise async natif |
| **Load Balancing** | NGINX/HAProxy pour multiple workers |
| **CDN** | CloudFlare pour assets statiques |

---

## ✅ Checklist Déploiement

- [ ] Modèle `modele_pokemon.mod` disponible
- [ ] API testée en local
- [ ] Documentation Swagger validée
- [ ] Tests unitaires passants
- [ ] Environment variables configurées
- [ ] CORS activé si nécessaire
- [ ] Logging et monitoring en place
- [ ] SSL/HTTPS configuré (production)
- [ ] Rate limiting activé
- [ ] Backup du modèle en place

---

## 📞 Endpoints de Référence

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Info service |
| `GET` | `/health` | Santé service |
| `POST` | `/predict` | Prédiction simple |
| `POST` | `/batch-predict` | Prédictions batch |
| `GET` | `/docs` | Documentation Swagger |
| `GET` | `/compare` | Comparaison types (TODO) |

---

**Statut**: Ready for Deployment ✅
**Version API**: 1.0.0
**Dernière mise à jour**: 2026-04-17
