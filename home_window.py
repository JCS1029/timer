import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

from timer_window import TimerWindow
from custom_mode import CustomMode

HOME_WINDOW_WIDTH = 888
HOME_WINDOW_HEIGHT = 500

class HomeWindow:
    def __init__(self):
        self.timer_app = None
        self._frame = None
        self.master = tk.Tk()
        self.master.title("Home Window")
        res_width = self.master.winfo_screenwidth()
        res_height = self.master.winfo_screenheight()
        x = int(res_width // 2 - HOME_WINDOW_WIDTH // 2)
        y = int(res_height // 2 - HOME_WINDOW_HEIGHT // 2)
        self.master.geometry(f"888x500+{x}+{y}")
        
        self.style = Style(theme="cyborg")

        self.header = ttk.Frame(self.master)
        self.header.pack(anchor="nw", pady=10)

        self.redirectToTimerButton = ttk.Button(self.header, 
        text="Timer Window ->", command=self.redirect_to_timer_button)
        self.redirectToTimerButton.pack(side="left", padx=10)

        self.customMode = ttk.Button(self.header, text="Custom Mode", 
        command=self.redirect_to_custom_mode)
        self.customMode.pack(padx=2)

    def redirect_to_custom_mode(self):
        self.header.pack_forget()

        if self._frame is not None:
            self._frame.destroy()

        self._frame = CustomMode(self.master, on_back=self.back_button)
        self._frame.pack(fill="both", expand=True)

    def back_button(self):
        if self._frame is not None:
            self._frame.destroy()
            self._frame = None
        
        self.header.pack(anchor="nw", pady=10)

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