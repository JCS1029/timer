import json
from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

MODES_FILE = Path(__file__).resolve().parent / "modes.json"

DEFAULT_MODES = [
    {"name": "50:10", "session": "50", "break": "10", "count": ""},
    {"name": "25:5", "session": "25", "break": "5", "count": ""},
]

REMOVE_TRIGGER = 0

def duration_parts(value):
    text = str(value).strip()
    if text == "":
        return 0, 0, 0
    numbers = [int(float(piece)) if piece else 0 for piece in text.split(":")]
    if len(numbers) == 1:
        hours, minutes = divmod(numbers[0], 60)
        return hours, minutes, 0
    if len(numbers) == 2:
        return numbers[0], numbers[1], 0
    return numbers[0], numbers[1], numbers[2]


class DurationEntry(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.parts = []
        check = self.register(self._digits)
        for index, (caption, limit) in enumerate((("H", 99), ("M", 59), ("S", 59))):
            column = index * 2
            ttk.Label(self, text=caption).grid(row=0, column=column)
            entry = ttk.Entry(
                self, width=2, justify="center", validate="key",
                validatecommand=(check, "%P"),
            )
            entry.grid(row=1, column=column, padx=1)
            entry.bind("<FocusOut>", lambda event, entry=entry, limit=limit: self._clamp(entry, limit))
            self.parts.append((entry, limit))
            if index < 2:
                ttk.Label(self, text=":").grid(row=1, column=column + 1)
        self.set_time(0, 0, 0)

    def _digits(self, proposed):
        return proposed == "" or (proposed.isdigit() and len(proposed) <= 2)

    def _clamp(self, entry, limit):
        number = min(self._read(entry), limit)
        entry.delete(0, "end")
        entry.insert(0, f"{number:02d}")

    def _read(self, entry):
        text = entry.get().strip()
        if text == "":
            return 0
        return int(text)

    def get(self):
        hours, minutes, seconds = (
            min(self._read(entry), limit) for entry, limit in self.parts
        )
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def set_time(self, hours, minutes, seconds):
        for (entry, limit), number in zip(self.parts, (hours, minutes, seconds)):
            number = min(max(int(number), 0), limit)
            entry.delete(0, "end")
            entry.insert(0, f"{number:02d}")

    def insert(self, index, value):
        self.set_time(*duration_parts(value))

def write_default_modes():
    with MODES_FILE.open("w", encoding="utf-8") as file:
        json.dump(DEFAULT_MODES, file, indent=2)

class CustomMode(tk.Frame):
    def __init__(self, master, on_back=None):
        tk.Frame.__init__(self, master)
        self.on_back = on_back

        self.style = Style(theme="cyborg")        
        self.style.configure('LabelStyle.TLabel', font=('Arial', 12))

        self.header = ttk.Frame(self)
        self.header.pack(fill="x", anchor="n", padx=20, pady=5)

        self.titleLabel = ttk.Label(self.header, text="Custom mode", font=('Arial', 32))
        self.titleLabel.pack(side="top")

        self.redirectToHomeButton = ttk.Button(self.header, text="Home Window", command=self.redirect_to_home_button, style="Action.TButton")
        self.redirectToHomeButton.pack(side="left", padx=2)

        self.modeViewport = tk.Frame(self, height=1, bg=self.style.colors.bg, highlightthickness=0)
        self.modeViewport.pack_propagate(False)
        self.modeViewport.pack(fill="x", padx=40)

        self.modeList = ttk.ScrolledFrame(self.modeViewport)
        self.modeList.pack(fill="both", expand=True)
        # Leave would turn wheel scrolling off as soon as the pointer hits a label or entry.
        self.modeList.container.unbind("<Leave>")
        self.modeList.enable_scrolling()
        self._fitting = False

        self.modeForms = []

        self.buttonRow = ttk.Frame(self)
        self.buttonRow.pack(pady=10)

        self.addModeButton = ttk.Button(self.buttonRow, text="Add Mode", command=self.add_mode, style="Action.TButton")
        self.addModeButton.pack(side="left", padx=(0,10))

        self.deleteButton = ttk.Button(self.buttonRow, text="Remove Mode", command=self.delete_mode, style="Action.TButton")
        self.deleteButton.pack(side="left", padx=(0,10))

        self.saveButton = ttk.Button(self.buttonRow, text="Save Changes", command=self.save_mode_changes, style="Action.TButton")
        self.saveButton.pack(side="left")

        self.bind("<Configure>", self.fit_mode_list)

        self.load_modes()

    def redirect_to_home_button(self):
        if self.on_back is not None:
            self.on_back()

    def fit_mode_list(self, event=None):
        if self._fitting:
            return
        if event is not None and event.widget is not self:
            return
        self._fitting = True
        try:
            self.update_idletasks()
            content_height = self.modeList.winfo_reqheight()
            available = (
                self.winfo_height()
                - self.header.winfo_reqheight()
                - self.buttonRow.winfo_reqheight()
                - 30
            )
            if available < 1:
                height = content_height
            else:
                height = min(content_height, available)
            height = max(int(height), 1)
            if int(self.modeViewport.cget("height")) != height:
                self.modeViewport.configure(height=height)
        finally:
            self._fitting = False

    def add_mode(self):
        row = ttk.Frame(self.modeList)
        row.pack(fill="x", pady=10)

        mode = ttk.Frame(row)
        mode.pack(side="left", fill="x",expand=True)

        removeButton = ttk.Button(row, text="X")

        for column in range(4):
            mode.columnconfigure(column, weight=1, uniform="fields")

        nameLabel = ttk.Label(mode, text="Mode Name", style="LabelStyle.TLabel")
        nameLabel.grid(row=0, column=0, padx=20, pady=5)
        nameInput = ttk.Entry(mode)
        nameInput.grid(row=1, column=0, padx=20, sticky="s")

        sessionLabel = ttk.Label(mode, text="Session Duration", style="LabelStyle.TLabel")
        sessionLabel.grid(row=0, column=1, padx=20)
        sessionInput = DurationEntry(mode)
        sessionInput.grid(row=1, column=1, padx=20, sticky="s")

        breakLabel = ttk.Label(mode, text="Break Duration", style="LabelStyle.TLabel")
        breakLabel.grid(row=0, column=2, padx=20)
        breakInput = DurationEntry(mode)
        breakInput.grid(row=1, column=2, padx=20, sticky="s")

        countLabel = ttk.Label(mode, text="Number of Sessions", style="LabelStyle.TLabel")
        countLabel.grid(row=0, column=3, padx=20)
        countInput = ttk.Entry(mode)
        countInput.grid(row=1, column=3, padx=20, sticky="s")

        self.modeForms.append({
            "name": nameInput,
            "session": sessionInput,
            "break": breakInput,
            "count": countInput,
            "mode": mode,
            "row": row,
            "removeButton": removeButton,
        })
        self.modeList.enable_scrolling()
        self.fit_mode_list()

    def delete_mode(self):
        global REMOVE_TRIGGER
        if REMOVE_TRIGGER == 0:
            for form in self.modeForms:
                button = form["removeButton"]
                button.pack(side="left", before=form["mode"], anchor="s")
                button.configure(command=lambda form=form: self.remove_form(form))
            REMOVE_TRIGGER = 1
        else:
            for form in self.modeForms:
                button = form["removeButton"]
                button.pack_forget()
            REMOVE_TRIGGER = 0

    def remove_form(self, form):
        form["row"].destroy()
        self.modeForms.remove(form)
        self.fit_mode_list()
        self.save_mode_changes()

    def save_mode_changes(self):
        modes = []
        for form in self.modeForms:
            modes.append({
                "name": form["name"].get(),
                "session": form["session"].get(),
                "break": form["break"].get(),
                "count": form["count"].get(),
            })
        with MODES_FILE.open("w", encoding="utf-8") as file:
            json.dump(modes, file, indent=2)

    def load_modes(self):
            if not MODES_FILE.exists():
                write_default_modes()
            with MODES_FILE.open(encoding="utf-8") as file:
                modes = json.load(file)
            for mode in modes:
                self.add_mode()
                form = self.modeForms[-1]
                form["removeButton"].configure(command=lambda form=form: self.remove_form(form))
                form["name"].insert(0, mode["name"])
                form["session"].insert(0, mode["session"])
                form["break"].insert(0, mode["break"])
                form["count"].insert(0, mode["count"])

