# 🎯 Fiche Technique API - Pokémon Predictor

## 📌 Informations Générales

| Propriété | Valeur |
|-----------|--------|
| **Service** | Pokémon Battle Victory Predictor |
| **Version** | 1.0.0 |
| **Type** | Régression (Prédiction de taux) |
| **Modèle** | Random Forest Regressor |
| **Framework** | FastAPI / Uvicorn |
| **Format Entrée** | JSON |
| **Format Sortie** | JSON |
| **Authentification** | API Key (optionnel) |

---

## 🔌 Endpoints

### 1. Health Check
```
GET /health
```
**Description**: Vérifier l'état du service

**Réponse**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-04-17"
}
```

---

### 2. Prédiction Simple
```
POST /predict
```

**Description**: Obtenir le taux de victoire d'un Pokémon

**Body (JSON)**:
```json
{
  "hp": 100,
  "attack": 120,
  "defense": 80,
  "sp_defense": 80,
  "speed": 95,
  "type_1": 1,
  "legendary": 0
}
```

**Paramètres**:
| Champ | Type | Range | Description |
|-------|------|-------|-------------|
| `hp` | int | 20-200 | Points de vie |
| `attack` | int | 20-200 | Niveau d'attaque |
| `defense` | int | 20-200 | Niveau de défense |
| `sp_defense` | int | 20-200 | Défense spéciale |
| `speed` | int | 20-200 | Vitesse |
| `type_1` | int | 0-17 | Type primaire (0=Normal, 1=Feu, etc.) |
| `legendary` | int | 0 ou 1 | Statut légendaire |

**Réponse (200 OK)**:
```json
{
  "victory_rate": 0.756,
  "victory_percentage": "75.6%",
  "recommendation": "FORT - Bon choix ⭐⭐",
  "confidence": "HAUTE"
}
```

**Codes erreur**:
- `400 Bad Request` - Paramètres invalides
- `422 Unprocessable Entity` - Validation échouée
- `500 Internal Server Error` - Erreur serveur

---

### 3. Prédictions Batch
```
POST /batch-predict
```

**Description**: Prédictions pour plusieurs Pokémon simultanément

**Body (JSON)**:
```json
[
  {
    "hp": 100,
    "attack": 120,
    "defense": 80,
    "sp_defense": 80,
    "speed": 95,
    "type_1": 1,
    "legendary": 0
  },
  {
    "hp": 80,
    "attack": 100,
    "defense": 90,
    "sp_defense": 70,
    "speed": 110,
    "type_1": 4,
    "legendary": 0
  }
]
```

**Réponse (200 OK)**:
```json
{
  "predictions": [
    {
      "victory_rate": 0.756,
      "victory_percentage": "75.6%",
      "recommendation": "FORT - Bon choix ⭐⭐",
      "confidence": "HAUTE"
    },
    {
      "victory_rate": 0.682,
      "victory_percentage": "68.2%",
      "recommendation": "MOYEN - À considérer ⭐",
      "confidence": "MOYENNE"
    }
  ],
  "count": 2
}
```

---

### 4. Documentation Interactive
```
GET /docs
GET /redoc
```

**Description**: Accès à la documentation Swagger/ReDoc

---

## 📊 Types Pokémon (Mapping)

```
0 = Normal       9 = Eau          
1 = Feu         10 = Électrique   
2 = Herbe       11 = Glace        
3 = Poison      12 = Combat       
4 = Vol         13 = Psy          
5 = Insecte     14 = Roche        
6 = Sol         15 = Spectre      
7 = Roche       16 = Dragon       
8 = Acier       17 = Fée          
```

---

## 🎯 Grille d'Interprétation

### Taux de Victoire

| Taux | Niveau | Emoji | Interprétation |
|------|--------|-------|---|
| ≥ 0.80 | **TRÈS FORT** | ⭐⭐⭐ | Fortement recommandé |
| 0.70-0.79 | **FORT** | ⭐⭐ | Bon choix de combat |
| 0.50-0.69 | **MOYEN** | ⭐ | À considérer |
| < 0.50 | **FAIBLE** | ❌ | À éviter |

### Confiance du Modèle

| Confiance | Condition |
|-----------|-----------|
| **TRÈS HAUTE** | Taux > 0.95 ou < 0.05 |
| **HAUTE** | Taux > 0.85 ou < 0.15 |
| **MOYENNE** | Entre 0.15 et 0.85 |

---

## 🚀 Déploiement URL

### Développement
```
http://localhost:8000
```

### Staging
```
https://pokemon-api-staging.example.com
```

### Production
```
https://api.pokemon-predictor.com
```

---

## 💻 Exemples d'Appels

### cURL
```bash
# Prédiction simple
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"hp":100,"attack":120,"defense":80,"sp_defense":80,"speed":95,"type_1":1,"legendary":0}'

# Avec API Key
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"hp":100,"attack":120,"defense":80,"sp_defense":80,"speed":95,"type_1":1,"legendary":0}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "hp": 100,
        "attack": 120,
        "defense": 80,
        "sp_defense": 80,
        "speed": 95,
        "type_1": 1,
        "legendary": 0
    }
)

print(response.json())
```

### JavaScript
```javascript
const payload = {
  hp: 100,
  attack: 120,
  defense: 80,
  sp_defense: 80,
  speed: 95,
  type_1: 1,
  legendary: 0
};

fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📈 Performances

| Métrique | Valeur |
|----------|--------|
| **Temps réponse** | ~50-100ms |
| **Throughput** | ~100 req/sec (single worker) |
| **Modèle size** | ~50MB |
| **Mémoire RAM** | ~300MB minimum |
| **Processeur** | 1 CPU minimum |

---

## 🔒 Sécurité

### Headers de Sécurité
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

### CORS
```
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, X-API-Key
```

### Rate Limiting
```
10 requêtes / minute (par IP)
1000 requêtes / heure (par API Key)
```

---

## 📋 Logs & Monitoring

### Format Log
```json
{
  "timestamp": "2026-04-17T10:30:45Z",
  "level": "INFO",
  "endpoint": "/predict",
  "status": 200,
  "response_time_ms": 75,
  "model_confidence": 0.85
}
```

### Métriques Disponibles (Prometheus)
- `predictions_total` - Nombre total de prédictions
- `prediction_duration_seconds` - Temps de réponse
- `model_errors_total` - Erreurs du modèle
- `api_requests_total` - Total requêtes API

---

## 🔄 Versioning

### Version Actuelle: 1.0.0

**Format**: `X.Y.Z`
- **X** (Majeure): Changements incompatibles
- **Y** (Mineure): Nouvelles features compatibles
- **Z** (Patch): Corrections de bugs

**Exemple**:
```
GET /v1/predict  # Version 1
GET /v2/predict  # Future version 2
```

---

## 📞 Support & Contact

- **Documentation**: http://localhost:8000/docs
- **Issues**: GitHub Repository
- **Email Support**: support@pokemon-predictor.com
- **Status Page**: status.pokemon-predictor.com

---

## ✅ SLA (Service Level Agreement)

| Métrique | Cible |
|----------|-------|
| **Uptime** | 99.9% |
| **Response Time p95** | < 200ms |
| **Response Time p99** | < 500ms |
| **Error Rate** | < 0.1% |

---

**Dernière mise à jour**: 2026-04-17
**Statut**: Production Ready ✅
