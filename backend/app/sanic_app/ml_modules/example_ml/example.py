import pandas as pd
from loguru import logger
import joblib

from backend.app.sanic_app.ml_modules import ML_AbstractModel


class ExampleML(ML_AbstractModel):

    def make_predictions(self, data: dict):
        new_data = self.load_data_csv()
        self.preprocessing(new_data)
        return self.predict(new_data)

    def preprocessing(self, new_data):
        preprocessor = self.load_preprocessor()
        preprocessor.transform(new_data)

    def predict(self, new_data):
        model = self.load_model()
        return model.predict(new_data)

    def load_model(self):
        model = joblib.load(self.model_path)
        return model

    def load_preprocessor(self):
        preprocessor = joblib.load(self.preprocessor_path)
        return preprocessor

    @staticmethod
    def load_data_json():
        new_data = pd.read_csv('backend/ml_models/synthetic_dataset.csv')
        logger.info(new_data.columns)

        return new_data

    @staticmethod
    def load_data_csv():
        new_data = pd.read_csv('backend/ml_models/synthetic_dataset.csv')
        logger.info(new_data.columns)

        return new_data

    @staticmethod
    def define_metrics():
        numerical_features = ['CreditScore', 'Age', 'Balance']
        categorical_features = ['Geography', 'Gender', 'NumOfProducts']
