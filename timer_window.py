import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style
import ctypes as ct


def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, 20, ct.byref(value),
                         4)

POPUP_COUNT = 0

class TimerWindow:
    def __init__(self, master):
        #self.master = tk.Tk()
        #self.master.title("Timer")
        #self.master.attributes("-alpha", 0.0)

        self.master = master
        self.root = tk.Toplevel(self.master)
        res_width = self.root.winfo_screenwidth()
        res_height = self.root.winfo_screenheight()
        x = int(res_width - 210)
        y = int(res_height - 215)
        self.root.geometry(f"180x135+{x}+{y}")
        dark_title_bar(self.root)
        self.style = Style(theme="cyborg")
        #self.style.theme_use()

        self.style.configure('Link.TButton', font=('Arial', 12))
        self.style.configure('Action.TButton', font=('Arial', 8), background="#060606", borderwidth=0)
        #self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        #self.master.bind("<Unmap>", lambda e: self.root.withdraw())   # Hide child if master minimizes
        #self.root.bind("<Map>", lambda e: self.root.after_idle(
            #lambda: self.root.winfo_exists() and self.root.overrideredirect(True)
        #))

        self.control_panel = ttk.Frame(self.root)
        self.control_panel.pack(anchor="ne", padx=1, pady=1)

        self.redirectToHomeButton = ttk.Button(self.control_panel, text="Home Window", command=self.redirect_to_home_button, style="Action.TButton")
        self.redirectToHomeButton.pack(side="right", padx=2)

        self.time_frame = ttk.Frame(self.root)
        self.time_frame.pack(pady=10)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=0)

        self.hours_button = ttk.Button(self.time_frame, text="00", command=self.select_hours, bootstyle="link")
        self.hours_button.pack(side="left", padx=0)

        self.first_colon_label = ttk.Label(self.time_frame, text=":", font=("Arial", 12))
        self.first_colon_label.pack(side="left", padx=0)

        self.minutes_button = ttk.Button(self.time_frame, text="00", command=self.select_minutes, bootstyle="link")
        self.minutes_button.pack(side="left", padx=0)

        self.second_colon_label = ttk.Label(self.time_frame, text=":", font=("Arial", 12))
        self.second_colon_label.pack(side="left", padx=0)

        self.seconds_button = ttk.Button(self.time_frame, text="00", command=self.select_seconds, bootstyle="link")
        self.seconds_button.pack(side="left", padx=0)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_timer, style="Action.TButton")
        self.start_button.pack(side="left", padx=0)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_timer, style="Action.TButton")
        self.stop_button.pack(side="left", padx=0)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_timer, style="Action.TButton")
        self.reset_button.pack(side="left", padx=0)

        self.hours_var = tk.StringVar(value="00")
        self.minutes_var = tk.StringVar(value="00")
        self.seconds_var = tk.StringVar(value="00")

        self._picker = None

    def redirect_to_home_button(self):
        self.master.deiconify()

    def show_picker(self, button, values, on_select):
        global POPUP_COUNT
        POPUP_COUNT += 1
        if POPUP_COUNT > 1:
            self._picker.destroy()
            POPUP_COUNT -= 1

        popup = tk.Toplevel(self.root)
        self._picker = popup
        #popup.withdraw()
        #popup.transient(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        popup.geometry(f"50x120+{x}+{y}")


        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(frame, height=10, width=5, yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=listbox.yview)

        for value in values:
            listbox.insert("end", value)

        #popup.update_idletasks()


        #popup.deiconify()
        #popup.lift()
        #listbox.focus_set()

        def on_pick(event):
            global POPUP_COUNT
            selection = listbox.curselection()   
            if not selection:
                return

            on_select(listbox.get(selection[0]))
            popup.destroy()
            POPUP_COUNT -= 1

        listbox.bind("<<ListboxSelect>>", on_pick)

    def select_hours(self):
        values = [f"{h:02d}" for h in range(24)]
        self.show_picker(self.hours_button, values, self.set_hours)

    def select_minutes(self):
        values = [f"{h:02d}" for h in range(60)]
        self.show_picker(self.minutes_button, values, self.set_minutes)

    def select_seconds(self):
        values = [f"{h:02d}" for h in range(60)]
        self.show_picker(self.seconds_button, values, self.set_seconds)

    def set_hours(self, value):
        self.hours_var.set(value)
        self.hours_button.configure(text=value)

    def set_minutes(self, value):
        self.minutes_var.set(value)
        self.minutes_button.configure(text=value)

    def set_seconds(self, value):
        self.seconds_var.set(value)
        self.seconds_button.configure(text=value)

    def start_timer(self):
        if getattr(self, 'running', False): 
            return
        
        seconds = int(self.seconds_var.get())
        minutes = int(self.minutes_var.get())
        hours = int(self.hours_var.get())

        self.range_val = hours * 3600 + minutes * 60 + seconds

        if self.range_val > 0:
            self.running = True
            self.countdown()


    def countdown(self):
        if not getattr(self, 'running', False): 
            return

        if self.range_val > 0:
            self.range_val -= 1

            h = self.range_val // 3600
            m = (self.range_val % 3600) // 60
            s = self.range_val % 60

            self.hours_button.config(text=f"{h:02d}")
            self.minutes_button.config(text=f"{m:02d}")
            self.seconds_button.config(text=f"{s:02d}")

            self.root.after(1000, self.countdown)

        else:
            self.running = False

    def stop_timer(self):
        self.running = False
        h = self.range_val // 3600
        m = (self.range_val % 3600) // 60
        s = self.range_val % 60

        self.hours_var.set(h)
        self.minutes_var.set(m)
        self.seconds_var.set(s)

    def reset_timer(self):
        self.running = False

        self.hours_var.set("00")
        self.minutes_var.set("00")
        self.seconds_var.set("00")

        self.hours_button.config(text="00")
        self.minutes_button.config(text="00")
        self.seconds_button.config(text="00")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimerWindow()
    app.main()