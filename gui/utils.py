"""
Utility functions for the Parkinson's Detection GUI
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


def format_prediction(prediction, probability):
    """
    Format prediction result for display with enhanced styling
    """
    if prediction == 1:
        status = "⚠️ PARKINSON'S DISEASE DETECTED"
        color = '#f44336'
        bg_color = '#ffebee'
        icon = "⚠️"
        confidence = f"Confidence: {probability:.1%}"
        recommendation = "Please consult a neurologist for further evaluation."
        next_steps = [
            "📋 Schedule a clinical evaluation",
            "🧠 Consult with a movement disorder specialist",
            "📊 Consider additional diagnostic tests",
            "💊 Discuss treatment options if diagnosed"
        ]
    else:
        status = "✅ HEALTHY - No Parkinson's Detected"
        color = '#4caf50'
        bg_color = '#e8f5e9'
        icon = "✅"
        confidence = f"Confidence: {(1-probability):.1%}"
        recommendation = "No significant indicators detected. Regular check-ups recommended."
        next_steps = [
            "🏃 Maintain a healthy lifestyle",
            "🩺 Schedule regular health check-ups",
            "📈 Monitor for any voice changes",
            "📋 Continue routine screenings"
        ]
    
    return {
        'status': status,
        'color': color,
        'bg_color': bg_color,
        'icon': icon,
        'confidence': confidence,
        'recommendation': recommendation,
        'next_steps': next_steps,
        'raw_prediction': prediction,
        'raw_probability': probability
    }


def validate_input(values, feature_ranges):
    """
    Validate input values against expected ranges
    """
    errors = []
    warnings = []
    
    for feature, value in values.items():
        try:
            val = float(value)
            if feature in feature_ranges:
                min_val, max_val = feature_ranges[feature]
                if val < min_val or val > max_val:
                    errors.append(f"{feature}: {val} (expected: {min_val:.3f} - {max_val:.3f})")
                elif val < min_val * 1.1 or val > max_val * 0.9:
                    warnings.append(f"{feature}: {val} (near boundary: {min_val:.3f} - {max_val:.3f})")
        except ValueError:
            errors.append(f"{feature}: '{value}' is not a valid number")
    
    return errors, warnings


def get_feature_ranges(feature_names, df=None):
    """
    Get expected ranges for features
    """
    default_ranges = {
        'MDVP:Fo(Hz)': (88.0, 260.0),
        'MDVP:Fhi(Hz)': (100.0, 600.0),
        'MDVP:Flo(Hz)': (65.0, 240.0),
        'MDVP:Jitter(%)': (0.001, 0.035),
        'MDVP:Jitter(Abs)': (0.000007, 0.00026),
        'MDVP:RAP': (0.00068, 0.0215),
        'MDVP:PPQ': (0.00092, 0.0196),
        'Jitter:DDP': (0.00204, 0.0643),
        'MDVP:Shimmer': (0.0095, 0.119),
        'MDVP:Shimmer(dB)': (0.085, 1.302),
        'Shimmer:APQ3': (0.00455, 0.0565),
        'Shimmer:APQ5': (0.005, 0.064),
        'MDVP:APQ': (0.008, 0.075),
        'Shimmer:DDA': (0.0136, 0.169),
        'NHR': (0.00065, 0.315),
        'HNR': (8.44, 33.05),
        'RPDE': (0.2566, 0.685),
        'DFA': (0.574, 0.825),
        'spread1': (-7.965, -2.434),
        'spread2': (0.006, 0.451),
        'D2': (1.423, 3.671),
        'PPE': (0.0445, 0.527)
    }
    
    ranges = {}
    for feature in feature_names:
        if feature in default_ranges:
            ranges[feature] = default_ranges[feature]
        else:
            ranges[feature] = (0, 1000)
    
    return ranges


def generate_summary_report(results_df, output_path):
    """
    Generate a detailed summary report
    """
    report = []
    report.append("="*60)
    report.append("PARKINSON'S DISEASE DETECTION - SUMMARY REPORT")
    report.append("="*60)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Statistics
    total = len(results_df)
    parkinsons = (results_df['Prediction'] == "Parkinson's").sum()
    healthy = total - parkinsons
    
    report.append(f"Total Patients Analyzed: {total}")
    report.append(f"Parkinson's Detected: {parkinsons} ({parkinsons/total*100:.1f}%)")
    report.append(f"Healthy: {healthy} ({healthy/total*100:.1f}%)")
    report.append("")
    
    # Confidence statistics
    avg_confidence = results_df['Probability_Parkinsons'].mean()
    report.append(f"Average Confidence: {avg_confidence:.1%}")
    report.append("")
    
    report.append("-"*60)
    report.append("DETAILED RESULTS")
    report.append("-"*60)
    
    for i, row in results_df.iterrows():
        report.append(f"\nPatient {i+1}:")
        report.append(f"  Prediction: {row['Prediction']}")
        report.append(f"  Confidence: {row['Probability_Parkinsons']:.1%}")
    
    # Save report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    return output_path