from backend.app.sanic_app.ml_modules.example_ml.example import ExampleML
from backend.app.sanic_app.ml_modules.schemas import ML_ModelSchema


class ML_Factory:

    @classmethod
    def create(cls, ml_model_name: str) -> ML_ModelSchema:
        ml_model = cls.define_ml_model(ml_model_name)
        preprocessor_path = cls.define_preprocessor_path(ml_model_name)
        ml_model_path = cls.define_ml_model_path(ml_model_name)
        return ML_ModelSchema(**{
            'ml_model': ml_model,
            'preprocessor_path': preprocessor_path,
            'ml_model_path': ml_model_path
        })

    @staticmethod
    def define_ml_model(ml_model_name: str):
        ml_models: dict = {
            'example': ExampleML
        }

        return ml_models[ml_model_name]

    @staticmethod
    def define_preprocessor_path(ml_model_name: str):
        define_preprocessors_path: dict = {
            'example': 'backend/ml_models/preprocessor.pkl'
        }

        return define_preprocessors_path[ml_model_name]

    @staticmethod
    def define_ml_model_path(ml_model_name: str):
        ml_models_path: dict = {
            'example': 'backend/ml_models/xgb_model.pkl'
        }

        return ml_models_path[ml_model_name]
