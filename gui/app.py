"""
NeuroDetect Pro - Main Application with Homepage First
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.config import APP_TITLE, APP_WIDTH, APP_HEIGHT, COLORS
from gui.utils import format_prediction, validate_input, get_feature_ranges, generate_summary_report
from gui.model_loader import ModelLoader
from gui.csv_handler import CSVHandler
from gui.styles import (get_primary_button_style, get_secondary_button_style,
                        get_danger_button_style, get_success_button_style,
                        get_card_style)
from gui.login import LoginSystem
from gui.homepage import Homepage


class NeuroDetectApp:
    """Main Application Class - Homepage First"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.configure(bg=COLORS['background'])
        self.root.minsize(900, 700)
        
        # Set icon
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Initialize components
        self.model_loader = ModelLoader()
        self.csv_handler = None
        self.feature_names = []
        self.feature_ranges = {}
        self.input_entries = {}
        
        # Data storage
        self.analytics_data = {
            'predictions': [],
            'probabilities': [],
            'patient_ids': [],
            'source': []
        }
        
        self.batch_results_data = None
        self.batch_predictions = None
        self.batch_probabilities = None
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("🔄 Initializing NeuroDetect Pro...")
        self.model_loaded = False
        self.current_user = None
        
        # UI elements
        self.form_container = None
        self.loading_label = None
        self.predict_btn = None
        self.batch_threshold_var = None
        self.batch_threshold_label = None
        
        # Show Homepage first
        self._show_homepage()
        
        # Start model loading in background
        self._load_model_background()
    
    def _show_homepage(self):
        """Show the initial homepage"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.homepage = Homepage(self.root, self._show_login, self._show_register)
    
    def _show_login(self):
        """Show login screen"""
        self._clear_window()
        LoginSystem(self.root, self._on_login_success, self._show_homepage, show_register=False)
    
    def _show_register(self):
        """Show registration screen"""
        self._clear_window()
        LoginSystem(self.root, self._on_login_success, self._show_homepage, show_register=True)
    
    def _clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _on_login_success(self, username, user_data):
        """Handle successful login - show user homepage"""
        self.current_user = {'username': username, 'data': user_data}
        self._show_user_homepage()
    
    def _show_user_homepage(self):
        """Show homepage with user info and launch button"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create user homepage with launch button
        self._create_user_homepage()
    
    def _create_user_homepage(self):
        """Create user homepage"""
        
        # Header
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧠 NeuroDetect Pro", 
                font=('Segoe UI', 22, 'bold'), 
                fg='white', bg=COLORS['primary']).pack(side=tk.LEFT, padx=30, pady=20)
        
        tk.Label(header, text=f"Welcome, {self.current_user['data']['name']}",
                font=('Segoe UI', 11), fg='#e0e0e0', bg=COLORS['primary']).pack(side=tk.RIGHT, padx=30, pady=25)
        
        # Main container
        main = tk.Frame(self.root, bg=COLORS['background'])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Welcome Card
        welcome_card = tk.Frame(main, bg='white', relief='flat', bd=1,
                                highlightbackground=COLORS['border'], highlightthickness=1)
        welcome_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(welcome_card, text="👋 Welcome to NeuroDetect Pro", 
                font=('Segoe UI', 24, 'bold'), bg='white', fg=COLORS['primary']).pack(pady=(25, 10))
        
        tk.Label(welcome_card, text="Your AI-Powered Assistant for Early Parkinson's Detection",
                font=('Segoe UI', 12), bg='white', fg=COLORS['gray']).pack(pady=(0, 20))
        
        # Stats Cards
        stats_frame = tk.Frame(main, bg=COLORS['background'])
        stats_frame.pack(fill=tk.X, pady=(0, 25))
        
        stats = [
            {"icon": "🎯", "title": "Model Accuracy", "value": "81.97%", "color": COLORS['success']},
            {"icon": "🩺", "title": "Sensitivity", "value": "97.96%", "color": COLORS['info']},
            {"icon": "📊", "title": "Features", "value": "22", "color": COLORS['secondary']},
            {"icon": "⚡", "title": "Analysis Speed", "value": "< 1 sec", "color": COLORS['warning']}
        ]
        
        for stat in stats:
            card = tk.Frame(stats_frame, bg='white', relief='flat', bd=1,
                           highlightbackground=COLORS['border'], highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(card, text=stat['icon'], font=('Segoe UI', 28), 
                    bg='white', fg=stat['color']).pack(pady=(12, 5))
            tk.Label(card, text=stat['value'], font=('Segoe UI', 20, 'bold'),
                    bg='white', fg=stat['color']).pack()
            tk.Label(card, text=stat['title'], font=('Segoe UI', 10),
                    bg='white', fg=COLORS['gray']).pack(pady=(0, 12))
        
        # Launch Button
        launch_btn = tk.Button(main, text="🚀 Launch Detection System", 
                               command=self._create_main_ui,
                               **get_primary_button_style())
        launch_btn.pack(pady=20, ipadx=30, ipady=10)
        
        # Info Section
        info_card = tk.Frame(main, bg='white', relief='flat', bd=1,
                             highlightbackground=COLORS['border'], highlightthickness=1)
        info_card.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(info_card, text="📋 How It Works", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg=COLORS['primary']).pack(pady=(15, 10))
        
        steps = [
            "1️⃣ Enter patient voice measurements (22 parameters)",
            "2️⃣ AI model analyzes the voice patterns",
            "3️⃣ Get instant prediction with confidence score",
            "4️⃣ Export results or process multiple patients via CSV"
        ]
        
        for step in steps:
            tk.Label(info_card, text=step, font=('Segoe UI', 10),
                    bg='white', fg=COLORS['dark'], anchor='w').pack(fill=tk.X, padx=20, pady=3)
        
        tk.Label(info_card, text="\n⚠️ Important: This tool is for screening purposes only. Always consult a medical professional for diagnosis.",
                font=('Segoe UI', 9), bg='white', fg=COLORS['gray']).pack(pady=(10, 15))
        
        # Logout button
        logout_btn = tk.Button(main, text="🚪 Logout", command=self._logout,
                               bg=COLORS['danger'], fg='white', font=('Segoe UI', 10),
                               padx=20, pady=5, cursor='hand2', relief='flat')
        logout_btn.pack(pady=10)
        
        # Footer
        footer = tk.Frame(self.root, bg=COLORS['light'], height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="© 2024 NeuroDetect Pro - AI-Powered Parkinson's Detection",
                font=('Segoe UI', 8), bg=COLORS['light'], fg=COLORS['gray']).pack(pady=10)
    
    def _create_main_ui(self):
        """Create main application UI after login"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🧠 NeuroDetect Pro", 
                               font=('Segoe UI', 22, 'bold'), 
                               fg='white', bg=COLORS['primary'])
        title_label.pack(side=tk.LEFT, padx=30, pady=15)
        
        user_label = tk.Label(header_frame, text=f"Welcome, {self.current_user['data']['name']}",
                              font=('Segoe UI', 10), fg='#e0e0e0', bg=COLORS['primary'])
        user_label.pack(side=tk.RIGHT, padx=30, pady=22)
        
        logout_btn = tk.Button(header_frame, text="🚪 Logout", command=self._logout,
                               bg=COLORS['danger'], fg='white', font=('Segoe UI', 9),
                               padx=10, pady=5, cursor='hand2', relief='flat')
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=18)
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self._create_manual_tab()
        self._create_batch_tab()
        self._create_analytics_tab()
        self._create_about_tab()
        
        # Status Bar
        status_bar = tk.Frame(self.root, bg=COLORS['dark'], height=35)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = tk.Label(status_bar, textvariable=self.status_var, 
                                bg=COLORS['dark'], fg='white', anchor='w', 
                                font=('Segoe UI', 9), padx=15)
        status_label.pack(fill=tk.X, side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_bar, mode='indeterminate', length=150)
        self.progress.pack(side=tk.RIGHT, padx=15)
        
        # Start model loading if not already loaded
        if not self.model_loaded:
            self._load_model_background()
        else:
            if self.feature_names:
                self._populate_input_fields()
                if self.predict_btn:
                    self.predict_btn.config(state='normal')
    
    def _create_manual_tab(self):
        """Create manual input tab with scrollable area and threshold slider"""
        manual_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(manual_frame, text="📝 Manual Input")
        
        # Create a canvas with scrollbar for the ENTIRE manual tab
        main_canvas = tk.Canvas(manual_frame, bg=COLORS['background'], highlightthickness=0)
        main_scrollbar = tk.Scrollbar(manual_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Input Form Section (Left side)
        form_frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        # Input Card
        input_card = tk.Frame(form_frame, **get_card_style())
        input_card.pack(fill=tk.BOTH, expand=True, pady=5)
        
        card_header = tk.Frame(input_card, bg=COLORS['primary'], height=45)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        tk.Label(card_header, text="Patient Voice Measurements", 
                font=('Segoe UI', 13, 'bold'), fg='white', bg=COLORS['primary']).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Form container for input fields
        self.form_container = tk.Frame(input_card, bg='white')
        self.form_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Loading placeholder
        self.loading_label = tk.Label(self.form_container, text="🔄 Loading AI Model...\n\nPlease wait while the model loads.",
                                      font=('Segoe UI', 12), bg='white', fg=COLORS['gray'], justify='center')
        self.loading_label.pack(expand=True, pady=50)
        
        # Results Panel (Right side)
        results_frame = tk.Frame(scrollable_frame, bg=COLORS['background'], width=400)
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        results_frame.pack_propagate(False)
        
        # Results Card
        self.result_card = tk.Frame(results_frame, **get_card_style())
        self.result_card.pack(fill=tk.BOTH, expand=True, pady=5)
        
        result_header = tk.Frame(self.result_card, bg=COLORS['info'], height=45)
        result_header.pack(fill=tk.X)
        result_header.pack_propagate(False)
        tk.Label(result_header, text="Analysis Result", 
                font=('Segoe UI', 13, 'bold'), fg='white', bg=COLORS['info']).pack(side=tk.LEFT, padx=15, pady=10)
        
        self.result_content = tk.Frame(self.result_card, bg='white')
        self.result_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.result_label = tk.Label(self.result_content, text="Ready to analyze...",
                                     font=('Segoe UI', 12), bg='white', fg=COLORS['gray'],
                                     wraplength=320, justify='center')
        self.result_label.pack(expand=True)
        
        # Manual Threshold Slider Section
        manual_threshold_frame = tk.Frame(self.result_card, bg='white')
        manual_threshold_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=10)
        
        tk.Label(manual_threshold_frame, text="Detection Sensitivity Threshold:", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['dark']).pack()
        
        self.manual_threshold_var = tk.DoubleVar(value=0.8)
        
        manual_threshold_scale = tk.Scale(
            manual_threshold_frame, from_=0.5, to=0.95, resolution=0.01,
            orient=tk.HORIZONTAL, variable=self.manual_threshold_var,
            length=250, bg='white', fg=COLORS['primary'],
            font=('Segoe UI', 9)
        )
        manual_threshold_scale.pack(pady=5)
        
        self.manual_threshold_label = tk.Label(manual_threshold_frame,
            text=f"Current: {self.manual_threshold_var.get():.2f} | Lower=More Sensitive, Higher=More Specific",
            font=('Segoe UI', 8), bg='white', fg=COLORS['gray'])
        self.manual_threshold_label.pack()
        
        def update_manual_threshold(*args):
            self.manual_threshold_label.config(
                text=f"Current: {self.manual_threshold_var.get():.2f} | Lower=More Sensitive, Higher=More Specific"
            )
            self.model_loader.optimal_threshold = self.manual_threshold_var.get()
        
        self.manual_threshold_var.trace('w', update_manual_threshold)
        
        # Buttons
        button_frame = tk.Frame(self.result_card, bg='white', height=60)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=10)
        
        self.predict_btn = tk.Button(button_frame, text="🔍 PREDICT", command=self.predict_manual,
                                     **get_primary_button_style())
        self.predict_btn.pack(side=tk.LEFT, padx=5)
        self.predict_btn.config(state='disabled')
        
        clear_btn = tk.Button(button_frame, text="🗑️ CLEAR", command=self.clear_manual_inputs,
                              **get_danger_button_style())
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_batch_tab(self):
        """Create batch upload tab with threshold slider"""
        batch_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(batch_frame, text="📁 Batch Upload")
        
        # Upload Card
        upload_card = tk.Frame(batch_frame, **get_card_style())
        upload_card.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(upload_card, text="CSV File Upload", font=('Segoe UI', 14, 'bold'),
                bg='white', fg=COLORS['primary']).pack(pady=(15, 5))
        
        tk.Label(upload_card, text="Upload a CSV file with patient voice measurements.\n"
                 "The file must contain all 22 required feature columns.",
                 bg='white', fg=COLORS['gray'], font=('Segoe UI', 10)).pack(pady=(0, 15))
        
        file_frame = tk.Frame(upload_card, bg='white')
        file_frame.pack(pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, width=50,
                              font=('Segoe UI', 10), bg=COLORS['light'])
        file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(file_frame, text="📂 Browse", command=self.browse_csv,
                               **get_secondary_button_style())
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        upload_btn = tk.Button(upload_card, text="🚀 UPLOAD & PREDICT", command=self.predict_batch,
                               **get_primary_button_style())
        upload_btn.pack(pady=15)
        
        # Batch Threshold Slider Section
        batch_threshold_frame = tk.Frame(upload_card, bg='white')
        batch_threshold_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(batch_threshold_frame, text="Batch Detection Threshold:", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg=COLORS['dark']).pack()
        
        self.batch_threshold_var = tk.DoubleVar(value=0.8)
        
        batch_threshold_scale = tk.Scale(
            batch_threshold_frame, from_=0.5, to=0.95, resolution=0.01,
            orient=tk.HORIZONTAL, variable=self.batch_threshold_var,
            length=300, bg='white', fg=COLORS['primary'],
            font=('Segoe UI', 9)
        )
        batch_threshold_scale.pack(pady=5)
        
        self.batch_threshold_label = tk.Label(batch_threshold_frame,
            text=f"Current Threshold: {self.batch_threshold_var.get():.2f} | Lower=More Sensitive, Higher=More Specific",
            font=('Segoe UI', 8), bg='white', fg=COLORS['gray'])
        self.batch_threshold_label.pack()
        
        def update_batch_threshold(*args):
            self.batch_threshold_label.config(
                text=f"Current Threshold: {self.batch_threshold_var.get():.2f} | Lower=More Sensitive, Higher=More Specific"
            )
        
        self.batch_threshold_var.trace('w', update_batch_threshold)
        
        # Results Card
        results_card = tk.Frame(batch_frame, **get_card_style())
        results_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(results_card, text="Batch Results", font=('Segoe UI', 13, 'bold'),
                bg='white', fg=COLORS['primary']).pack(pady=(10, 5))
        
        text_frame = tk.Frame(results_card, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.batch_result_text = scrolledtext.ScrolledText(text_frame, width=80, height=12,
                                                            font=('Consolas', 10),
                                                            bg=COLORS['light'],
                                                            relief='flat')
        self.batch_result_text.pack(fill=tk.BOTH, expand=True)
        
        export_frame = tk.Frame(results_card, bg='white')
        export_frame.pack(fill=tk.X, pady=10)
        
        self.export_btn = tk.Button(export_frame, text="📊 Export Results", command=self.export_results,
                                    **get_success_button_style())
        self.export_btn.pack(pady=5)
        self.export_btn.config(state='disabled')
        
        self.batch_results_data = None
        self.batch_predictions = None
        self.batch_probabilities = None
    
    def _create_analytics_tab(self):
        """Create analytics tab"""
        self.analytics_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.analytics_frame, text="📊 Analytics")
        
        self.analytics_canvas_frame = tk.Frame(self.analytics_frame, bg=COLORS['background'])
        self.analytics_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        refresh_btn = tk.Button(self.analytics_frame, text="🔄 Refresh Analytics", 
                                command=self.update_analytics,
                                **get_secondary_button_style())
        refresh_btn.pack(pady=5)
        
        self.analytics_label = tk.Label(self.analytics_canvas_frame, 
                                        text="No data available. Make predictions first.",
                                        font=('Segoe UI', 12), bg=COLORS['background'], 
                                        fg=COLORS['gray'], justify='center')
        self.analytics_label.pack(expand=True)
    
    def _create_about_tab(self):
        """Create about tab"""
        about_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(about_frame, text="ℹ️ About")
        
        about_text = """
        NeuroDetect Pro - AI-Powered Parkinson's Detection System
        
        Version: 2.0
        Model: CatBoost Classifier
        Features: 22 voice biomarkers
        
        Team:
        - Gayathri: Project Lead & Environment Setup
        - Krishna: Data Analysis & EDA
        - Sakshitha: Feature Engineering
        - Vishnu: Model Building & Optimization
        - Shiva: GUI Development & Deployment
        
        Important: This tool is for screening purposes only.
        Always consult a medical professional for diagnosis.
        """
        
        about_widget = scrolledtext.ScrolledText(about_frame, wrap=tk.WORD, width=80, height=25,
                                                  font=('Segoe UI', 10), bg=COLORS['light'])
        about_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        about_widget.insert('1.0', about_text)
        about_widget.config(state='disabled')
    
    def _load_model_background(self):
        """Load model in background"""
        self.status_var.set("🔄 Loading AI Model... Please wait")
        if hasattr(self, 'progress') and self.progress:
            self.progress.start(10)
        
        def load():
            success = self.model_loader.load_model()
            self.root.after(0, lambda: self._on_model_loaded(success))
        
        threading.Thread(target=load, daemon=True).start()
    
    def _on_model_loaded(self, success):
        """Handle model loaded"""
        if hasattr(self, 'progress') and self.progress:
            self.progress.stop()
        
        if success:
            self.model_loaded = True
            self.feature_names = self.model_loader.get_feature_names()
            self.feature_ranges = get_feature_ranges(self.feature_names)
            self.csv_handler = CSVHandler(self.feature_names)
            
            if hasattr(self, 'form_container') and self.form_container:
                self.root.after(0, self._populate_input_fields)
            if hasattr(self, 'predict_btn') and self.predict_btn:
                self.predict_btn.config(state='normal')
            
            self.status_var.set(f"✅ Model ready. {len(self.feature_names)} features loaded.")
            print(f"✅ Model ready. {len(self.feature_names)} features loaded.")
        else:
            self.status_var.set(f"❌ Error: {self.model_loader.error_message}")
            print(f"❌ Error: {self.model_loader.error_message}")
            messagebox.showerror("Model Load Error", self.model_loader.error_message)
    
    def _populate_input_fields(self):
        """Populate input fields after model loads"""
        if self.loading_label and self.loading_label.winfo_exists():
            self.loading_label.destroy()
            self.loading_label = None
        
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        left_column = tk.Frame(self.form_container, bg='white')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = tk.Frame(self.form_container, bg='white')
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.input_entries = {}
        mid_point = len(self.feature_names) // 2
        
        for i, feature in enumerate(self.feature_names):
            column = left_column if i < mid_point else right_column
            
            field_frame = tk.Frame(column, bg='white')
            field_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(field_frame, text=feature, font=('Segoe UI', 9),
                            bg='white', anchor='w', width=24)
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(field_frame, width=14, font=('Segoe UI', 9),
                            bg=COLORS['light'], relief='flat', bd=1)
            entry.pack(side=tk.RIGHT, padx=5)
            self.input_entries[feature] = entry
        
        print(f"✅ Manual input fields populated: {len(self.feature_names)} fields")
    
    def _logout(self):
        """Logout and return to homepage"""
        self.current_user = None
        self._show_homepage()
    
    def predict_manual(self):
        """Make prediction from manual input using current threshold"""
        if not self.model_loaded:
            messagebox.showwarning("Not Ready", "Model still loading. Please wait.")
            return
        
        # Update threshold from manual slider
        if hasattr(self, 'manual_threshold_var'):
            self.model_loader.optimal_threshold = self.manual_threshold_var.get()
        
        values = {}
        for feature, entry in self.input_entries.items():
            values[feature] = entry.get().strip()
        
        empty_fields = [f for f, v in values.items() if not v]
        if empty_fields:
            messagebox.showerror("Input Error", f"Please fill all fields.\nMissing: {empty_fields[:5]}")
            return
        
        errors, warnings = validate_input(values, self.feature_ranges)
        
        if errors:
            messagebox.showerror("Input Error", "Invalid values:\n" + "\n".join(errors[:5]))
            return
        
        try:
            value_list = [float(values[f]) for f in self.feature_names]
            prediction, probability = self.model_loader.predict_single(value_list)
            result = format_prediction(prediction, probability)
            
            patient_id = f"Manual_{len(self.analytics_data['predictions']) + 1}"
            self.analytics_data['predictions'].append(prediction)
            self.analytics_data['probabilities'].append(probability)
            self.analytics_data['patient_ids'].append(patient_id)
            self.analytics_data['source'].append('manual')
            
            for widget in self.result_content.winfo_children():
                widget.destroy()
            
            status_icon = tk.Label(self.result_content, text=result['icon'], 
                                   font=('Segoe UI', 48), bg='white', fg=result['color'])
            status_icon.pack(pady=(0, 10))
            
            status_label = tk.Label(self.result_content, text=result['status'],
                                    font=('Segoe UI', 14, 'bold'), bg='white', fg=result['color'])
            status_label.pack(pady=5)
            
            confidence_label = tk.Label(self.result_content, text=result['confidence'],
                                        font=('Segoe UI', 12), bg='white', fg=COLORS['gray'])
            confidence_label.pack(pady=5)
            
            rec_label = tk.Label(self.result_content, text=result['recommendation'],
                                 font=('Segoe UI', 10), bg='white', fg=COLORS['dark'],
                                 wraplength=280, justify='center')
            rec_label.pack(pady=10)
            
            self.update_analytics()
            self.status_var.set(f"✅ Prediction complete: {result['status'][:50]}")
            
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
    
    def clear_manual_inputs(self):
        """Clear all manual input fields"""
        for entry in self.input_entries.values():
            entry.delete(0, tk.END)
        self.status_var.set("Input fields cleared")
        
        for widget in self.result_content.winfo_children():
            widget.destroy()
        
        ready_label = tk.Label(self.result_content, text="Ready to analyze...",
                               font=('Segoe UI', 12), bg='white', fg=COLORS['gray'],
                               wraplength=280, justify='center')
        ready_label.pack(expand=True)
    
    def browse_csv(self):
        """Open file dialog"""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def predict_batch(self):
        """Make batch predictions with current threshold"""
        if not self.model_loaded or self.csv_handler is None:
            messagebox.showwarning("Not Ready", "Model still loading. Please wait.")
            return
        
        filepath = self.file_path_var.get()
        if not filepath:
            messagebox.showwarning("No File", "Please select a CSV file first.")
            return
        
        # Use batch threshold for predictions
        if hasattr(self, 'batch_threshold_var'):
            batch_threshold = self.batch_threshold_var.get()
        else:
            batch_threshold = 0.8
        
        self.status_var.set("🔄 Processing CSV file...")
        
        df, error = self.csv_handler.load_csv(filepath)
        if error:
            messagebox.showerror("CSV Error", error)
            self.status_var.set("CSV processing failed")
            return
        
        errors = self.csv_handler.validate_values(df)
        if errors:
            messagebox.showerror("Data Error", "\n".join(errors))
            return
        
        try:
            # Get probabilities from model
            X = df[self.feature_names].values.astype(float)
            probabilities = self.model_loader.model.predict_proba(X)[:, 1]
            
            # Apply batch threshold
            predictions = (probabilities >= batch_threshold).astype(int)
            
            for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
                patient_id = f"Batch_{len(self.analytics_data['predictions']) + i + 1}"
                self.analytics_data['predictions'].append(pred)
                self.analytics_data['probabilities'].append(prob)
                self.analytics_data['patient_ids'].append(patient_id)
                self.analytics_data['source'].append('batch')
            
            self.batch_results_data = df
            self.batch_predictions = predictions
            self.batch_probabilities = probabilities
            
            self.batch_result_text.delete(1.0, tk.END)
            self.batch_result_text.insert(tk.END, "="*70 + "\n")
            self.batch_result_text.insert(tk.END, f"📊 BATCH PREDICTION RESULTS (Threshold: {batch_threshold:.2f})\n")
            self.batch_result_text.insert(tk.END, "="*70 + "\n\n")
            
            parkinsons_count = 0
            for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
                status = "⚠️ PARKINSON'S" if pred == 1 else "✅ HEALTHY"
                confidence = prob if pred == 1 else 1 - prob
                if pred == 1:
                    parkinsons_count += 1
                self.batch_result_text.insert(tk.END, f"Patient {i+1}: {status} (Confidence: {confidence:.1%})\n")
            
            self.batch_result_text.insert(tk.END, "\n" + "="*70 + "\n")
            self.batch_result_text.insert(tk.END, f"📈 SUMMARY\n")
            self.batch_result_text.insert(tk.END, f"   Total Patients: {len(predictions)}\n")
            self.batch_result_text.insert(tk.END, f"   Parkinson's Detected: {parkinsons_count}\n")
            self.batch_result_text.insert(tk.END, f"   Healthy: {len(predictions) - parkinsons_count}\n")
            self.batch_result_text.insert(tk.END, f"   Threshold Used: {batch_threshold:.2f}\n")
            self.batch_result_text.insert(tk.END, "="*70 + "\n")
            
            self.export_btn.config(state='normal')
            self.status_var.set(f"✅ Batch complete. {len(predictions)} patients processed.")
            self.update_analytics()
            
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
            self.status_var.set("Batch prediction failed")
    
    def export_results(self):
        """Export results"""
        if self.batch_results_data is None:
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="predictions_results.csv"
        )
        
        if filepath:
            try:
                results = self.batch_results_data.copy()
                results['Prediction'] = ['Parkinson\'s' if p == 1 else 'Healthy' for p in self.batch_predictions]
                results['Probability_Parkinsons'] = self.batch_probabilities
                results.to_csv(filepath, index=False)
                messagebox.showinfo("Export Successful", f"Results saved to:\n{filepath}")
                self.status_var.set(f"✅ Results exported to {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def update_analytics(self):
        """Update analytics tab"""
        for widget in self.analytics_canvas_frame.winfo_children():
            widget.destroy()
        
        if len(self.analytics_data['predictions']) == 0:
            placeholder = tk.Label(self.analytics_canvas_frame, 
                                   text="No data available. Make predictions first.",
                                   font=('Segoe UI', 12), bg=COLORS['background'], 
                                   fg=COLORS['gray'], justify='center')
            placeholder.pack(expand=True)
            return
        
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
        
        predictions = self.analytics_data['predictions']
        parkinsons = sum(predictions)
        healthy = len(predictions) - parkinsons
        
        labels = ['Parkinson\'s', 'Healthy']
        sizes = [parkinsons, healthy]
        colors = ['#e74c3c', '#4caf50']
        
        bars = ax.bar(labels, sizes, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Count', fontsize=11)
        ax.set_title('Prediction Distribution', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, sizes):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
                   str(val), ha='center', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.analytics_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    app = NeuroDetectApp()
    app.run()


if __name__ == "__main__":
    main()