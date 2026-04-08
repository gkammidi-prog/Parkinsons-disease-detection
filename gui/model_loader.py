"""
Model loading and prediction functions for Parkinson's Detection GUI
"""
import joblib
import numpy as np
import pandas as pd
import os
from .config import MODELS_DIR, DATA_DIR


class ModelLoader:
    """Handles loading and using the trained CatBoost model"""
    
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.is_loaded = False
        self.error_message = None
        self.optimal_threshold = 0.8  # Default threshold
    
    def load_model(self):
        """
        Load the trained CatBoost model and feature names
        """
        try:
            print("="*50)
            print("LOADING PARKINSON'S DETECTION MODEL")
            print("="*50)
            
            # Define paths - use CatBoost model
            model_path = os.path.join(MODELS_DIR, 'catboost_gui_model.joblib')
            features_path = os.path.join(DATA_DIR, 'selected_features.txt')
            
            # Fallback to other models if CatBoost not found
            if not os.path.exists(model_path):
                model_path = os.path.join(MODELS_DIR, 'production_model.joblib')
                if not os.path.exists(model_path):
                    model_path = os.path.join(MODELS_DIR, 'random_forest_baseline.joblib')
            
            if not os.path.exists(model_path):
                self.error_message = "Model file not found"
                print(self.error_message)
                return False
            
            self.model = joblib.load(model_path)
            print(f"✓ Model loaded: {os.path.basename(model_path)}")
            print(f"  Model type: {type(self.model).__name__}")
            
            # Load feature names
            if os.path.exists(features_path):
                with open(features_path, 'r') as f:
                    self.feature_names = [line.strip() for line in f.readlines()]
                print(f"✓ Loaded {len(self.feature_names)} features")
            else:
                self.error_message = "Features file not found"
                return False
            
            self.is_loaded = True
            print("="*50)
            return True
            
        except Exception as e:
            self.error_message = f"Error loading model: {str(e)}"
            print(self.error_message)
            import traceback
            traceback.print_exc()
            return False
    
    def predict_single(self, values):
        """
        Make a single prediction
        """
        if not self.is_loaded:
            raise Exception("Model not loaded")
        
        # Convert to numpy array
        input_array = np.array([float(v) for v in values]).reshape(1, -1)
        print(f"Input shape: {input_array.shape}")
        
        # Make prediction
        probability = self.model.predict_proba(input_array)[0][1]
        prediction = 1 if probability >= self.optimal_threshold else 0
        
        status = "Parkinson's" if prediction == 1 else "Healthy"
        print(f"Probability: {probability:.4f}, Prediction: {status}")
        
        return prediction, probability
    
    def predict_batch(self, data):
        """
        Make batch predictions from DataFrame
        """
        if not self.is_loaded:
            raise Exception("Model not loaded")
        
        # Extract features in correct order
        X = data[self.feature_names].values.astype(float)
        print(f"Batch input shape: {X.shape}")
        
        # Make predictions
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = (probabilities >= self.optimal_threshold).astype(int)
        
        return predictions, probabilities
    
    def get_feature_names(self):
        return self.feature_names
    
    def get_model_info(self):
        if not self.is_loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "features_count": len(self.feature_names) if self.feature_names else 0,
            "model_type": type(self.model).__name__,
            "features": self.feature_names[:5] if self.feature_names else [],
            "threshold": self.optimal_threshold
        }