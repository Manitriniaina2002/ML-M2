"""
Pokémon Battle Victory Predictor API
Endpoint pour la prédiction du taux de victoire Pokémon

Framework: FastAPI
Model: Random Forest Regressor
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import joblib
import numpy as np
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
MODEL_PATH = os.getenv("MODEL_PATH", "modele/modele_pokemon.mod")
API_KEY_ENABLED = os.getenv("API_KEY_ENABLED", "False").lower() == "true"
API_KEY = os.getenv("API_KEY", "")

POKEMON_TYPES = {
    0: "Normal",      9: "Eau",
    1: "Feu",        10: "Électrique",
    2: "Herbe",      11: "Glace",
    3: "Poison",     12: "Combat",
    4: "Vol",        13: "Psy",
    5: "Insecte",    14: "Roche",
    6: "Sol",        15: "Spectre",
    7: "Roche",      16: "Dragon",
    8: "Acier",      17: "Fée"
}

# ============================================================================
# LOAD MODEL
# ============================================================================

try:
    if not os.path.exists(MODEL_PATH):
        logger.warning(f"Modèle non trouvé: {MODEL_PATH}")
        modele = None
    else:
        modele = joblib.load(MODEL_PATH)
        logger.info(f"✅ Modèle chargé: {MODEL_PATH}")
except Exception as e:
    logger.error(f"❌ Erreur chargement modèle: {str(e)}")
    modele = None

# ============================================================================
# INITIALIZE APP
# ============================================================================

app = FastAPI(
    title=os.getenv("API_TITLE", "Pokémon Battle Predictor"),
    description=os.getenv("API_DESCRIPTION", "Prédiction du taux de victoire"),
    version=os.getenv("API_VERSION", "1.0.0"),
    docs_url="/docs" if os.getenv("ENABLE_SWAGGER_UI", "True") == "True" else None,
    redoc_url="/redoc" if os.getenv("ENABLE_REDOC", "True") == "True" else None,
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "['http://localhost:3000']")
app.add_middleware(
    CORSMiddleware,
    allow_origins=eval(origins) if isinstance(origins, str) else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class PokemonStats(BaseModel):
    """Statistiques d'un Pokémon pour prédiction"""
    hp: int = Field(..., ge=20, le=200, description="Points de vie (20-200)")
    attack: int = Field(..., ge=20, le=200, description="Niveau d'attaque (20-200)")
    defense: int = Field(..., ge=20, le=200, description="Niveau de défense (20-200)")
    sp_defense: int = Field(..., ge=20, le=200, description="Défense spéciale (20-200)")
    speed: int = Field(..., ge=20, le=200, description="Vitesse (20-200)")
    type_1: int = Field(..., ge=0, le=17, description="Type primaire (0-17)")
    legendary: int = Field(default=0, ge=0, le=1, description="Statut légendaire (0=non, 1=oui)")

    @validator('type_1')
    def validate_type(cls, v):
        if v not in POKEMON_TYPES:
            raise ValueError(f"Type invalide. Types acceptés: 0-17")
        return v

    class Config:
        schema_extra = {
            "example": {
                "hp": 100,
                "attack": 120,
                "defense": 80,
                "sp_defense": 80,
                "speed": 95,
                "type_1": 1,
                "legendary": 0
            }
        }

class PredictionResponse(BaseModel):
    """Réponse de prédiction"""
    victory_rate: float = Field(..., description="Taux de victoire (0.0-1.0)")
    victory_percentage: str = Field(..., description="Pourcentage formaté")
    recommendation: str = Field(..., description="Recommandation pour le dresseur")
    confidence: str = Field(..., description="Confiance du modèle")
    pokemon_type: Optional[str] = Field(None, description="Type du Pokémon")
    timestamp: str = Field(..., description="Timestamp de la prédiction")

class HealthResponse(BaseModel):
    """Réponse health check"""
    status: str
    model_loaded: bool
    environment: str
    timestamp: str

class ErrorResponse(BaseModel):
    """Réponse d'erreur"""
    error: str
    detail: Optional[str] = None
    status_code: int

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_recommendation(victory_rate: float) -> str:
    """Convertir taux victoire en recommandation"""
    if victory_rate >= 0.8:
        return "TRÈS FORT - Recommandé ⭐⭐⭐"
    elif victory_rate >= 0.7:
        return "FORT - Bon choix ⭐⭐"
    elif victory_rate >= 0.5:
        return "MOYEN - À considérer ⭐"
    else:
        return "FAIBLE - À éviter ❌"

def get_confidence(victory_rate: float) -> str:
    """Évaluer la confiance du modèle"""
    if victory_rate > 0.95 or victory_rate < 0.05:
        return "TRÈS HAUTE (>95% ou <5%)"
    elif victory_rate > 0.85 or victory_rate < 0.15:
        return "HAUTE (>85% ou <15%)"
    else:
        return "MOYENNE (15%-85%)"

