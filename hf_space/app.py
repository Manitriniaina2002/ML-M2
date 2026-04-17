from pathlib import Path

import joblib
import numpy as np
import streamlit as st


TYPE_MAPPING = {
    0: "Normal",
    1: "Feu",
    2: "Herbe",
    3: "Poison",
    4: "Vol",
    5: "Insecte",
    6: "Sol",
    7: "Roche",
    8: "Acier",
    9: "Eau",
    10: "Electrique",
    11: "Glace",
    12: "Combat",
    13: "Psy",
    14: "Roche",
    15: "Spectre",
    16: "Dragon",
    17: "Fee",
}

MODEL_CANDIDATES = [
    Path("modele/modele_pokemon.mod"),
    Path("modele_pokemon.mod"),
]


def load_model():
    for candidate in MODEL_CANDIDATES:
        if candidate.exists():
            return joblib.load(candidate), str(candidate)
    return None, None


def clamp_rate(value: float) -> float:
    return max(0.0, min(1.0, value))


def recommendation(rate: float) -> str:
    if rate >= 0.80:
        return "Tres fort"
    if rate >= 0.70:
        return "Fort"
    if rate >= 0.50:
        return "Moyen"
    return "Faible"


def fallback_predict(features: np.ndarray) -> float:
    hp, atk, defense, sp_def, speed, _, legendary = features[0]
    score = (
        0.0018 * hp
        + 0.0032 * atk
        + 0.0024 * defense
        + 0.0020 * sp_def
        + 0.0022 * speed
        + 0.10 * legendary
    )
    return clamp_rate(float(score))


def main():
    st.set_page_config(page_title="Pokemon Predictor", page_icon=":crossed_swords:", layout="centered")

    st.title("Pokemon Battle Predictor")
    st.write("Predisez le taux de victoire d'un Pokemon a partir de ses statistiques.")

    model, model_path = load_model()
    if model is not None:
        st.success(f"Modele charge: {model_path}")
    else:
        st.warning("Aucun modele trouve. L'application utilise une estimation de secours.")

    col1, col2 = st.columns(2)

    with col1:
        hp = st.slider("Points de vie (HP)", 20, 200, 100)
        attack = st.slider("Attaque", 20, 200, 120)
        defense = st.slider("Defense", 20, 200, 80)
        sp_defense = st.slider("Defense speciale", 20, 200, 80)

    with col2:
        speed = st.slider("Vitesse", 20, 200, 95)
        type_id = st.selectbox("Type principal", options=list(TYPE_MAPPING.keys()), format_func=lambda x: TYPE_MAPPING[x])
        legendary = st.selectbox("Legendaire", options=[0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")

    features = np.array([[hp, attack, defense, sp_defense, speed, type_id, legendary]], dtype=float)

    if st.button("Predire", type="primary"):
        if model is not None:
            raw = float(model.predict(features)[0])
            rate = clamp_rate(raw)
        else:
            rate = fallback_predict(features)

        st.metric("Taux de victoire estime", f"{rate * 100:.1f}%")
        st.write(f"Niveau recommande: **{recommendation(rate)}**")
        st.progress(rate)


if __name__ == "__main__":
    main()
