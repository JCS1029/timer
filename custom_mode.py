import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

class CustomMode(tk.Frame):
    def __init__(self, master, on_back=None):
        tk.Frame.__init__(self, master)
        self.frame = tk.Frame(self)
        self.frame.pack()
        tk.Label(self.frame, text="............").pack()
        ttk.Button(self.frame, text="<-", command=on_back).pack()

        