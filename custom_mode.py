import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

class CustomMode(tk.Frame):
    def __init__(self, master, on_back=None):
        tk.Frame.__init__(self, master)

        self.style = Style()        
        self.style.configure('LabelStyle.TLabel', font=('Arial', 12))

        self.header = tk.Frame(self)
        self.header.pack(fill="x", anchor="n", pady=5)

        self.titleLabel = tk.Label(self.header, text="Custom mode", font=('Arial', 32))
        self.titleLabel.pack(side="top")

        self.options = tk.Frame(self)
        self.options.pack(fill="x", pady=30)

        self.frame = tk.Frame(self)
        self.frame.pack(fill="x", pady=15)

        self.modeName = ttk.Label(self.frame, text="Mode Name", style="LabelStyle.TLabel")
        self.modeName.grid(row=0, column=0, padx=(60, 20))

        self.modeNameInput = tk.Entry(self.frame)
        self.modeNameInput.grid(row=1, column=0, padx=(60, 20), pady=15)
        
        self.sessionTime = ttk.Label(self.frame, text="Session Duration", style="LabelStyle.TLabel")
        self.sessionTime.grid(row=0, column=1, padx=20)

        self.sessionTimeInput = tk.Entry(self.frame)
        self.sessionTimeInput.grid(row=1, column=1, padx=20, pady=15)
        
        self.breakTime = ttk.Label(self.frame, text="Break Duration", style="LabelStyle.TLabel")
        self.breakTime.grid(row=0, column=2, padx=20)

        self.breakTimeInput = tk.Entry(self.frame)
        self.breakTimeInput.grid(row=1, column=2, padx=20, pady=15)

        self.sessionCount = ttk.Label(self.frame, text="Number of sessions", style="LabelStyle.TLabel")
        self.sessionCount.grid(row=0, column=3, padx=(20, 60))

        self.sessionCountInput = tk.Entry(self.frame)
        self.sessionCountInput.grid(row=1, column=3, padx=(20, 60), pady=15)