def verify_api_key(x_token: str = Header(None)) -> str:
    """Vérifier l'API Key si activée"""
    if not API_KEY_ENABLED:
        return "no-key"
    
    if x_token is None:
        raise HTTPException(status_code=403, detail="API Key manquante")
    
    if x_token != API_KEY:
        raise HTTPException(status_code=403, detail="API Key invalide")
    
    return x_token

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """Endpoint racine - Information sur le service"""
    return {
        "service": "Pokémon Battle Predictor",
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": ENVIRONMENT,
        "status": "online",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "batch_predict": "/batch-predict (POST)",
            "documentation": "/docs"
        },
        "model_loaded": modele is not None
    }

@app.get("/health", response_model=HealthResponse, tags=["Info"])
async def health_check():
    """Vérifier l'état du service"""
    return HealthResponse(
        status="healthy",
        model_loaded=modele is not None,
        environment=ENVIRONMENT,
        timestamp=datetime.now().isoformat()
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_victory_rate(
    pokemon: PokemonStats,
    api_key: str = Depends(verify_api_key)
):
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
    if modele is None:
        raise HTTPException(
            status_code=503,
            detail="Modèle non disponible. Erreur serveur."
        )
    
    try:
        logger.info(f"Prédiction reçue: HP={pokemon.hp}, ATK={pokemon.attack}")
        
        # Préparer les données [HP, ATK, DEF, SP_DEF, SPD, TYPE, LEGENDARY]
        features = np.array([[
            pokemon.hp,
            pokemon.attack,
            pokemon.defense,
            pokemon.sp_defense,
            pokemon.speed,
            pokemon.type_1,
            pokemon.legendary
        ]])
        
        # Faire la prédiction
        prediction = float(modele.predict(features)[0])
        
        # Limiter entre 0 et 1
        victory_rate = max(0.0, min(1.0, prediction))
        
        # Générer recommandation et confiance
        recommendation = get_recommendation(victory_rate)
        confidence = get_confidence(victory_rate)
        pokemon_type = POKEMON_TYPES.get(pokemon.type_1, "Unknown")
        
        logger.info(f"Prédiction réussie: {victory_rate:.1%}")
        
        return PredictionResponse(
            victory_rate=round(victory_rate, 3),
            victory_percentage=f"{victory_rate*100:.1f}%",
            recommendation=recommendation,
            confidence=confidence,
            pokemon_type=pokemon_type,
            timestamp=datetime.now().isoformat()
        )
        
    except ValueError as e:
        logger.error(f"Erreur validation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erreur validation: {str(e)}")
    except Exception as e:
        logger.error(f"Erreur prédiction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.post("/batch-predict", tags=["Prediction"])
async def batch_predict(
    pokemons: List[PokemonStats],
    api_key: str = Depends(verify_api_key)
):
    """
    Prédictions en batch pour plusieurs Pokémon
    
    **Limite**: Max 100 Pokémon par requête
    """
    max_batch = int(os.getenv("MAX_BATCH_SIZE", "100"))
    
    if len(pokemons) > max_batch:
        raise HTTPException(
            status_code=400,
            detail=f"Trop de Pokémon. Max: {max_batch}"
        )
    
    if modele is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    results = []
    errors = []
    
    for i, pokemon in enumerate(pokemons):
        try:
            features = np.array([[
                pokemon.hp,
                pokemon.attack,
                pokemon.defense,
                pokemon.sp_defense,
                pokemon.speed,
                pokemon.type_1,
                pokemon.legendary
            ]])
            
            prediction = float(modele.predict(features)[0])
            victory_rate = max(0.0, min(1.0, prediction))
            
            result = {
                "index": i,
                "victory_rate": round(victory_rate, 3),
                "victory_percentage": f"{victory_rate*100:.1f}%",
                "recommendation": get_recommendation(victory_rate),
                "confidence": get_confidence(victory_rate)
            }
            results.append(result)
            
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    
    return {
        "predictions": results,
        "errors": errors,
        "count_success": len(results),
        "count_errors": len(errors),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/types", tags=["Info"])
async def get_pokemon_types():
    """Obtenir le mapping des types Pokémon"""
    return {
        "types": POKEMON_TYPES,
        "count": len(POKEMON_TYPES)
    }

@app.get("/status", tags=["Info"])
async def get_status():
    """Obtenir le statut détaillé du service"""
    return {
        "service": "Pokémon Battle Predictor",
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": ENVIRONMENT,
        "model_loaded": modele is not None,
        "model_path": MODEL_PATH,
        "debug_mode": DEBUG,
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": "N/A"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Gestionnaire d'erreurs global"""
    logger.error(f"Erreur non traitée: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if DEBUG else "Une erreur s'est produite",
            "status_code": 500
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestionnaire d'erreurs HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Événement au démarrage"""
    logger.info(f"🚀 Application démarrée - Environnement: {ENVIRONMENT}")
    if modele is None:
        logger.warning("⚠️  Modèle non disponible")
    else:
        logger.info("✅ Modèle prêt pour prédictions")

@app.on_event("shutdown")
async def shutdown_event():
    """Événement à l'arrêt"""
    logger.info("🛑 Application arrêtée")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    
    logger.info(f"Démarrage du serveur: {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
