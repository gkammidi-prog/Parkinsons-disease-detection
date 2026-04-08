"""
Professional Homepage with Modern UI Design - Working Version
"""
import tkinter as tk
from .styles import get_primary_button_style, get_secondary_button_style
from .config import COLORS


class Homepage:
    """Professional Homepage with Working Layout"""
    
    def __init__(self, parent, on_login, on_register):
        self.parent = parent
        self.on_login = on_login
        self.on_register = on_register
        
        self._create_ui()
    
    def _create_ui(self):
        """Create modern homepage UI"""
        
        # Header
        header = tk.Frame(self.parent, bg=COLORS['primary'], height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧠 NeuroDetect Pro", 
                font=('Segoe UI', 28, 'bold'), 
                fg='white', bg=COLORS['primary']).pack(pady=20)
        
        tk.Label(header, text="AI-Powered Early Detection System for Parkinson's Disease",
                font=('Segoe UI', 10), fg='#e0e0e0', bg=COLORS['primary']).pack()
        
        # Main scrollable area with proper canvas configuration
        canvas = tk.Canvas(self.parent, bg=COLORS['background'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # IMPORTANT: Create window with proper anchoring
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Bind canvas resize to update window width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Content - use fill=tk.X to ensure content expands horizontally
        self._create_content(scrollable_frame)
    
    def _create_content(self, parent):
        """Create all content"""
        
        # Main container - NO FIXED WIDTH, let it expand
        main_container = tk.Frame(parent, bg=COLORS['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ========== HERO SECTION ==========
        hero_frame = tk.Frame(main_container, bg='white', relief='flat', bd=1,
                              highlightbackground=COLORS['border'], highlightthickness=1)
        hero_frame.pack(fill=tk.X, pady=10)
        
        hero_content = tk.Frame(hero_frame, bg='white')
        hero_content.pack(pady=25, padx=20)
        
        tk.Label(hero_content, text="Early Detection Saves Lives", 
                font=('Segoe UI', 26, 'bold'), 
                bg='white', fg=COLORS['primary']).pack()
        
        tk.Label(hero_content, 
                text="NeuroDetect Pro uses advanced machine learning to analyze voice patterns\n"
                     "and detect early signs of Parkinson's disease with exceptional accuracy.",
                font=('Segoe UI', 11), bg='white', fg=COLORS['gray'], justify='center').pack(pady=(8, 20))
        
        # Buttons
        btn_frame = tk.Frame(hero_content, bg='white')
        btn_frame.pack()
        
        tk.Button(btn_frame, text="🔐 LOGIN", command=self.on_login,
                 bg=COLORS['primary'], fg='white', font=('Segoe UI', 11, 'bold'),
                 padx=35, pady=8, cursor='hand2', relief='flat').pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="📝 REGISTER", command=self.on_register,
                 bg='white', fg=COLORS['primary'], font=('Segoe UI', 11, 'bold'),
                 padx=35, pady=8, cursor='hand2', relief='solid', bd=1).pack(side=tk.LEFT, padx=10)
        
        tk.Label(hero_content, text="New user? Create an account to get started!",
                font=('Segoe UI', 10), bg='white', fg=COLORS['gray']).pack(pady=(12, 0))
        
        # ========== STATS SECTION ==========
        stats_frame = tk.Frame(main_container, bg=COLORS['background'])
        stats_frame.pack(fill=tk.X, pady=12)
        
        stats = [
            ("🎯", "81.97%", "Accuracy", COLORS['success']),
            ("🩺", "97.96%", "Sensitivity", COLORS['info']),
            ("📊", "22", "Features", COLORS['secondary']),
            ("⚡", "< 1 sec", "Response", COLORS['warning'])
        ]
        
        for icon, value, label, color in stats:
            card = tk.Frame(stats_frame, bg='white', relief='flat', bd=1,
                           highlightbackground=COLORS['border'], highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
            
            tk.Label(card, text=icon, font=('Segoe UI', 28), 
                    bg='white', fg=color).pack(pady=(8, 0))
            tk.Label(card, text=value, font=('Segoe UI', 20, 'bold'),
                    bg='white', fg=color).pack()
            tk.Label(card, text=label, font=('Segoe UI', 10),
                    bg='white', fg=COLORS['gray']).pack(pady=(0, 6))
        
        # ========== FEATURES TITLE ==========
        tk.Label(main_container, text="Key Features", 
                font=('Segoe UI', 22, 'bold'), 
                bg=COLORS['background'], fg=COLORS['primary']).pack(pady=(12, 8))
        
        # ========== FEATURES GRID ==========
        features_container = tk.Frame(main_container, bg=COLORS['background'])
        features_container.pack(fill=tk.X)
        
        features = [
            ("🎙️", "Voice Analysis", "22 voice biomarkers analyzed"),
            ("📊", "Batch Processing", "CSV file upload support"),
            ("📈", "Analytics", "Interactive visualizations"),
            ("🔒", "Secure Login", "Personalized accounts"),
            ("📋", "Export Reports", "CSV export capability"),
            ("🤖", "AI Powered", "CatBoost machine learning")
        ]
        
        # 2 rows of 3 columns
        for row_idx in range(2):
            row = tk.Frame(features_container, bg=COLORS['background'])
            row.pack(pady=5)
            
            for col_idx in range(3):
                idx = row_idx * 3 + col_idx
                if idx < len(features):
                    icon, title, desc = features[idx]
                    card = tk.Frame(row, bg='white', relief='flat', bd=1,
                                   highlightbackground=COLORS['border'], highlightthickness=1)
                    card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
                    
                    tk.Label(card, text=icon, font=('Segoe UI', 28), 
                            bg='white', fg=COLORS['primary']).pack(pady=(8, 2))
                    tk.Label(card, text=title, font=('Segoe UI', 11, 'bold'),
                            bg='white', fg=COLORS['dark']).pack()
                    tk.Label(card, text=desc, font=('Segoe UI', 9),
                            bg='white', fg=COLORS['gray']).pack(pady=(0, 6))
        
        # ========== HOW IT WORKS ==========
        howto_frame = tk.Frame(main_container, bg='#f8f9fa', relief='flat', bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        howto_frame.pack(fill=tk.X, pady=12)
        
        tk.Label(howto_frame, text="How It Works", 
                font=('Segoe UI', 20, 'bold'), bg='#f8f9fa', fg=COLORS['primary']).pack(pady=(12, 8))
        
        steps_frame = tk.Frame(howto_frame, bg='#f8f9fa')
        steps_frame.pack(pady=8, padx=10)
        
        steps = [
            ("1", "Input Data", "Enter 22 voice measurements"),
            ("2", "AI Analysis", "CatBoost model processes"),
            ("3", "Get Result", "Prediction with confidence"),
            ("4", "Export", "Save results to CSV")
        ]
        
        for num, title, desc in steps:
            card = tk.Frame(steps_frame, bg='white', relief='flat', bd=1,
                           highlightbackground=COLORS['border'], highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
            
            tk.Label(card, text=num, font=('Segoe UI', 22, 'bold'),
                    bg='white', fg=COLORS['primary']).pack(pady=(6, 0))
            tk.Label(card, text=title, font=('Segoe UI', 10, 'bold'),
                    bg='white', fg=COLORS['dark']).pack()
            tk.Label(card, text=desc, font=('Segoe UI', 8),
                    bg='white', fg=COLORS['gray']).pack(pady=(0, 5))
        
        tk.Frame(howto_frame, height=8, bg='#f8f9fa').pack()
        
        # ========== TECHNICAL SPECS ==========
        tech_frame = tk.Frame(main_container, bg='white', relief='flat', bd=1,
                              highlightbackground=COLORS['border'], highlightthickness=1)
        tech_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(tech_frame, text="Technical Specifications", 
                font=('Segoe UI', 18, 'bold'), bg='white', fg=COLORS['primary']).pack(pady=(10, 6))
        
        specs_container = tk.Frame(tech_frame, bg='white')
        specs_container.pack(pady=5, padx=15)
        
        specs = [
            ("Model:", "CatBoost Classifier"),
            ("Features:", "22 voice biomarkers"),
            ("Training Data:", "UCI Parkinson's Dataset"),
            ("Accuracy:", "81.97%"),
            ("Sensitivity:", "97.96%"),
            ("Response Time:", "< 1 second")
        ]
        
        for i in range(0, len(specs), 2):
            row = tk.Frame(specs_container, bg='white')
            row.pack(fill=tk.X, pady=2)
            
            for j in range(2):
                idx = i + j
                if idx < len(specs):
                    label, value = specs[idx]
                    col = tk.Frame(row, bg='white')
                    col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    
                    tk.Label(col, text=label, font=('Segoe UI', 9, 'bold'),
                            bg='white', fg=COLORS['dark']).pack(side=tk.LEFT)
                    tk.Label(col, text=value, font=('Segoe UI', 9),
                            bg='white', fg=COLORS['gray']).pack(side=tk.LEFT, padx=(5, 0))
        
        tk.Frame(tech_frame, height=6, bg='white').pack()
        
        # ========== IMPORTANT NOTICE ==========
        notice_frame = tk.Frame(main_container, bg='#fff8e7', relief='flat', bd=1,
                                highlightbackground=COLORS['warning'], highlightthickness=1)
        notice_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(notice_frame, text="⚠️ Important Medical Notice", 
                font=('Segoe UI', 11, 'bold'), bg='#fff8e7', fg=COLORS['warning']).pack(pady=(6, 2))
        
        tk.Label(notice_frame, 
                text="This tool is for screening purposes only. Always consult a healthcare professional for diagnosis.",
                font=('Segoe UI', 9), bg='#fff8e7', fg=COLORS['dark']).pack(pady=(0, 6))
        
        # Bottom spacing
        tk.Frame(main_container, height=10, bg=COLORS['background']).pack()