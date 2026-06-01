import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

HOME_WINDOW_WIDTH = 888
HOME_WINDOW_HEIGHT = 500

class HomeWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Home Window")
        res_width = self.root.winfo_screenwidth()
        res_height = self.root.winfo_screenheight()
        x = int(res_width // 2 - HOME_WINDOW_WIDTH // 2)
        y = int(res_height // 2 - HOME_WINDOW_HEIGHT // 2)
        self.root.geometry(f"888x500+{x}+{y}")
        
        self.style = Style(theme="cyborg")

        self.frame1 = ttk.Frame(self.root)

        self.redirectToTimerButton = ttk.Button(self.frame1, 
        text="Timer Window ->", command=self.redirect_to_timer_button)

    def redirect_to_timer_button(self):
        pass


    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HomeWindow()
    app.main()