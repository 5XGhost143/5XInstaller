import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import App_Name, App_Desc, output_exe, desktop_shortcut_option_show, startmenu_shortcut_option_show, add_to_path_option_show
from utils import check_admin, create_desktop_shortcut, create_startmenu_shortcut
from installer import unpack_data_files, add_to_path
import threading

class ModernInstallerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(App_Name + " Installer")
        self.geometry("700x600")
        self.resizable(False, False)
        self.configure(bg="#0f0f0f")
    
        self.center_window()
        self.setup_styles()
        
        main_frame = tk.Frame(self, bg="#0f0f0f")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.create_header(main_frame)
        self.create_content(main_frame)
        self.create_footer(main_frame)
        
    def center_window(self):
        self.update_idletasks()
        width = 700
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure("Title.TLabel", 
                       background="#0f0f0f", 
                       foreground="#ffffff", 
                       font=("Segoe UI", 24, "bold"))
        
        style.configure("Subtitle.TLabel", 
                       background="#0f0f0f", 
                       foreground="#888888", 
                       font=("Segoe UI", 11))
        
        style.configure("Modern.TLabel", 
                       background="#0f0f0f", 
                       foreground="#e0e0e0", 
                       font=("Segoe UI", 10))
        
        style.configure("Status.TLabel", 
                       background="#0f0f0f", 
                       foreground="#b0b0b0", 
                       font=("Segoe UI", 9))
        
        style.configure("Modern.TButton",
                       background="#2d2d2d",
                       foreground="#ffffff",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10),
                       padding=(15, 10))
        
        style.map("Modern.TButton",
                 background=[('active', '#404040'),
                            ('pressed', '#1a1a1a')])
        
        style.configure("Primary.TButton",
                       background="#0078d4",
                       foreground="#ffffff",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 12, "bold"),
                       padding=(30, 15))
        
        style.map("Primary.TButton",
                 background=[('active', '#106ebe'),
                            ('pressed', '#005a9e'),
                            ('disabled', '#404040')])
        
        style.configure("Modern.TEntry",
                       fieldbackground="#1a1a1a",
                       foreground="#ffffff",
                       borderwidth=1,
                       insertcolor="#ffffff",
                       font=("Segoe UI", 10),
                       padding=(12, 8))
        
        style.configure("Modern.TCheckbutton",
                       background="#0f0f0f",
                       foreground="#e0e0e0",
                       focuscolor="none",
                       font=("Segoe UI", 10))
        
        style.map("Modern.TCheckbutton",
                 background=[('active', '#0f0f0f')],
                 foreground=[('selected', '#0078d4')])

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="#0f0f0f")
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = ttk.Label(header_frame, text=App_Name, style="Title.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(header_frame, text=App_Desc, style="Subtitle.TLabel")
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        separator = tk.Frame(header_frame, height=1, bg="#2d2d2d")
        separator.pack(fill="x", pady=(20, 0))

    def create_content(self, parent):
        content_frame = tk.Frame(parent, bg="#0f0f0f")
        content_frame.pack(fill="both", expand=True)
        
        path_section = tk.Frame(content_frame, bg="#0f0f0f")
        path_section.pack(fill="x", pady=(0, 25))
        
        path_label = ttk.Label(path_section, text="Installation Directory", style="Modern.TLabel")
        path_label.pack(anchor="w", pady=(0, 8))
        
        path_container = tk.Frame(path_section, bg="#0f0f0f")
        path_container.pack(fill="x")
        
        self.path_var = tk.StringVar(value="C:\\Program Files\\" + App_Name)
        self.path_entry = ttk.Entry(path_container, textvariable=self.path_var, style="Modern.TEntry")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(path_container, text="Browse", command=self.browse_folder, style="Modern.TButton")
        browse_btn.pack(side="right")
        
        options_section = tk.Frame(content_frame, bg="#0f0f0f")
        options_section.pack(fill="x", pady=(0, 30))

        options_label = ttk.Label(options_section, text="Installation Options", style="Modern.TLabel")
        options_label.pack(anchor="w", pady=(0, 15))
        
        if add_to_path_option_show:
            self.add_path_var = tk.BooleanVar(value=True)
            path_checkbox = ttk.Checkbutton(options_section, 
                                   text="Add to system PATH environment variable", 
                                   variable=self.add_path_var,
                                   style="Modern.TCheckbutton")
            path_checkbox.pack(anchor="w", padx=(20, 0))
        else:
            self.add_path_var = tk.BooleanVar(value=False)

        if desktop_shortcut_option_show:
            self.desktop_shortcut_var = tk.BooleanVar(value=True)
            desktop_checkbox = ttk.Checkbutton(options_section,
                                   text="Create Desktop Shortcut",
                                   variable=self.desktop_shortcut_var,
                                   style="Modern.TCheckbutton")
            desktop_checkbox.pack(anchor="w", padx=(20, 0))
        else:
            self.desktop_shortcut_var = tk.BooleanVar(value=False)

        if startmenu_shortcut_option_show:
            self.startmenu_shortcut_var = tk.BooleanVar(value=True)
            startmenu_checkbox = ttk.Checkbutton(options_section,
                                   text="Create Start-Menu Shortcut",
                                   variable=self.startmenu_shortcut_var,
                                   style="Modern.TCheckbutton")
            startmenu_checkbox.pack(anchor="w", padx=(20, 0))
        else:
            self.startmenu_shortcut_var = tk.BooleanVar(value=False)
        
        status_section = tk.Frame(content_frame, bg="#0f0f0f")
        status_section.pack(fill="x", pady=(20, 0))
        
        self.status_var = tk.StringVar(value="Ready to install")
        self.status_label = ttk.Label(status_section, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor="w")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_section, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.pack_forget()

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="#0f0f0f")
        footer_frame.pack(fill="x", pady=(30, 0))
        
        separator = tk.Frame(footer_frame, height=1, bg="#2d2d2d")
        separator.pack(fill="x", pady=(0, 20))
        
        button_container = tk.Frame(footer_frame, bg="#0f0f0f")
        button_container.pack(fill="x")
        
        self.install_btn = ttk.Button(button_container, text="INSTALL", 
                                     command=self.start_install, style="Primary.TButton")
        self.install_btn.pack(expand=True, pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Installation Directory")
        if folder:
            self.path_var.set(folder)

    def update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()

    def show_success_message(self, install_path):
        success_window = tk.Toplevel(self)
        success_window.title("Installation Complete")
        success_window.geometry("400x200")
        success_window.configure(bg="#0f0f0f")
        success_window.resizable(False, False)
        success_window.transient(self)
        success_window.grab_set()
        
        success_window.update_idletasks()
        x = (success_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (success_window.winfo_screenheight() // 2) - (200 // 2)
        success_window.geometry(f'400x200+{x}+{y}')
        
        content = tk.Frame(success_window, bg="#0f0f0f")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        success_label = ttk.Label(content, text="✓ Installation Successful", 
                                 style="Title.TLabel", font=("Segoe UI", 16, "bold"))
        success_label.pack(pady=(0, 10))
        
        info_label = ttk.Label(content, text=App_Name + f" has been installed to:\n{install_path}", 
                              style="Modern.TLabel", justify="center")
        info_label.pack(pady=(0, 20))
        
        ok_btn = ttk.Button(content, text="OK", command=success_window.destroy, style="Primary.TButton")
        ok_btn.pack()

    def show_error_message(self, title, message):
        error_window = tk.Toplevel(self)
        error_window.title(title)
        error_window.geometry("450x200")
        error_window.configure(bg="#0f0f0f")
        error_window.resizable(False, False)
        error_window.transient(self)
        error_window.grab_set()
        
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (error_window.winfo_screenheight() // 2) - (200 // 2)
        error_window.geometry(f'450x200+{x}+{y}')
        
        content = tk.Frame(error_window, bg="#0f0f0f")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        error_label = ttk.Label(content, text="⚠ Error", 
                               style="Title.TLabel", font=("Segoe UI", 16, "bold"))
        error_label.pack(pady=(0, 15))
        
        info_label = ttk.Label(content, text=message, 
                               style="Modern.TLabel", justify="left", wraplength=400)
        info_label.pack(pady=(0, 20))
        
        ok_btn = ttk.Button(content, text="OK", command=error_window.destroy, style="Primary.TButton")
        ok_btn.pack()

    def start_install(self):
        install_path = self.path_var.get().strip()
        if not install_path:
            self.show_error_message("Invalid Path", "Please specify an installation path.")
            return

        if not check_admin():
            self.show_error_message("Administrator Required", 
                                   "Administrator privileges are required.\nPlease run this installer as Administrator.")
            return

        self.install_btn.config(state="disabled")

        self.progress_bar.pack(fill="x", pady=(10, 0))
        self.progress_bar.start(10)

        self.update_status("Installation started...")

        def run_install():
            try:
                if os.path.exists(install_path):
                    self.update_status("Removing existing installation...")
                    shutil.rmtree(install_path)

                os.makedirs(install_path, exist_ok=True)

                if not unpack_data_files(install_path, self.update_status):
                    self.after(0, lambda: self.show_error_message("Installation Error", "Failed to unpack data files. Make sure .5xdata files are present."))
                    return

                if self.add_path_var.get():
                    self.update_status("Adding to system PATH...")
                    result = add_to_path(install_path)
                    if result is not True:
                        self.update_status(f"Warning: Could not add to PATH: {result}")
                    else:
                        self.update_status("Added to system PATH")

                if self.desktop_shortcut_var.get():
                    self.update_status("Creating desktop shortcut...")
                    result = create_desktop_shortcut(install_path, App_Name, output_exe)
                    if result is not True:
                        self.update_status(f"Warning: Could not create desktop shortcut: {result}")

                if self.startmenu_shortcut_var.get():
                    self.update_status("Creating start menu shortcut...")
                    result = create_startmenu_shortcut(install_path, App_Name, output_exe)
                    if result is not True:
                        self.update_status(f"Warning: Could not create start menu shortcut: {result}")

                self.after(0, lambda: self.update_status("Installation completed successfully!"))
                self.after(0, lambda: self.show_success_message(install_path))

            except Exception as e:
                self.after(0, lambda: self.show_error_message("Installation Error", str(e)))

            finally:
                self.after(0, lambda: self.install_btn.config(state="normal"))
                self.after(0, lambda: self.progress_bar.stop())
                self.after(0, lambda: self.progress_bar.pack_forget())

        threading.Thread(target=run_install, daemon=True).start()


if __name__ == "__main__":
    app = ModernInstallerUI()
    app.mainloop()
