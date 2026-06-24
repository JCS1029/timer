import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

class CustomMode(tk.Frame):
    def __init__(self, master, on_back=None):
        tk.Frame.__init__(self, master)
        self.header = tk.Frame(self)
        self.header.pack(fill="x", anchor="n", pady=5)

        self.titleLabel = tk.Label(self.header, text="Custom mode", font=('Arial', 32))
        self.titleLabel.pack(side="top")

        self.options = tk.Frame(self)
        self.options.pack(fill="x", pady=30)

        self.frame = tk.Frame(self)
        self.frame.pack(fill="x", pady=15)

        self.sessionName = tk.Entry(self.frame)
        self.sessionName.pack(side="left", padx=15, pady=10)
        

        