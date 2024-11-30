from abc import abstractmethod


class ML_AbstractModel:
    def __init__(self, model_path: str, preprocessor_path: str):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path

    @abstractmethod
    def make_predictions(self, data: dict):
        pass

    @abstractmethod
    def preprocessing(self, new_data):
        pass

    @abstractmethod
    def predict(self, new_data):
        pass

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def load_preprocessor(self):
        pass
