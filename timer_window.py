import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

POPUP_COUNT = 0

class TimerWindow:
    def __init__(self):
        self.root = tk.Tk()
        res_width = self.root.winfo_screenwidth()
        res_height = self.root.winfo_screenheight()
        x = int(0.5 * res_width - 150)
        y = int(0.5 * res_height - 100)
        self.root.title("Timer")
        self.root.geometry(f"300x200+{x}+{y}")
        self.root.configure(bg="gray")
        self.style = Style(theme="darkly")
        self.style.theme_use()

        self.style.configure('Link.TButton', font=('Arial', 20))

        self.time_frame = ttk.Frame(self.root)
        self.time_frame.pack(pady=40)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=0)

        self.hours_button = ttk.Button(self.time_frame, text="00", command=self.select_hours, bootstyle="link")
        self.hours_button.pack(side="left", padx=10)

        self.first_colon_label = ttk.Label(self.time_frame, text=":", font=("Arial", 20))
        self.first_colon_label.pack(side="left", padx=1)

        self.minutes_button = ttk.Button(self.time_frame, text="00", command=self.select_minutes, bootstyle="link")
        self.minutes_button.pack(side="left", padx=10)

        self.second_colon_label = ttk.Label(self.time_frame, text=":", font=("Arial", 20))
        self.second_colon_label.pack(side="left", padx=1)

        self.seconds_button = ttk.Button(self.time_frame, text="00", command=self.select_seconds, bootstyle="link")
        self.seconds_button.pack(side="left", padx=10)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        self.hours_var = tk.StringVar(value="00")
        self.minutes_var = tk.StringVar(value="00")
        self.seconds_var = tk.StringVar(value="00")

        self._picker = None

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

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        popup.geometry(f"50x120+{x}+{y}")


        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(frame, height=10, width=5, yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)

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