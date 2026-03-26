# Parkinson's Disease Detection using Ensemble Machine Learning

**Team Members:**
- Gayathri – Project Setup & Environment
- Krishna – Data Analysis & EDA
- Sakshitha – Feature Engineering
- Vishnu – Model Building
- Shiva – Deployment (GUI)

## Dataset
UCI Parkinson's Disease Classification Dataset  
Source: [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/parkinsons)  
Description: 756 samples, 754 biomedical voice features, binary classification (1 = Parkinson's, 0 = healthy).

## Project Structure
- data/raw – original dataset
- data/processed – cleaned, scaled, feature‑selected data
- 
otebooks – Colab notebooks for each phase
- src – reusable Python scripts (if any)
- models – saved .joblib models
- gui – Windows GUI application (Tkinter / PyQt)
- 	ests – unit tests (optional)
- eports/figures – plots and figures for the report

## How to Run
1. Clone this repository.
2. Install dependencies: pip install -r requirements.txt
3. For data science work, open the notebooks in Google Colab and mount your Google Drive.
4. For GUI, run gui/app.py locally.

## Environment
- Data Science: Google Colab + shared Google Drive
- GUI: Python 3.9+ locally (Tkinter included)
