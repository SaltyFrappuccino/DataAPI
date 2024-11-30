from dataclasses import dataclass

from backend.app.sanic_app.ml_modules import ML_AbstractModel


@dataclass
class ML_ModelSchema:
    ml_model: ML_AbstractModel
    preprocessor_path: str
    ml_model_path: str
