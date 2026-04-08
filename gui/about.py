"""
Professional About Page
"""
import tkinter as tk
from tkinter import scrolledtext
from .config import COLORS


class AboutPage:
    """Professional About Page with System Information"""
    
    def __init__(self, parent):
        self.parent = parent
        self._create_ui()
    
    def _create_ui(self):
        """Create professional about page"""
        
        # Header
        header = tk.Frame(self.parent, bg=COLORS['primary'], height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="ℹ️ About NeuroDetect Pro", 
                font=('Segoe UI', 24, 'bold'), 
                fg='white', bg=COLORS['primary']).pack(pady=25)
        
        # Content
        content = tk.Frame(self.parent, bg=COLORS['background'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # System Overview
        overview_frame = tk.Frame(content, bg='white', relief='flat', bd=1,
                                  highlightbackground=COLORS['border'], highlightthickness=1)
        overview_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(overview_frame, text="System Overview", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg=COLORS['primary']).pack(anchor='w', padx=20, pady=15)
        
        overview_text = """
        NeuroDetect Pro is an advanced AI-powered medical screening system designed to assist healthcare professionals 
        in the early detection of Parkinson's disease through voice pattern analysis. The system utilizes state-of-the-art 
        machine learning algorithms to analyze 22 distinct voice biomarkers, providing rapid and accurate assessments.
        
        Key Capabilities:
        • Real-time voice pattern analysis
        • Batch processing for multiple patients
        • Comprehensive analytics and visualization
        • Secure user authentication
        • Professional reporting and export features
        """
        
        overview_widget = tk.Text(overview_frame, wrap=tk.WORD, font=('Segoe UI', 10),
                                   bg='white', fg=COLORS['dark'], height=8, padx=20, pady=10, relief='flat')
        overview_widget.insert('1.0', overview_text)
        overview_widget.config(state='disabled')
        overview_widget.pack(fill=tk.X)
        
        # Technical Specifications
        tech_frame = tk.Frame(content, bg='white', relief='flat', bd=1,
                              highlightbackground=COLORS['border'], highlightthickness=1)
        tech_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(tech_frame, text="Technical Specifications", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg=COLORS['primary']).pack(anchor='w', padx=20, pady=15)
        
        tech_grid = tk.Frame(tech_frame, bg='white')
        tech_grid.pack(fill=tk.X, padx=20, pady=10)
        
        tech_specs = [
            ("Model Architecture", "Stacking Ensemble (CatBoost + XGBoost + LightGBM + RF)"),
            ("Accuracy", "81.97%"),
            ("Sensitivity (Recall)", "97.96%"),
            ("AUC Score", "0.704"),
            ("Features Analyzed", "22 voice biomarkers"),
            ("Training Data", "UCI Parkinson's Dataset (195 samples)"),
            ("Framework", "Python + scikit-learn + XGBoost + CatBoost"),
            ("UI Framework", "Tkinter (Modern Healthcare Theme)")
        ]
        
        for i, (label, value) in enumerate(tech_specs):
            row = i // 2
            col = i % 2 * 2
            tk.Label(tech_grid, text=f"{label}:", font=('Segoe UI', 10, 'bold'),
                    bg='white', fg=COLORS['dark']).grid(row=row, column=col, sticky='w', padx=10, pady=8)
            tk.Label(tech_grid, text=value, font=('Segoe UI', 10),
                    bg='white', fg=COLORS['gray']).grid(row=row, column=col+1, sticky='w', padx=10, pady=8)
        
        # Team Information
        team_frame = tk.Frame(content, bg='white', relief='flat', bd=1,
                              highlightbackground=COLORS['border'], highlightthickness=1)
        team_frame.pack(fill=tk.X)
        
        tk.Label(team_frame, text="Development Team", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg=COLORS['primary']).pack(anchor='w', padx=20, pady=15)
        
        team_grid = tk.Frame(team_frame, bg='white')
        team_grid.pack(fill=tk.X, padx=20, pady=10)
        
        team_members = [
            ("Gayathri", "Project Lead & Environment Setup"),
            ("Krishna", "Data Analysis & EDA"),
            ("Sakshitha", "Feature Engineering"),
            ("Vishnu", "Model Building & Optimization"),
            ("Shiva", "GUI Development & Deployment")
        ]
        
        for i, (name, role) in enumerate(team_members):
            tk.Label(team_grid, text=f"{name}:", font=('Segoe UI', 10, 'bold'),
                    bg='white', fg=COLORS['primary']).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Label(team_grid, text=role, font=('Segoe UI', 10),
                    bg='white', fg=COLORS['gray']).grid(row=i, column=1, sticky='w', padx=10, pady=5)
        
        # Footer
        footer = tk.Frame(self.parent, bg=COLORS['light'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="© 2024 NeuroDetect Pro - All Rights Reserved | Version 2.0",
                font=('Segoe UI', 9), bg=COLORS['light'], fg=COLORS['gray']).pack(pady=10)