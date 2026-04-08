"""
Configuration settings for the Parkinson's Detection GUI - Modern Theme
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Model files
MODEL_PATH = os.path.join(MODELS_DIR, 'catboost_gui_model.joblib')
SCALER_PATH = os.path.join(MODELS_DIR, 'production_scaler.joblib')
FEATURES_PATH = os.path.join(DATA_DIR, 'selected_features.txt')

# Fallback
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(MODELS_DIR, 'random_forest_baseline.joblib')
if not os.path.exists(SCALER_PATH):
    SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.joblib')

# GUI Settings
APP_TITLE = "NeuroDetect Pro"
APP_WIDTH = 1100
APP_HEIGHT = 800

# Modern Color Palette (Healthcare Theme)
COLORS = {
    'primary': '#1a73e8',       # Medical Blue
    'primary_dark': '#0d47a1',   # Dark Blue
    'secondary': '#00bcd4',      # Teal
    'success': '#4caf50',        # Green
    'danger': '#f44336',         # Red
    'warning': '#ff9800',        # Orange
    'info': '#2196f3',           # Light Blue
    'light': '#f8f9fa',          # Off-white
    'dark': '#343a40',           # Dark Gray
    'gray': '#6c757d',           # Medium Gray
    'background': '#ffffff',     # White background
    'card_bg': '#ffffff',        # Card background
    'sidebar_bg': '#f0f2f5',     # Sidebar background
    'border': '#e0e0e0',         # Border color
    'text': '#212529',           # Text color
    'text_muted': '#6c757d'      # Muted text
}

# Fonts
FONT_FAMILY = 'Segoe UI'
FONT_SIZES = {
    'title': 22,
    'heading': 16,
    'subheading': 14,
    'normal': 11,
    'small': 9
}

# CSV Export Settings
EXPORT_FILENAME = 'parkinsons_predictions.csv'

# Model Settings
OPTIMAL_THRESHOLD = 0.6644