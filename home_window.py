import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

from timer_window import TimerWindow

HOME_WINDOW_WIDTH = 888
HOME_WINDOW_HEIGHT = 500

class HomeWindow:
    def __init__(self):
        self.timer_app = None
        self.master = tk.Tk()
        self.master.title("Home Window")
        res_width = self.master.winfo_screenwidth()
        res_height = self.master.winfo_screenheight()
        x = int(res_width // 2 - HOME_WINDOW_WIDTH // 2)
        y = int(res_height // 2 - HOME_WINDOW_HEIGHT // 2)
        self.master.geometry(f"888x500+{x}+{y}")
        
        self.style = Style(theme="cyborg")

        self.frame1 = ttk.Frame(self.master)
        self.frame1.pack(anchor="nw", pady=10)

        self.redirectToTimerButton = ttk.Button(self.frame1, 
        text="Timer Window ->", command=self.redirect_to_timer_button)
        self.redirectToTimerButton.pack(side="left", padx=10)


    def redirect_to_timer_button(self):
        self.master.iconify()
        if self.timer_app is None or not self.timer_app.root.winfo_exists():
            self.timer_app = TimerWindow(self.master)
        self.timer_app.root.deiconify()


    def main(self):
        self.master.mainloop()

if __name__ == "__main__":
    app = HomeWindow()
    app.main()