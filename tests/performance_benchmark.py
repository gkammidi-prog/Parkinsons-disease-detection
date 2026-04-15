"""
Performance benchmark for the Parkinson's Detection System
"""
import time
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.model_loader import ModelLoader

def benchmark_prediction_speed():
    """Measure prediction speed"""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARK: Prediction Speed")
    print("="*60)
    
    loader = ModelLoader()
    loader.load_model()
    
    feature_names = loader.get_feature_names()
    n_features = len(feature_names)
    
    # Test single prediction
    sample_values = [0.5] * n_features
    times = []
    
    for i in range(100):
        start = time.time()
        loader.predict_single(sample_values)
        end = time.time()
        times.append(end - start)
    
    avg_time = np.mean(times) * 1000  # Convert to milliseconds
    std_time = np.std(times) * 1000
    
    print(f"Single prediction (100 iterations):")
    print(f"  Average: {avg_time:.2f} ms")
    print(f"  Std Dev: {std_time:.2f} ms")
    print(f"  Min: {min(times)*1000:.2f} ms")
    print(f"  Max: {max(times)*1000:.2f} ms")
    
    return avg_time

def benchmark_batch_processing():
    """Measure batch processing speed"""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARK: Batch Processing")
    print("="*60)
    
    loader = ModelLoader()
    loader.load_model()
    
    feature_names = loader.get_feature_names()
    n_features = len(feature_names)
    
    # Test different batch sizes
    batch_sizes = [1, 10, 50, 100, 500]
    
    for batch_size in batch_sizes:
        # Create test data
        data = pd.DataFrame(np.random.randn(batch_size, n_features), columns=feature_names)
        
        start = time.time()
        predictions, probabilities = loader.predict_batch(data)
        end = time.time()
        
        elapsed = (end - start) * 1000  # milliseconds
        per_patient = elapsed / batch_size
        
        print(f"Batch size {batch_size:3d}: {elapsed:.2f} ms total, {per_patient:.2f} ms per patient")

def benchmark_model_load_time():
    """Measure model loading time"""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARK: Model Load Time")
    print("="*60)
    
    start = time.time()
    loader = ModelLoader()
    loader.load_model()
    end = time.time()
    
    load_time = (end - start) * 1000
    print(f"Model load time: {load_time:.2f} ms")
    
    return load_time

def main():
    print("\n" + "="*60)
    print("PARKINSON'S DETECTION SYSTEM - PERFORMANCE BENCHMARK")
    print("="*60)
    
    benchmark_model_load_time()
    benchmark_prediction_speed()
    benchmark_batch_processing()
    
    print("\n" + "="*60)
    print("BENCHMARK COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()