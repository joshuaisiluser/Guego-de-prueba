"""Clasificador Iris con un modelo ya entrenado guardado como mimodelo.pkl.

Implementación para Streamlit Community Cloud. No vuelve a entrenar el modelo.
"""

from pathlib import Path
import re
import unicodedata

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Iris | Clasificador de flores",
    page_icon="🌸",
    layout="centered",
)

MODEL_PATH = Path(__file__).resolve().parent / "mimodelo.pkl"

# Orden estándar de las cuatro características del dataset Iris.
FEATURES = (
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
)

IRIS_NAMES = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}


def normalize_name(value):
    """Normaliza nombres como SepalLengthCm o 'sepal length (cm)'."""
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", value.lower())


def identify_iris_feature(name):
    """Identifica una característica Iris independientemente de su estilo de nombre."""
    normalized = normalize_name(name)

    if "sepal" in normalized or "sepalo" in normalized:
        part = "sepal"
    elif "petal" in normalized or "petalo" in normalized:
        part = "petal"
    else:
        return None

    if "length" in normalized or "longitud" in normalized or "largo" in normalized:
        measure = "length"
    elif "width" in normalized or "ancho" in normalized or "anchura" in normalized:
        measure = "width"
    else:
        return None

    return f"{part}_{measure}"


@st.cache_resource(show_spinner="Cargando el modelo de Machine Learning...")
def load_model():
    """Carga el archivo entrenado del repositorio (únicamente si es confiable)."""
    return joblib.load(MODEL_PATH)


def build_input(model, measures):
    """Ajusta el orden y tipo de entrada a lo empleado durante el entrenamiento.

    Si el estimador fue entrenado con pandas y conserva feature_names_in_,
    utiliza esos nombres y su orden real. En caso contrario, utiliza el orden
    clásico de Iris con un array de NumPy.
    """
    expected_count = getattr(model, "n_features_in_", None)
    if expected_count is not None and expected_count != 4:
        raise ValueError(
            f"El modelo espera {expected_count} atributos, pero Iris necesita 4. "
            "Revisa cómo entrenaste y guardaste mimodelo.pkl."
        )

    columns = getattr(model, "feature_names_in_", None)
    if columns is None:
        return np.array([[measures[f] for f in FEATURES]], dtype=float), None

    columns = [str(col) for col in columns]
    if len(columns) != 4:
        raise ValueError(f"El modelo espera {len(columns)} columnas en lugar de 4.")

    recognized = [identify_iris_feature(name) for name in columns]
    if None not in recognized and set(recognized) == set(FEATURES):
        data = {col: measures[key] for col, key in zip(columns, recognized)}
        return pd.DataFrame([data], columns=columns), None

    # Algunos notebooks crean nombres genéricos; si se usan, explicitar
    # la suposición y evitar presentarla como una correspondencia confirmada.
