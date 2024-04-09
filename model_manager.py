import joblib
from tensorflow.keras.models import load_model

class ModelManager:
    def __init__(self):
        self.models = {}
        self.scalers = {}

    def normalize_test_data(self, scaler_name, test_df):
        scaler = self.scalers.get(scaler_name)
        if scaler is not None:
            test_df_norm = pd.DataFrame(scaler.transform(test_df), columns=test_df.columns)
            return test_df_norm
        else:
            raise ValueError(f"Scaler {scaler_name} not found.")

    def load_model(self, model_name, model_path):
        print(f"Loading {model_name}...")
        model = load_model(model_path)
        self.models[model_name] = model
        print(f"Done loading {model_name}.")

    def load_scaler(self, scaler_name, scaler_path):
        print(f"Loading {scaler_name}...")
        scaler = joblib.load(scaler_path)
        self.scalers[scaler_name] = scaler
        print(f"Done loading {scaler_name}.")

    def get_model(self, model_name):
        if model_name in self.models:
            return self.models[model_name]
        else:
            raise ValueError(f"Model {model_name} not found.")

    def get_scaler(self, scaler_name):
        if scaler_name in self.scalers:
            return self.scalers[scaler_name]
        else:
            raise ValueError(f"Scaler {scaler_name} not found.")
