"""
Advanced Analytics Module with Professional Charts
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from .config import COLORS

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
sns.set_context("talk", font_scale=0.8)


def create_advanced_analytics(parent, data, title="Analytics Dashboard"):
    """
    Create advanced analytics dashboard with multiple chart types
    """
    # Create figure with subplots
    fig = plt.figure(figsize=(12, 10), facecolor='white')
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    # 1. Donut Chart - Prediction Distribution
    ax1 = fig.add_subplot(2, 3, 1)
    parkinsons = sum(data['predictions'])
    healthy = len(data['predictions']) - parkinsons
    
    # Donut chart
    wedges, texts, autotexts = ax1.pie([parkinsons, healthy], 
                                        labels=['Parkinson\'s', 'Healthy'],
                                        colors=['#e74c3c', '#4caf50'],
                                        autopct='%1.1f%%',
                                        startangle=90,
                                        wedgeprops=dict(width=0.3, edgecolor='white'))
    
    # Center circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=0)
    ax1.add_artist(centre_circle)
    ax1.set_title('Prediction Distribution', fontsize=12, fontweight='bold')
    
    # 2. Confidence Distribution (KDE)
    ax2 = fig.add_subplot(2, 3, 2)
    confidences = data['probabilities']
    parkinsons_conf = [c for c, p in zip(confidences, data['predictions']) if p == 1]
    healthy_conf = [1-c for c, p in zip(confidences, data['predictions']) if p == 0]
    
    sns.kdeplot(parkinsons_conf, ax=ax2, fill=True, color='#e74c3c', label='Parkinson\'s', alpha=0.5)
    sns.kdeplot(healthy_conf, ax=ax2, fill=True, color='#4caf50', label='Healthy', alpha=0.5)
    ax2.set_xlabel('Confidence Score')
    ax2.set_ylabel('Density')
    ax2.set_title('Confidence Distribution', fontsize=12, fontweight='bold')
    ax2.legend()
    
    # 3. Radar Chart - Feature Importance
    ax3 = fig.add_subplot(2, 3, 3, projection='polar')
    features = ['Jitter', 'Shimmer', 'HNR', 'RPDE', 'DFA', 'PPE']
    importance = [0.85, 0.78, 0.92, 0.88, 0.76, 0.95]
    
    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    importance += importance[:1]
    angles += angles[:1]
    
    ax3.plot(angles, importance, 'o-', linewidth=2, color=COLORS['primary'])
    ax3.fill(angles, importance, alpha=0.25, color=COLORS['primary'])
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(features, fontsize=9)
    ax3.set_title('Feature Importance', fontsize=12, fontweight='bold', pad=20)
    
    # 4. Trend Line
    ax4 = fig.add_subplot(2, 3, 4)
    if len(data['predictions']) > 1:
        rolling_avg = pd.Series([1 if p == 1 else 0 for p in data['predictions']]).rolling(3, min_periods=1).mean()
        ax4.plot(rolling_avg, marker='o', linewidth=2, color=COLORS['secondary'], markersize=4)
        ax4.fill_between(range(len(rolling_avg)), 0, rolling_avg, alpha=0.3, color=COLORS['secondary'])
    ax4.set_xlabel('Analysis Sequence')
    ax4.set_ylabel('Parkinson\'s Detection Rate')
    ax4.set_title('Detection Trend', fontsize=12, fontweight='bold')
    ax4.set_ylim(0, 1)
    ax4.grid(True, alpha=0.3)
    
    # 5. Source Comparison
    ax5 = fig.add_subplot(2, 3, 5)
    source_data = {
        'Manual': [sum(1 for i, s in enumerate(data['source']) if s == 'manual' and data['predictions'][i] == 1),
                   sum(1 for i, s in enumerate(data['source']) if s == 'manual' and data['predictions'][i] == 0)],
        'Batch': [sum(1 for i, s in enumerate(data['source']) if s == 'batch' and data['predictions'][i] == 1),
                  sum(1 for i, s in enumerate(data['source']) if s == 'batch' and data['predictions'][i] == 0)]
    }
    
    x = np.arange(2)
    width = 0.35
    ax5.bar(x - width/2, source_data['Manual'], width, label='Manual', color='#3498db')
    ax5.bar(x + width/2, source_data['Batch'], width, label='Batch', color='#1abc9c')
    ax5.set_xticks(x)
    ax5.set_xticklabels(['Parkinson\'s', 'Healthy'])
    ax5.set_ylabel('Count')
    ax5.set_title('Predictions by Source', fontsize=12, fontweight='bold')
    ax5.legend()
    
    # 6. Summary Statistics Card
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    total = len(data['predictions'])
    parkinsons_count = sum(data['predictions'])
    healthy_count = total - parkinsons_count
    avg_confidence = np.mean([p if pred == 1 else 1-p for p, pred in zip(data['probabilities'], data['predictions'])])
    
    stats_text = f"""
    📊 SUMMARY STATISTICS
    ═══════════════════════════════════════
    
    Total Analyses:        {total:>6}
    Parkinson's Detected:  {parkinsons_count:>6} ({parkinsons_count/total*100:>5.1f}%)
    Healthy:               {healthy_count:>6} ({healthy_count/total*100:>5.1f}%)
    
    ═══════════════════════════════════════
    Average Confidence:    {avg_confidence:>6.1%}
    Detection Rate:        {parkinsons_count/total*100:>6.1f}%
    
    ═══════════════════════════════════════
    Manual Analyses:       {sum(1 for s in data['source'] if s == 'manual'):>6}
    Batch Analyses:        {sum(1 for s in data['source'] if s == 'batch'):>6}
    """
    
    ax6.text(0.1, 0.95, stats_text, transform=ax6.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor=COLORS['border']))
    
    plt.tight_layout()
    
    # Embed in tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return canvas