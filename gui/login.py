"""
Modern Login & Registration System - With Homepage Navigation
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
from datetime import datetime
from .styles import get_primary_button_style, get_secondary_button_style, get_card_style
from .config import COLORS


class LoginSystem:
    """Login and Registration System"""
    
    def __init__(self, parent, on_login_success, on_back, show_register=False):
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_back = on_back
        self.show_register = show_register
        
        # Clear parent window
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.users_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')
        self._init_users_file()
        self._create_ui()
    
    def _init_users_file(self):
        """Initialize users file if not exists"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f, indent=4)
    
    def _create_ui(self):
        """Create login UI"""
        
        # Header with back button
        header = tk.Frame(self.parent, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        back_btn = tk.Button(header, text="← Back", command=self.on_back,
                             bg=COLORS['primary'], fg='white', font=('Segoe UI', 10),
                             relief='flat', cursor='hand2')
        back_btn.pack(side=tk.LEFT, padx=20, pady=25)
        
        tk.Label(header, text="NeuroDetect Pro", 
                font=('Segoe UI', 20, 'bold'), 
                fg='white', bg=COLORS['primary']).pack(side=tk.LEFT, padx=10)
        
        # Main Card
        card = tk.Frame(self.parent, bg='white', relief='flat', bd=1,
                        highlightbackground=COLORS['border'], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Tabs
        tab_control = ttk.Notebook(card)
        tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Login Tab
        login_tab = tk.Frame(tab_control, bg='white')
        tab_control.add(login_tab, text="🔐 Login")
        
        # Register Tab
        register_tab = tk.Frame(tab_control, bg='white')
        tab_control.add(register_tab, text="📝 Register")
        
        self._create_login_tab(login_tab)
        self._create_register_tab(register_tab)
        
        # Select appropriate tab
        if self.show_register:
            tab_control.select(1)
        
        # Footer
        footer = tk.Frame(self.parent, bg=COLORS['light'], height=35)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text="© 2024 NeuroDetect Pro",
                font=('Segoe UI', 8), bg=COLORS['light'], fg=COLORS['gray']).pack(pady=8)
    
    def _create_login_tab(self, parent):
        """Create login form"""
        
        tk.Label(parent, text="Welcome Back", 
                font=('Segoe UI', 20, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(pady=(30, 5))
        
        tk.Label(parent, text="Sign in to access your dashboard",
                font=('Segoe UI', 10), bg='white', fg=COLORS['gray']).pack(pady=(0, 30))
        
        # Username
        tk.Label(parent, text="Username", font=('Segoe UI', 11, 'bold'),
                bg='white', fg=COLORS['dark']).pack(anchor='w', padx=40, pady=(0, 5))
        
        self.username_entry = tk.Entry(parent, font=('Segoe UI', 11), 
                                        bg=COLORS['light'], relief='flat', bd=1)
        self.username_entry.pack(fill=tk.X, padx=40, pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(parent, text="Password", font=('Segoe UI', 11, 'bold'),
                bg='white', fg=COLORS['dark']).pack(anchor='w', padx=40, pady=(0, 5))
        
        self.password_entry = tk.Entry(parent, show="•", font=('Segoe UI', 11),
                                        bg=COLORS['light'], relief='flat', bd=1)
        self.password_entry.pack(fill=tk.X, padx=40, pady=(0, 20), ipady=8)
        
        # Login Button
        login_btn = tk.Button(parent, text="SIGN IN", command=self._handle_login,
                              **get_primary_button_style())
        login_btn.pack(pady=15)
        
        # Demo hint
        tk.Label(parent, text="No account? Register above to create one.",
                font=('Segoe UI', 8), bg='white', fg=COLORS['gray']).pack(pady=10)
        
        self.password_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _create_register_tab(self, parent):
        """Create scrollable registration form"""
        
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        tk.Label(scrollable_frame, text="Create Account", 
                font=('Segoe UI', 20, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(pady=(20, 5))
        
        tk.Label(scrollable_frame, text="Join NeuroDetect Pro today",
                font=('Segoe UI', 10), bg='white', fg=COLORS['gray']).pack(pady=(0, 20))
        
        # Form fields
        form_frame = tk.Frame(scrollable_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        fields = [
            ("Full Name", "reg_name"),
            ("Email", "reg_email"),
            ("Username", "reg_username"),
            ("Password", "reg_password", True),
            ("Confirm Password", "reg_confirm", True)
        ]
        
        for field in fields:
            label = field[0]
            attr = field[1]
            show = field[2] if len(field) > 2 else False
            
            tk.Label(form_frame, text=label, font=('Segoe UI', 11, 'bold'),
                    bg='white', fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
            entry = tk.Entry(form_frame, font=('Segoe UI', 11), bg=COLORS['light'], relief='flat', bd=1)
            if show:
                entry.config(show="•")
            entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
            setattr(self, attr, entry)
        
        # Role
        tk.Label(form_frame, text="Role", font=('Segoe UI', 11, 'bold'),
                bg='white', fg=COLORS['dark']).pack(anchor='w', pady=(0, 5))
        self.reg_role = ttk.Combobox(form_frame, values=['Doctor', 'Researcher', 'Student'],
                                      font=('Segoe UI', 11), state='readonly')
        self.reg_role.set('Doctor')
        self.reg_role.pack(fill=tk.X, pady=(0, 20), ipady=5)
        
        # Register Button
        register_btn = tk.Button(form_frame, text="CREATE ACCOUNT", command=self._handle_register,
                                  **get_secondary_button_style())
        register_btn.pack(pady=(5, 20))
        
        tk.Label(form_frame, text="Already have an account? Login above.",
                font=('Segoe UI', 9), bg='white', fg=COLORS['gray']).pack(pady=(0, 10))
    
    def _handle_login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except:
            users = {}
        
        if username in users:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            if users[username]['password'] == hashed:
                messagebox.showinfo("Success", f"Welcome back, {users[username]['name']}!")
                self.on_login_success(username, users[username])
                return
        
        messagebox.showerror("Error", "Invalid username or password")
    
    def _handle_register(self):
        """Handle registration"""
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        role = self.reg_role.get()
        
        if not all([name, email, username, password]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except:
            users = {}
        
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        users[username] = {
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "email": email,
            "name": name,
            "role": role.lower(),
            "created_at": datetime.now().isoformat()
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
        
        messagebox.showinfo("Success", "Account created successfully! Please login.")
        
        # Clear fields
        self.reg_name.delete(0, tk.END)
        self.reg_email.delete(0, tk.END)
        self.reg_username.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)
        self.reg_confirm.delete(0, tk.END)
        self.reg_role.set('Doctor')
    
    def run(self):
        pass