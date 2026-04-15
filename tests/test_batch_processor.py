"""
Test script for batch prediction functionality
Run this to validate the system before Week 10 presentation
"""
import os
import sys
import pandas as pd
import numpy as np
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.model_loader import ModelLoader
from gui.csv_handler import CSVHandler

def test_model_loading():
    """Test if model loads correctly"""
    print("="*60)
    print("TEST 1: Model Loading")
    print("="*60)
    
    loader = ModelLoader()
    success = loader.load_model()
    
    if success:
        print("✅ Model loaded successfully")
        print(f"   Features: {len(loader.get_feature_names())}")
        return loader
    else:
        print("❌ Model loading failed")
        return None

def test_single_prediction(loader):
    """Test single prediction"""
    print("\n" + "="*60)
    print("TEST 2: Single Prediction")
    print("="*60)
    
    # Sample patient data (Parkinson's case)
    sample_values = [
        119.992, 157.302, 74.997, 0.00784, 0.00007,
        0.00370, 0.00554, 0.01109, 0.04374, 0.426,
        0.02182, 0.03106, 0.02971, 0.06545, 0.02211,
        21.033, 0.414783, 0.815285, -4.813031, 0.266482,
        2.301442, 0.284654
    ]
    
    try:
        prediction, probability = loader.predict_single(sample_values)
        status = "Parkinson's" if prediction == 1 else "Healthy"
        print(f"✅ Prediction successful")
        print(f"   Prediction: {status}")
        print(f"   Probability: {probability:.4f}")
        return True
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_csv_validation():
    """Test CSV validation using actual CSVHandler methods"""
    print("\n" + "="*60)
    print("TEST 3: CSV Validation")
    print("="*60)
    
    feature_names = [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
        'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
        'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
        'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1',
        'spread2', 'D2', 'PPE'
    ]
    
    handler = CSVHandler(feature_names)
    
    # Test 1: Valid CSV file
    print("\n   Test 1: Valid CSV file...")
    valid_data = pd.DataFrame({col: [0.5] for col in feature_names})
    
    # Save to temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        valid_data.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        df, error = handler.load_csv(temp_file)
        if error is None:
            print("   ✅ Valid CSV accepted")
        else:
            print(f"   ❌ Valid CSV rejected: {error}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        os.unlink(temp_file)
    
    # Test 2: CSV with missing columns
    print("\n   Test 2: CSV with missing columns...")
    missing_cols = feature_names[:-1]  # Missing PPE column
    invalid_data = pd.DataFrame({col: [0.5] for col in missing_cols})
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        invalid_data.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        df, error = handler.load_csv(temp_file)
        if error:
            print(f"   ✅ Missing columns detected")
            print(f"      Error: {error[:80]}...")
        else:
            print("   ❌ Missing columns not detected")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        os.unlink(temp_file)
    
    # Test 3: Empty CSV file
    print("\n   Test 3: Empty CSV file...")
    empty_data = pd.DataFrame(columns=feature_names)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        empty_data.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        df, error = handler.load_csv(temp_file)
        if error:
            print(f"   ✅ Empty file detected: {error[:50]}...")
        else:
            print("   ❌ Empty file not detected")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        os.unlink(temp_file)
    
    return True

def test_batch_prediction(loader):
    """Test batch prediction"""
    print("\n" + "="*60)
    print("TEST 4: Batch Prediction")
    print("="*60)
    
    feature_names = loader.get_feature_names()
    
    # Create test data with 3 patients
    test_data = pd.DataFrame({
        feature_names[0]: [119.992, 101.982, 129.931],
        feature_names[1]: [157.302, 125.552, 151.126],
        feature_names[2]: [74.997, 88.013, 118.501],
    })
    
    # Fill remaining columns with default values
    for col in feature_names[3:]:
        test_data[col] = 0.01
    
    try:
        predictions, probabilities = loader.predict_batch(test_data)
        print(f"✅ Batch prediction successful")
        print(f"   Patients processed: {len(predictions)}")
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            status = "Parkinson's" if pred == 1 else "Healthy"
            print(f"   Patient {i+1}: {status} (Confidence: {prob:.1%})")
        return True
    except Exception as e:
        print(f"❌ Batch prediction failed: {e}")
        return False

def test_numeric_validation():
    """Test numeric value validation"""
    print("\n" + "="*60)
    print("TEST 5: Numeric Value Validation")
    print("="*60)
    
    feature_names = [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
        'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
        'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
        'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1',
        'spread2', 'D2', 'PPE'
    ]
    
    handler = CSVHandler(feature_names)
    
    # Test with non-numeric values
    print("\n   Testing CSV with non-numeric values...")
    invalid_data = pd.DataFrame({
        feature_names[0]: ['abc', 'def', 'ghi'],
        feature_names[1]: [157.302, 125.552, 151.126],
    })
    
    # Fill remaining columns
    for col in feature_names[2:]:
        invalid_data[col] = 0.01
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        invalid_data.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        df, error = handler.load_csv(temp_file)
        if error:
            print(f"   ✅ Non-numeric values detected")
        else:
            # Validate numeric values
            errors = handler.validate_values(df)
            if errors:
                print(f"   ✅ Non-numeric values detected via validate_values")
                print(f"      Errors: {errors[:1]}...")
            else:
                print("   ❌ Non-numeric values not detected")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        os.unlink(temp_file)
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PARKINSON'S DETECTION SYSTEM - TEST SUITE")
    print("="*60)
    
    # Test 1: Model Loading
    loader = test_model_loading()
    if loader is None:
        print("\n❌ Critical: Model failed to load. Aborting tests.")
        return
    
    # Test 2: Single Prediction
    test_single_prediction(loader)
    
    # Test 3: CSV Validation
    test_csv_validation()
    
    # Test 4: Batch Prediction
    test_batch_prediction(loader)
    
    # Test 5: Numeric Validation
    test_numeric_validation()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()