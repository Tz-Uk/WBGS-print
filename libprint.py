
#!/usr/bin/env python3
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, font as tkfont, messagebox, ttk
from urllib.parse import quote

# ---- Connection settings ----
HOST = "172.24.77.24"
USER = "anonymous"
PASSWORD = ""
REMOTE_DIR = "lp"
TIMEOUT = 10

# ---- Footer info (edit these) ----
CREDIT = "TZUK"
GITHUB_URL = "https://github.com/TZ-UK/WBGS-print"

# ---- Theme ----
BG = "#16171d"
CARD = "#22242e"
FIELD = "#2b2d3a"
FG = "#e8e9ee"
MUTED = "#8b8fa3"
ACCENT = "#4f8cff"
ACCENT_HOVER = "#6aa0ff"
ACCENT_DISABLED = "#34496e"
OK = "#4ade80"
ERR = "#f87171"
BORDER = "#33364a"


class PrinterUploadApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Printer Upload")
        self.configure(bg=BG)

        self.file_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="binary")
        self.copies_var = tk.StringVar(value="1")
        self.sending = False

        self._setup_styles()
        self._build_ui()

        # Lock minimum size to what the content needs, so text never gets cut off
        self.update_idletasks()
        self.base_w = self.winfo_reqwidth()
        self.base_h = self.winfo_reqheight()
        self.minsize(self.base_w, self.base_h)

        if shutil.which("curl") is None:
            messagebox.showerror(
                "System Error",
                "'curl' is not installed on this system.\n"
                "Please install curl to run this script.",
            )
            self.after(0, self.destroy)

    # ---- styling ----
    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        base = tkfont.nametofont("TkDefaultFont")
        base.configure(size=10)
        self.title_font = base.copy()
        self.title_font.configure(size=17, weight="bold")
        self.section_font = base.copy()
        self.section_font.configure(size=9, weight="bold")
        self.small_font = base.copy()
        self.small_font.configure(size=9)
        self.link_font = base.copy()
        self.link_font.configure(size=9)

        s.configure(".", background=BG, foreground=FG, bordercolor=BORDER,
                    lightcolor=BG, darkcolor=BG, focuscolor=BG)
        s.configure("TFrame", background=BG)
        s.configure("Card.TFrame", background=CARD)
        s.configure("TLabel", background=BG, foreground=FG)
        s.configure("Card.TLabel", background=CARD, foreground=FG)
        s.configure("Section.TLabel", background=CARD, foreground=MUTED,
                    font=self.section_font)

        s.configure("TEntry", fieldbackground=FIELD, foreground=FG,
                    insertcolor=FG, bordercolor=BORDER, lightcolor=FIELD,
                    darkcolor=FIELD, padding=7)
        s.map("TEntry", bordercolor=[("focus", ACCENT)],
              lightcolor=[("focus", ACCENT)], darkcolor=[("focus", ACCENT)])

        s.configure("TSpinbox", fieldbackground=FIELD, foreground=FG,
                    insertcolor=FG, bordercolor=BORDER, arrowcolor=MUTED,
                    background=FIELD, lightcolor=FIELD, darkcolor=FIELD,
                    padding=6)
        s.map("TSpinbox", bordercolor=[("focus", ACCENT)],
              arrowcolor=[("active", FG)])

        s.configure("TRadiobutton", background=CARD, foreground=FG,
                    indicatorbackground=FIELD, indicatorforeground=ACCENT,
                    focuscolor=CARD, padding=3)
        s.map("TRadiobutton",
              background=[("active", CARD)],
              indicatorbackground=[("selected", ACCENT), ("active", FIELD)],
              indicatorforeground=[("selected", "#ffffff")])

        s.configure("TButton", background=FIELD, foreground=FG,
                    bordercolor=BORDER, lightcolor=FIELD, darkcolor=FIELD,
                    padding=(14, 7), relief="flat")
        s.map("TButton", background=[("active", BORDER), ("disabled", FIELD)],
              foreground=[("disabled", MUTED)])

        s.configure("Accent.TButton", background=ACCENT, foreground="#ffffff",
                    bordercolor=ACCENT, lightcolor=ACCENT, darkcolor=ACCENT,
                    padding=(18, 9), font=self.section_font)
        s.map("Accent.TButton",
              background=[("disabled", ACCENT_DISABLED), ("active", ACCENT_HOVER)],
              bordercolor=[("disabled", ACCENT_DISABLED), ("active", ACCENT_HOVER)],
              lightcolor=[("disabled", ACCENT_DISABLED), ("active", ACCENT_HOVER)],
              darkcolor=[("disabled", ACCENT_DISABLED), ("active", ACCENT_HOVER)],
              foreground=[("disabled", "#9db2d6")])

    def _card(self, parent, title, row):
        outer = ttk.Frame(parent, style="Card.TFrame", padding=(14, 10, 14, 12))
        outer.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        outer.columnconfigure(0, weight=1)
        ttk.Label(outer, text=title.upper(), style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6))
        return outer

    # ---- UI ----
    def _build_ui(self):
        root = ttk.Frame(self, padding=(20, 18, 20, 12))
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)

        ttk.Label(root, text="Printer Upload", font=self.title_font).grid(
            row=0, column=0, sticky="w")
        ttk.Label(root, text="Dont be stupid pls", foreground=MUTED,
                  font=self.small_font).grid(row=1, column=0, sticky="w",
                                             pady=(0, 14))

        # File
        c1 = self._card(root, "File", 2)
        c1.columnconfigure(0, weight=1)
        self.file_entry = ttk.Entry(c1, textvariable=self.file_var)
        self.file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(c1, text="Browse…", command=self.browse).grid(row=1, column=1)

        # Format
        c2 = self._card(root, "Transfer format", 3)
        ttk.Radiobutton(
            c2, text="Binary — PDFs, images, PostScript, PCL (recommended)",
            variable=self.mode_var, value="binary", style="TRadiobutton",
        ).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(
            c2, text="ASCII — plain text, logs, scripts",
            variable=self.mode_var, value="ascii", style="TRadiobutton",
        ).grid(row=2, column=0, sticky="w")

        # Copies
        c3 = self._card(root, "Copies", 4)
        ttk.Spinbox(c3, from_=1, to=999, textvariable=self.copies_var,
                    width=6, justify="center").grid(row=1, column=0, sticky="w")

        # Send button
        self.send_btn = ttk.Button(root, text="Send to Printer",
                                   style="Accent.TButton", command=self.send)
        self.send_btn.grid(row=5, column=0, sticky="ew", pady=(2, 8))

        # Status (single line) + error details (hidden until needed)
        self.status = tk.Label(root, text="Ready", bg=BG, fg=MUTED,
                               font=self.small_font, anchor="w", justify="left")
        self.status.grid(row=6, column=0, sticky="ew")
        root.bind("<Configure>", lambda e: self.status.configure(
            wraplength=max(e.width - 40, 100)))

        self.details = tk.Text(root, height=4, bg=FIELD, fg=ERR, relief="flat",
                               font=self.small_font, wrap="word", padx=8, pady=6,
                               state="disabled", highlightthickness=1,
                               highlightbackground=BORDER, highlightcolor=BORDER,
                               insertbackground=FG)
        self.details.grid(row=7, column=0, sticky="ew", pady=(6, 0))
        self.details.grid_remove()

        # Footer
        sep = tk.Frame(root, bg=BORDER, height=1)
        sep.grid(row=8, column=0, sticky="ew", pady=(12, 8))
        footer = ttk.Frame(root)
        footer.grid(row=9, column=0, sticky="ew")
        footer.columnconfigure(1, weight=1)

        tk.Label(footer, text=f"Credit: {CREDIT}", bg=BG, fg=MUTED,
                 font=self.small_font).grid(row=0, column=0, sticky="w")
        link = tk.Label(footer, text="GitHub", bg=BG, fg=ACCENT,
                        font=self.link_font, cursor="hand2")
        link.grid(row=0, column=2, sticky="e")
        link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))
        link.bind("<Enter>", lambda e: link.configure(fg=ACCENT_HOVER))
        link.bind("<Leave>", lambda e: link.configure(fg=ACCENT))

    # ---- helpers ----
    def browse(self):
        path = filedialog.askopenfilename(title="Select file to print")
        if path:
            self.file_var.set(path)
            self.set_status("Ready", MUTED)

    def set_status(self, text, color=MUTED, details=None):
        """Thread-safe status update. `details` shows the error box when given."""
        def _apply():
            self.status.configure(text=text, fg=color)
            if details:
                self.details.configure(state="normal")
                self.details.delete("1.0", "end")
                self.details.insert("1.0", details)
                self.details.configure(state="disabled")
                self.details.grid()
                self.update_idletasks()
                need = self.winfo_reqheight()
                if self.winfo_height() < need:
                    self.geometry(f"{self.winfo_width()}x{need}")
            else:
                self.details.grid_remove()
        self.after(0, _apply)

    def set_busy(self, busy):
        self.sending = busy
        self.after(0, lambda: self.send_btn.configure(
            state="disabled" if busy else "normal",
            text="Sending…" if busy else "Send to Printer"))

    # ---- main action ----
    def send(self):
        if self.sending:
            return

        raw = self.file_var.get().strip()
        local_file = Path(raw).expanduser() if raw else None

        if not local_file or not local_file.is_file():
            self.set_status("File not found",
                            ERR, f"File '{raw}' not found.\nPlease check the path and try again.")
            return

        ascii_mode = self.mode_var.get() == "ascii"

        try:
            copies = int(self.copies_var.get().strip() or 1)
        except ValueError:
            copies = 1
        copies = max(copies, 1)
        self.copies_var.set(str(copies))

        self.set_busy(True)
        self.set_status("Connecting…", MUTED)
        threading.Thread(target=self._upload,
                         args=(local_file, ascii_mode, copies),
                         daemon=True).start()

    def _upload(self, local_file, ascii_mode, copies):
        name = local_file.name
        ftp_url = f"ftp://{HOST}/{REMOTE_DIR}/{quote(name, safe='')}"

        cmd = [
            "curl",
            "--silent", "--show-error",
            "--globoff",
            "--connect-timeout", str(TIMEOUT),
            "--user", f"{USER}:{PASSWORD}",
        ]
        if ascii_mode:
            cmd.append("--use-ascii")
        cmd += ["-T", str(local_file), ftp_url]

        extra = {}
        if sys.platform == "win32":
            extra["creationflags"] = subprocess.CREATE_NO_WINDOW

        sent = 0
        for i in range(1, copies + 1):
            if copies > 1:
                self.set_status(f"Sending copy {i} of {copies}…", MUTED)
            else:
                self.set_status("Sending…", MUTED)
            try:
                subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    stdin=subprocess.DEVNULL,
                    **extra,
                )
            except subprocess.CalledProcessError as e:
                detail = (e.stderr or "").strip() or "No details from curl."
                self.set_status(
                    f"Failed on copy {i} of {copies} ({sent} sent)", ERR,
                    f"Curl error (exit {e.returncode}): {detail}")
                self.set_busy(False)
                return
            sent += 1

        plural = "copy" if copies == 1 else "copies"
        self.set_status(f"✓ Sent {copies} {plural} of {name}", OK)
        self.set_busy(False)


if __name__ == "__main__":
    # Crisp rendering on high-DPI Windows displays
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    PrinterUploadApp().mainloop()
