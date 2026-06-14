import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class WagonFailurePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        self._train_model()

    def _generate_synthetic_data(self, n_samples=2000):
        np.random.seed(42)
        
        # Features
        wagon_age = np.random.uniform(1, 40, n_samples)
        load_weight = np.random.uniform(10, 120, n_samples)
        days_since_service = np.random.uniform(0, 500, n_samples)
        
        # Labels: Failure happens mostly when old AND heavy AND not serviced recently
        # We define a hidden risk score
        risk_score = (wagon_age / 40.0) * 0.4 + (load_weight / 120.0) * 0.3 + (days_since_service / 500.0) * 0.3
        
        # Add some non-linear threshold and noise
        probability = 1 / (1 + np.exp(-10 * (risk_score - 0.6)))
        
        labels = np.random.binomial(1, probability)
        
        df = pd.DataFrame({
            'wagon_age_years': wagon_age,
            'load_weight_tons': load_weight,
            'days_since_service': days_since_service,
            'failure': labels
        })
        return df

    def _train_model(self):
        df = self._generate_synthetic_data()
        X = df[['wagon_age_years', 'load_weight_tons', 'days_since_service']]
        y = df['failure']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        print("\n--- ML Model (Wagon Failure Prediction) Trained ---")
        print(classification_report(y_test, y_pred))
        print("---------------------------------------------------\n")
        
    def predict_failure_probability(self, wagon_age, load_weight, days_since_service):
        X_new = pd.DataFrame({
            'wagon_age_years': [wagon_age],
            'load_weight_tons': [load_weight],
            'days_since_service': [days_since_service]
        })
        prob = self.model.predict_proba(X_new)[0][1] # Probability of class 1 (failure)
        return round(prob * 100, 2) # Return as percentage

# Singleton instance
ml_predictor = WagonFailurePredictor()
