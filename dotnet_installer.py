import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys
from datetime import datetime

class DotNetInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(".NET Web Library 2.0")
        
        # Plik konfiguracyjny z rozmiarami okien
        self.config_file = "windows_config.txt"
        
        # Plik logu
        self.log_file = "installation_log.txt"
        
        # Słownik do przechowywania konfiguracji okien
        self.window_configs = {}
        
        # Słownik do przechowywania output widgets dla każdej zakładki
        self.output_widgets = {}
        
        # Wczytaj konfiguracje wszystkich okien
        self.load_all_window_configs()
        
        # Wczytaj rozmiar głównego okna
        window_size = self.window_configs.get('main_window', '700x600')
        self.root.geometry(window_size)
        self.root.resizable(False, False)  # Pozwól na zmianę rozmiaru
        
        # Ustaw minimalny rozmiar okna
        self.root.minsize(700, 600)
        
        # Ustawienia języka
        self.current_language = "EN"
        self.translations = {
            "EN": {
                "title": ".NET Web Library\nInstaller and Updater",
                "version": "ver. 2.0 | by Sebastian Januchowski | polsoft.ITS",
                "additional_options": "Additional Options:",
                "microsoft_net": "🌐 Microsoft .NET",
                "powershell_script": "PowerShell Script",
                "bash_script": "Bash Script",
                "about": "ℹ️ About",
                "help": "📖 Help",
                "language": "🌐 Language: EN",
                "status_ready": "Ready",
                "status_installing": "Installing",
                "status_success": "Successfully installed",
                "status_error": "Error installing",
                "select_package": "Select a package to install or update",
                "install_update": "Install/Update",
                "about_title": "About",
                "about_created": "Created by:",
                "about_contact": "Contact:",
                "about_description": "A powerful tool for managing .NET Runtime\ninstallations across multiple versions.\nBuilt with Python and Tkinter.",
                "about_close": "Close",
                "help_not_found": "Help File Not Found",
                "help_not_found_msg": "Help.html file not found at:\n{path}\n\nPlease make sure Help.html is in the same folder as the application.",
                "error": "Error",
                "error_help": "Could not open help file:\n{error}",
                "success": "Success",
                "success_msg": "{package} has been installed/updated successfully!",
                "error_msg": "Failed to install {package}\n\n{error}",
                "error_occurred": "An error occurred:\n{error}"
            },
            "PL": {
                "title": ".NET Web Library\nInstalator i Aktualizator",
                "version": "wer. 2.0 | autor: Sebastian Januchowski | polsoft.ITS",
                "additional_options": "Dodatkowe Opcje:",
                "microsoft_net": "🌐 Microsoft .NET",
                "powershell_script": "Skrypt PowerShell",
                "bash_script": "Skrypt Bash",
                "about": "ℹ️ O programie",
                "help": "📖 Pomoc",
                "language": "🌐 Język: PL",
                "status_ready": "Gotowy",
                "status_installing": "Instalowanie",
                "status_success": "Pomyślnie zainstalowano",
                "status_error": "Błąd instalacji",
                "select_package": "Wybierz pakiet do zainstalowania lub aktualizacji",
                "install_update": "Instaluj/Aktualizuj",
                "about_title": "O programie",
                "about_created": "Stworzony przez:",
                "about_contact": "Kontakt:",
                "about_description": "Potężne narzędzie do zarządzania instalacjami\n.NET Runtime w wielu wersjach.\nStworzone w Python i Tkinter.",
                "about_close": "Zamknij",
                "help_not_found": "Nie znaleziono pliku pomocy",
                "help_not_found_msg": "Plik Help.html nie został znaleziony w:\n{path}\n\nUpewnij się, że Help.html znajduje się w tym samym folderze co aplikacja.",
                "error": "Błąd",
                "error_help": "Nie można otworzyć pliku pomocy:\n{error}",
                "success": "Sukces",
                "success_msg": "{package} został pomyślnie zainstalowany/zaktualizowany!",
                "error_msg": "Nie udało się zainstalować {package}\n\n{error}",
                "error_occurred": "Wystąpił błąd:\n{error}"
            }
        }
        
        # Ustaw ikonę
        self.set_icon()
        
        # Kolory
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#0078d4"
        self.button_color = "#3c3c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Loguj start aplikacji
        self.log_to_file("Application started", "INFO")
        self.log_to_file(f"Main window size: {window_size}", "INFO")
        
        self.create_widgets()
        
        # Zapisuj rozmiar okna przy zmianie
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Zapisuj rozmiar okna przy zamykaniu
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def set_icon(self):
        """Ustaw ikonę okna aplikacji"""
        try:
            # Ścieżka do ikony
            if getattr(sys, 'frozen', False):
                # Jeśli aplikacja jest skompilowana (exe)
                application_path = sys._MEIPASS
            else:
                # Jeśli uruchamiana jako skrypt
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, 'icon.ico')
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"Icon file not found at: {icon_path}")
        except Exception as e:
            print(f"Error setting icon: {e}")
    
    def load_all_window_configs(self):
        """Wczytaj konfiguracje wszystkich okien z pliku"""
        try:
            # Ścieżka do pliku konfiguracyjnego
            if getattr(sys, 'frozen', False):
                config_dir = os.path.dirname(sys.executable)
            else:
                config_dir = os.path.dirname(os.path.abspath(__file__))
            
            config_path = os.path.join(config_dir, self.config_file)
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            self.window_configs[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error loading window configs: {e}")
        
        # Ustaw domyślne wartości jeśli nie ma w pliku
        if 'main_window' not in self.window_configs:
            self.window_configs['main_window'] = '850x600'
        if 'about_window' not in self.window_configs:
            self.window_configs['about_window'] = '400x541'
    
    def save_all_window_configs(self):
        """Zapisz konfiguracje wszystkich okien do pliku"""
        try:
            # Ścieżka do pliku konfiguracyjnego
            if getattr(sys, 'frozen', False):
                config_dir = os.path.dirname(sys.executable)
            else:
                config_dir = os.path.dirname(os.path.abspath(__file__))
            
            config_path = os.path.join(config_dir, self.config_file)
            
            # Zapisz wszystkie konfiguracje
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write("# .NET Web Library 2.0 - Window Configurations\n")
                f.write("# Format: window_name=widthxheight+x+y (or widthxheight)\n")
                f.write("# Auto-generated - modifications will be preserved\n\n")
                
                for key, value in sorted(self.window_configs.items()):
                    f.write(f"{key}={value}\n")
        except Exception as e:
            print(f"Error saving window configs: {e}")
    
    def save_window_size(self, window_name='main_window'):
        """Zapisz rozmiar i pozycję okna do konfiguracji"""
        try:
            if window_name == 'main_window':
                # Pobierz pełną geometrię okna (rozmiar + pozycja)
                geometry = self.root.winfo_geometry()
                # Format: WIDTHxHEIGHT+X+Y
                self.log_to_file(f"Main window size saved: {geometry}", "INFO")
            else:
                # Dla innych okien - nie zapisujemy tutaj
                return
            
            # Zaktualizuj konfigurację
            self.window_configs[window_name] = geometry
            
            # Zapisz wszystkie konfiguracje
            self.save_all_window_configs()
        except Exception as e:
            print(f"Error saving window size: {e}")
            self.log_to_file(f"Error saving window size: {e}", "ERROR")
    
    def on_window_resize(self, event):
        """Obsługa zdarzenia zmiany rozmiaru okna"""
        # Zapisuj tylko gdy zmiana dotyczy głównego okna
        if event.widget == self.root:
            # Użyj after(), aby uniknąć zbyt częstego zapisywania
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(500, lambda: self.save_window_size('main_window'))
    
    def on_closing(self):
        """Obsługa zamykania okna"""
        self.save_window_size('main_window')
        self.log_to_file("Application closed", "INFO")
        self.log_to_file("=" * 50, "INFO")  # Separator dla kolejnej sesji
        self.root.destroy()
    
    def create_widgets(self):
        # Header
        self.header_frame = tk.Frame(self.root, bg=self.bg_color)
        self.header_frame.pack(pady=20)
        
        self.title_label = tk.Label(
            self.header_frame,
            text=self.translations[self.current_language]["title"],
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.title_label.pack()
        
        self.version_label = tk.Label(
            self.header_frame,
            text=self.translations[self.current_language]["version"],
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#888888"
        )
        self.version_label.pack(pady=5)
        
        # Notebook (zakładki)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Style dla zakładek
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Zakładki dla różnych wersji
        self.create_version_tab(".NET 3.1", [
            ("Runtime", "Microsoft.DotNet.Runtime.3_1"),
            ("SDK", "Microsoft.DotNet.SDK.3_1"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.3_1"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.3_1")
        ])
        
        self.create_version_tab(".NET 5.0", [
            ("Runtime", "Microsoft.DotNet.Runtime.5"),
            ("SDK", "Microsoft.DotNet.SDK.5"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.5"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.5")
        ])
        
        self.create_version_tab(".NET 6.0", [
            ("Runtime", "Microsoft.DotNet.Runtime.6"),
            ("SDK", "Microsoft.DotNet.SDK.6"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.6"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.6")
        ])
        
        self.create_version_tab(".NET 7.0", [
            ("Runtime", "Microsoft.DotNet.Runtime.7"),
            ("SDK", "Microsoft.DotNet.SDK.7"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.7"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.7")
        ])
        
        self.create_version_tab(".NET 8.0", [
            ("Runtime", "Microsoft.DotNet.Runtime.8"),
            ("SDK", "Microsoft.DotNet.SDK.8"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.8"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.8")
        ])
        
        self.create_version_tab(".NET 9.0", [
            ("Runtime", "Microsoft.DotNet.Runtime.9"),
            ("SDK", "Microsoft.DotNet.SDK.9"),
            ("Desktop Runtime", "Microsoft.DotNet.DesktopRuntime.9"),
            ("ASP.NET Core Runtime", "Microsoft.DotNet.AspNetCore.9")
        ])
        
        self.create_version_tab(".NET 10.0 Preview", [
            ("Runtime Preview", "Microsoft.DotNet.Runtime.Preview"),
            ("SDK Preview", "Microsoft.DotNet.SDK.Preview"),
            ("Desktop Runtime Preview", "Microsoft.DotNet.DesktopRuntime.Preview"),
            ("ASP.NET Core Runtime Preview", "Microsoft.DotNet.AspNetCore.Preview")
        ])
        
        # Dodatkowe opcje
        self.extras_frame = tk.Frame(self.root, bg=self.bg_color)
        self.extras_frame.pack(pady=10, padx=20, fill='x')
        
        self.options_label = tk.Label(
            self.extras_frame,
            text=self.translations[self.current_language]["additional_options"],
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.options_label.pack(anchor='w', pady=5)
        
        self.button_frame = tk.Frame(self.extras_frame, bg=self.bg_color)
        self.button_frame.pack(fill='x')
        
        self.lang_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["language"],
            self.toggle_language
        )
        self.lang_btn.pack(side='left', padx=5)
        
        self.net_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["microsoft_net"],
            lambda: subprocess.run(["start", "https://dotnet.microsoft.com/en-us/"], shell=True)
        )
        self.net_btn.pack(side='left', padx=5)
        
        self.ps_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["powershell_script"],
            lambda: subprocess.run(["start", "https://builds.dotnet.microsoft.com/dotnet/scripts/v1/dotnet-install.ps1"], shell=True)
        )
        self.ps_btn.pack(side='left', padx=5)
        
        self.bash_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["bash_script"],
            lambda: subprocess.run(["start", "https://builds.dotnet.microsoft.com/dotnet/scripts/v1/dotnet-install.sh"], shell=True)
        )
        self.bash_btn.pack(side='left', padx=5)
        
        self.about_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["about"],
            self.show_about
        )
        self.about_btn.pack(side='left', padx=5)
        
        self.help_btn = self.create_extra_button(
            self.button_frame,
            self.translations[self.current_language]["help"],
            self.show_help
        )
        self.help_btn.pack(side='left', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value=self.translations[self.current_language]["status_ready"])
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w',
            bg=self.button_color,
            fg=self.fg_color,
            font=("Arial", 9)
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def create_version_tab(self, version_name, packages):
        tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(tab, text=version_name)
        
        # Instrukcje
        info_label = tk.Label(
            tab,
            text=f"{self.translations[self.current_language]['select_package']} {version_name}:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            name=f"info_{version_name.replace(' ', '_').replace('.', '_')}"
        )
        info_label.pack(pady=15)
        
        # Ramka dla kompaktowych przycisków (wszystkie w jednej linii)
        buttons_container = tk.Frame(tab, bg=self.bg_color)
        buttons_container.pack(pady=5, padx=10)
        
        # Przyciski dla każdego pakietu - kompaktowe, w jednej linii
        for package_name, package_id in packages:
            btn = tk.Button(
                buttons_container,
                text=f"{package_name}",  # Tylko nazwa bez "Install/Update"
                command=lambda pid=package_id, pname=package_name: self.install_package(pid, pname),
                bg=self.accent_color,
                fg=self.fg_color,
                font=("Arial", 9, "bold"),
                width=18,
                height=1,
                relief=tk.FLAT,
                cursor="hand2",
                name=f"btn_{package_id.replace('.', '_')}"
            )
            btn.pack(side='left', padx=3, pady=5)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#005a9e"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.accent_color))
        
        # Output window - bezpośrednio pod przyciskami w tej zakładce
        # Mniejszy w pionie (połowa poprzedniego), wyrównany z przyciskami
        output_frame = tk.Frame(tab, bg=self.bg_color)
        output_frame.pack(fill='x', expand=False, padx=10, pady=10)
        
        # Nagłówek output
        output_header = tk.Frame(output_frame, bg=self.bg_color)
        output_header.pack(fill='x', pady=(0, 5))
        
        output_label = tk.Label(
            output_header,
            text="Installation Output:",
            font=("Arial", 9, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor='w'
        )
        output_label.pack(side='left')
        
        # Ramka dla output text - stały rozmiar w pionie
        text_container = tk.Frame(output_frame, bg=self.bg_color, height=120)
        text_container.pack(fill='x', expand=False)
        text_container.pack_propagate(False)  # Wymusza stały rozmiar
        
        # Scrollbar dla output
        output_scroll = tk.Scrollbar(text_container)
        output_scroll.pack(side='right', fill='y')
        
        # Text widget dla output - stała wysokość (ok. 4-5 wierszy)
        output_text = tk.Text(
            text_container,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Consolas", 9),
            relief=tk.SUNKEN,
            borderwidth=2,
            wrap=tk.WORD,
            yscrollcommand=output_scroll.set,
            state='disabled',
            height=5  # 5 wierszy zamiast rozciągliwego
        )
        output_text.pack(side='left', fill='both', expand=True)
        output_scroll.config(command=output_text.yview)
        
        # Zapisz widget output dla tej zakładki
        tab_id = version_name.replace(' ', '_').replace('.', '_')
        self.output_widgets[tab_id] = output_text
    
    def create_extra_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.button_color,
            fg=self.fg_color,
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn.bind("<Enter>", lambda e: btn.config(bg="#4c4c4c"))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.button_color))
        return btn
    
    def toggle_language(self):
        """Przełącz język między EN i PL"""
        # Zmień język
        old_language = self.current_language
        self.current_language = "PL" if self.current_language == "EN" else "EN"
        self.log_to_file(f"Language changed from {old_language} to {self.current_language}", "INFO")
        
        # Aktualizuj wszystkie teksty
        self.title_label.config(text=self.translations[self.current_language]["title"])
        self.version_label.config(text=self.translations[self.current_language]["version"])
        self.options_label.config(text=self.translations[self.current_language]["additional_options"])
        
        # Aktualizuj przyciski
        self.lang_btn.config(text=self.translations[self.current_language]["language"])
        self.net_btn.config(text=self.translations[self.current_language]["microsoft_net"])
        self.ps_btn.config(text=self.translations[self.current_language]["powershell_script"])
        self.bash_btn.config(text=self.translations[self.current_language]["bash_script"])
        self.about_btn.config(text=self.translations[self.current_language]["about"])
        self.help_btn.config(text=self.translations[self.current_language]["help"])
        
        # Aktualizuj pasek statusu
        current_status = self.status_var.get()
        if "Ready" in current_status or "Gotowy" in current_status:
            self.status_var.set(self.translations[self.current_language]["status_ready"])
        
        # Aktualizuj etykiety i przyciski w zakładkach
        for tab_id in range(self.notebook.index("end")):
            tab = self.notebook.nametowidget(self.notebook.tabs()[tab_id])
            for widget in tab.winfo_children():
                if isinstance(widget, tk.Label):
                    # Zaktualizuj etykiety informacyjne
                    current_text = widget.cget("text")
                    if "Select a package" in current_text or "Wybierz pakiet" in current_text:
                        # Wyciągnij nazwę wersji z obecnego tekstu
                        version = current_text.split(":")[-1].strip()
                        if not version:
                            parts = current_text.split()
                            for i, part in enumerate(parts):
                                if ".NET" in part and i + 1 < len(parts):
                                    version = f"{part} {parts[i+1]}"
                                    break
                        widget.config(text=f"{self.translations[self.current_language]['select_package']} {version}:")
                elif isinstance(widget, tk.Frame):
                    # Przyciski są teraz w ramce - nie zmieniamy ich tekstu
                    # Zawierają tylko nazwy pakietów bez "Install/Update"
                    pass
    
    def show_help(self):
        """Otwórz plik pomocy Help.html"""
        self.log_to_file("Opening Help file", "INFO")
        try:
            # Ścieżka do pliku Help.html
            if getattr(sys, 'frozen', False):
                # Jeśli aplikacja jest skompilowana (exe)
                application_path = sys._MEIPASS
            else:
                # Jeśli uruchamiana jako skrypt
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            help_path = os.path.join(application_path, 'Help.html')
            
            if os.path.exists(help_path):
                subprocess.run(["start", help_path], shell=True)
            else:
                messagebox.showwarning(
                    self.translations[self.current_language]["help_not_found"],
                    self.translations[self.current_language]["help_not_found_msg"].format(path=help_path)
                )
        except Exception as e:
            messagebox.showerror(
                self.translations[self.current_language]["error"],
                self.translations[self.current_language]["error_help"].format(error=str(e))
            )
    
    def show_about(self):
        """Wyświetl okno About z informacjami o autorze"""
        self.log_to_file("Opening About window", "INFO")
        about_window = tk.Toplevel(self.root)
        about_window.title(self.translations[self.current_language]["about_title"])
        
        # Wczytaj zapisany rozmiar lub użyj domyślnego
        about_size = self.window_configs.get('about_window', '500x400')
        about_window.geometry(about_size)
        about_window.resizable(False, False)  # Pozwól na zmianę rozmiaru
        about_window.minsize(400, 350)  # Minimalny rozmiar
        about_window.configure(bg=self.bg_color)
        
        # Centruj okno
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Timer do zapisu rozmiaru
        resize_timer = None
        
        def on_about_resize(event):
            """Zapisz rozmiar okna About po zmianie"""
            nonlocal resize_timer
            if event.widget == about_window:
                if resize_timer:
                    about_window.after_cancel(resize_timer)
                resize_timer = about_window.after(500, lambda: save_about_size(about_window))
        
        def save_about_size(window):
            """Zapisz rozmiar i pozycję okna About"""
            try:
                geometry = window.winfo_geometry()
                self.window_configs['about_window'] = geometry
                self.save_all_window_configs()
                self.log_to_file(f"About window size saved: {geometry}", "INFO")
            except Exception as e:
                print(f"Error saving about window size: {e}")
                self.log_to_file(f"Error saving about window size: {e}", "ERROR")
        
        def on_about_close():
            """Zapisz rozmiar przy zamykaniu"""
            save_about_size(about_window)
            self.log_to_file("About window closed", "INFO")
            about_window.destroy()
        
        # Podepnij obsługę zdarzeń
        about_window.bind("<Configure>", on_about_resize)
        about_window.protocol("WM_DELETE_WINDOW", on_about_close)
        
        # Główny kontener ze scrollbarem dla małych ekranów
        main_frame = tk.Frame(about_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas ze scrollbarem
        canvas = tk.Canvas(main_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        header_frame.pack(pady=20, fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text=self.translations[self.current_language]["title"],
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        version_label = tk.Label(
            header_frame,
            text="Version 2.0",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        version_label.pack(pady=5)
        
        # Separator
        separator = tk.Frame(scrollable_frame, height=2, bg=self.accent_color)
        separator.pack(fill='x', padx=40, pady=10)
        
        # Informacje o autorze
        info_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        info_frame.pack(pady=10)
        
        tk.Label(
            info_frame,
            text=self.translations[self.current_language]["about_created"],
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack()
        
        tk.Label(
            info_frame,
            text="Sebastian Januchowski",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text="polsoft.ITS London",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack()
        
        # Kontakt
        contact_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        contact_frame.pack(pady=15)
        
        tk.Label(
            contact_frame,
            text=self.translations[self.current_language]["about_contact"],
            font=("Arial", 9, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack()
        
        email_label = tk.Label(
            contact_frame,
            text="polsoft.its@fastservice.com",
            font=("Arial", 9, "underline"),
            bg=self.bg_color,
            fg=self.accent_color,
            cursor="hand2"
        )
        email_label.pack()
        email_label.bind("<Button-1>", lambda e: subprocess.run(
            ["start", "mailto:polsoft.its@fastservice.com"], shell=True
        ))
        
        github_label = tk.Label(
            contact_frame,
            text="GitHub: seb07uk",
            font=("Arial", 9, "underline"),
            bg=self.bg_color,
            fg=self.accent_color,
            cursor="hand2"
        )
        github_label.pack(pady=5)
        github_label.bind("<Button-1>", lambda e: subprocess.run(
            ["start", "https://github.com/seb07uk"], shell=True
        ))
        
        # Opis
        desc_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        desc_frame.pack(pady=10, padx=40)
        
        tk.Label(
            desc_frame,
            text=self.translations[self.current_language]["about_description"],
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#888888",
            justify='center'
        ).pack()
        
        # Separator
        separator2 = tk.Frame(scrollable_frame, height=1, bg="#333333")
        separator2.pack(fill='x', padx=40, pady=10)
        
        # Copyright
        tk.Label(
            scrollable_frame,
            text="© 2025 polsoft.ITS™",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#666666"
        ).pack()
        
        # Przycisk Close
        button_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        close_btn = tk.Button(
            button_frame,
            text=self.translations[self.current_language]["about_close"],
            command=on_about_close,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5
        )
        close_btn.pack()
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#6a40ed"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=self.accent_color))
        
        # Pakowanie canvas i scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Włącz scrollowanie myszką
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Usuń binding przy zamykaniu okna
        def cleanup_and_close():
            canvas.unbind_all("<MouseWheel>")
            on_about_close()
        
        about_window.protocol("WM_DELETE_WINDOW", cleanup_and_close)
    
    def get_winget_path(self):
        """Pobierz ścieżkę do winget.exe z katalogu głównego aplikacji"""
        try:
            if getattr(sys, 'frozen', False):
                # Jeśli aplikacja jest skompilowana (exe)
                app_dir = os.path.dirname(sys.executable)
            else:
                # Jeśli uruchamiana jako skrypt
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            winget_path = os.path.join(app_dir, 'winget.exe')
            
            if os.path.exists(winget_path):
                return winget_path
            else:
                # Fallback do systemowego winget jeśli plik nie istnieje
                return "winget"
        except Exception as e:
            print(f"Error getting winget path: {e}")
            return "winget"
    
    def log_to_file(self, message, level="INFO"):
        """Zapisz log do pliku txt"""
        try:
            if getattr(sys, 'frozen', False):
                log_dir = os.path.dirname(sys.executable)
            else:
                log_dir = os.path.dirname(os.path.abspath(__file__))
            
            log_path = os.path.join(log_dir, self.log_file)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level}] {message}\n"
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def update_output(self, message, clear=False):
        """Aktualizuj okno output z przebiegiem instalacji"""
        try:
            # Pobierz aktualną zakładkę
            current_tab_index = self.notebook.index(self.notebook.select())
            tab_name = self.notebook.tab(current_tab_index, "text")
            tab_id = tab_name.replace(' ', '_').replace('.', '_')
            
            # Sprawdź czy output widget istnieje dla tej zakładki
            if tab_id not in self.output_widgets:
                print(f"Output widget not found for tab: {tab_id}")
                return
            
            output_text = self.output_widgets[tab_id]
            output_text.config(state='normal')
            
            if clear:
                output_text.delete(1.0, tk.END)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            output_text.insert(tk.END, f"[{timestamp}] {message}\n")
            output_text.see(tk.END)  # Auto-scroll do końca
            
            output_text.config(state='disabled')
            self.root.update_idletasks()  # Odśwież GUI
        except Exception as e:
            print(f"Error updating output: {e}")
    
    def install_package(self, package_id, package_name):
        self.status_var.set(f"{self.translations[self.current_language]['status_installing']} {package_name}...")
        self.log_to_file(f"Starting installation of {package_name} (ID: {package_id})", "INFO")
        
        # Wyczyść i zaktualizuj okno output
        self.update_output(f"=== Starting installation of {package_name} ===", clear=True)
        self.update_output(f"Package ID: {package_id}")
        
        def run_installation():
            try:
                winget_path = self.get_winget_path()
                self.log_to_file(f"Using winget path: {winget_path}", "INFO")
                self.update_output(f"Using winget: {winget_path}")
                self.update_output("Running winget install command...")
                
                # Uruchom winget z przechwytywaniem output
                process = subprocess.Popen(
                    [winget_path, "install", package_id, "--silent"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Czytaj output w czasie rzeczywistym
                output_lines = []
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        output_lines.append(line)
                        self.update_output(line)
                
                # Czekaj na zakończenie
                process.wait()
                
                # Sprawdź stderr
                stderr_output = process.stderr.read()
                if stderr_output:
                    for line in stderr_output.split('\n'):
                        if line.strip():
                            self.update_output(f"ERROR: {line.strip()}")
                
                if process.returncode == 0:
                    self.status_var.set(f"{self.translations[self.current_language]['status_success']} {package_name}")
                    self.log_to_file(f"Successfully installed {package_name}", "SUCCESS")
                    self.update_output(f"✓ Successfully installed {package_name}")
                    self.update_output("=== Installation completed successfully ===")
                    
                    if output_lines:
                        self.log_to_file(f"Output: {' '.join(output_lines[:10])}", "DEBUG")
                    
                    messagebox.showinfo(
                        self.translations[self.current_language]["success"],
                        self.translations[self.current_language]["success_msg"].format(package=package_name)
                    )
                else:
                    self.status_var.set(f"{self.translations[self.current_language]['status_error']} {package_name}")
                    self.log_to_file(f"Failed to install {package_name}: Return code {process.returncode}", "ERROR")
                    self.update_output(f"✗ Installation failed with return code: {process.returncode}")
                    self.update_output("=== Installation failed ===")
                    
                    error_msg = stderr_output if stderr_output else f"Return code: {process.returncode}"
                    messagebox.showerror(
                        self.translations[self.current_language]["error"],
                        self.translations[self.current_language]["error_msg"].format(package=package_name, error=error_msg)
                    )
            except Exception as e:
                self.status_var.set(self.translations[self.current_language]["status_error"])
                self.log_to_file(f"Exception during installation of {package_name}: {str(e)}", "ERROR")
                self.update_output(f"✗ Exception occurred: {str(e)}")
                self.update_output("=== Installation failed ===")
                messagebox.showerror(
                    self.translations[self.current_language]["error"],
                    self.translations[self.current_language]["error_occurred"].format(error=str(e))
                )
        
        # Uruchom instalację w osobnym wątku
        thread = threading.Thread(target=run_installation)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = DotNetInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
