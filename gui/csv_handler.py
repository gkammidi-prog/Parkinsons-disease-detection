"""
CSV file handling for batch predictions
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime


class CSVHandler:
    """Handles CSV file operations"""
    
    def __init__(self, expected_columns):
        self.expected_columns = expected_columns
    
    def load_csv(self, filepath):
        """
        Load and validate CSV file
        """
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            
            # Check if file is empty
            if df.empty:
                return None, "CSV file is empty"
            
            # Check for required columns
            missing_columns = [col for col in self.expected_columns if col not in df.columns]
            if missing_columns:
                return None, f"Missing required columns: {missing_columns}"
            
            # Check for empty values
            if df[self.expected_columns].isnull().any().any():
                return None, "CSV contains empty values. Please fill all required fields."
            
            return df, None
            
        except Exception as e:
            return None, f"Error reading CSV: {str(e)}"
    
    def validate_values(self, df):
        """
        Validate that all values are numeric
        """
        errors = []
        for col in self.expected_columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                errors.append(f"Column '{col}' contains non-numeric values")
        return errors
    
    def export_results(self, data, predictions, probabilities, output_path=None):
        """
        Export predictions to CSV
        """
        # Create results dataframe
        results = data.copy()
        results['Prediction'] = ['Parkinson\'s' if p == 1 else 'Healthy' for p in predictions]
        results['Probability_Parkinsons'] = probabilities
        results['Probability_Healthy'] = 1 - probabilities
        results['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Determine output path
        if output_path is None:
            output_path = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Save to CSV
        results.to_csv(output_path, index=False)
        
        return output_path