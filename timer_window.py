import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

class TimerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timer")
        self.root.geometry("300x200")
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

    def show_picker(self, button, values, on_select):
        if getattr(self, "_picker", None) and self._picker.winfo_exists():
            self._picker.destroy()

        popup = tk.Toplevel(self.root)
        popup.withdraw()
        popup.transient(self.root)
        popup.overrideredirect(True)

        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()

        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(frame, height=10, width=5, yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)

        for value in values:
            listbox.insert("end", value)

        popup.update_idletasks()

        popup.geometry(f"50x120+{x}+{y}")

        popup.deiconify()
        #popup.lift()
        #listbox.focus_set()

        def on_pick(event):
            selection = listbox.curselection()   
            if not selection:
                return

            on_select(listbox.get(selection[0]))
            popup.destroy()

        listbox.bind("<<ListboxSelect>>", on_pick)

    def select_hours(self):
        values = [f"{h:02d}" for h in range(24)]
        self.show_picker(self.hours_button, values, self.set_hours)

    def select_minutes(self):
        values = [f"{h:02d}" for h in range(60)]
        self.show_picker(self.hours_button, values, self.set_minutes)

    def select_seconds(self):
        values = [f"{h:02d}" for h in range(60)]
        self.show_picker(self.hours_button, values, self.set_seconds)

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
        pass

    def stop_timer(self):
        pass

    def reset_timer(self):
        pass

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimerWindow()
    app.main()