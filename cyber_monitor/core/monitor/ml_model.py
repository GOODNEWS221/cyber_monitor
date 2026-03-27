import pandas as pd
from sklearn.ensemble import IsolationForest
from .models import NetworkLog, Company 
import joblib
import os

MODEL_DIR = "ml_models"
os. makedirs(MODEL_DIR, exist_ok=True) # Ensure folder exists

def get_model_path(company_id):
    return os.path.join(MODEL_DIR, f"model_company_{company_id}.pkl")


def train_model(company):
    """
    Train IsolationForest for a specific company.
    """
    logs = NetworkLog.objects.filter(company=company).values('packet_size')

    df = pd.DataFrame(logs)
    if df.empty:
        return None
    
    features = df[['packet_size']]

    model = IsolationForest(contamination=0.05)
    model.fit(features)

    joblib.dumo(model, get_model_path(company.id))
    return model 

def load_model(company):
    """
    Load trained model for a specific company.
    """

    path = get_model_path(company.id)
    if os.path.exists(path):
        return joblib.load(path)
    return None

def detect(packet_size, model):
    """
    Detect anomaly using provided model.
    """

    if not model:
        return False
    
    result = model.predict([[packet_size]])
    return result[0] == -1


 