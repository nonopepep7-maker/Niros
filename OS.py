import tkinter as tk
from tkinter import messagebox
import datetime
import random

class NirOS:
    def __init__(self, root):
        self.root = root
        self.root.title("NirOS - Secure Session")
        self.root.geometry("1000x700")
                               
        self.theme = "dark"
        self.system_name = "NirOS 1.0"
        self.start_time = datetime.datetime.now()
        
        # User Credentials
        self.req_user = "Admin"
        self.req_pass = "Admin123"

        self.colors = {
            "dark": {"bg": "#202124", "fg": "#ffffff", "taskbar": "#3c4043", "accent": "#8ab4f8"},
            "light": {"bg": "#f1f3f4", "fg": "#202124", "taskbar": "#dadce0", "accent": "#1a73e8"}
        }
        
        self.setup_login()

    def setup_login(self):
        self.login_frame = tk.Frame(self.root, bg="#202124")
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        center = tk.Frame(self.login_frame, bg="#202124")
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(center, text="NirOS Login", font=("Arial", 28, "bold"), bg="#202124", fg="#8ab4f8").pack(pady=20)
        tk.Label(center, text="(usr: Admin & pass: Admin123)", font=("Arial", 12, "bold"), bg="#202124", fg="#8ab4f8").pack(pady=20)


        tk.Label(center, text="Username", bg="#202124", fg="white").pack()
        self.user_ent = tk.Entry(center, justify='center', font=("Arial", 12), width=25)
        self.user_ent.pack(pady=5)

        tk.Label(center, text="Password", bg="#202124", fg="white").pack()
        self.pass_ent = tk.Entry(center, justify='center', font=("Arial", 12), show="*", width=25)
        self.pass_ent.pack(pady=5)

        tk.Button(center, text="Sign In", command=self.authenticate, width=20, bg="#8ab4f8", fg="#202124", font=("Arial", 10, "bold")).pack(pady=25)

    def authenticate(self):
        # Updated Credentials Check
        if self.user_ent.get() == self.req_user and self.pass_ent.get() == self.req_pass:
            self.login_frame.destroy()
            self.build_desktop()
            self.show_notification("Security", f"Authenticated as {self.req_user}")
        else:
            messagebox.showerror("Access Denied", "Invalid Admin credentials.")

    def build_desktop(self):
        self.desktop = tk.Canvas(self.root, highlightthickness=0)
        self.desktop.place(relx=0, rely=0, relwidth=1, relheight=0.95)

        self.taskbar = tk.Frame(self.root, height=40)
        self.taskbar.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

        self.start_btn = tk.Button(self.taskbar, text="Start", font=("Arial", 9, "bold"), command=self.toggle_start_menu)
        self.start_btn.pack(side="left", padx=5)

        self.clock_label = tk.Label(self.taskbar, text="", font=("Arial", 10))
        self.clock_label.pack(side="right", padx=10)

        self.create_start_menu()
        self.apply_theme()
        self.update_clock()

    def apply_theme(self):
        c = self.colors[self.theme]
        self.desktop.config(bg=c["bg"])
        self.taskbar.config(bg=c["taskbar"])
        self.clock_label.configure(bg=c["taskbar"], fg=c["fg"])

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def create_start_menu(self):
        self.start_menu = tk.Frame(self.root, width=200, height=250, relief="raised", bd=2)
        apps = [
            ("Notepad", self.open_notepad),
            ("Settings", self.open_settings),
            ("Terminal", self.open_terminal),
            ("Calculator", self.open_calculator),
            ("System Info", self.open_sys_info)
        ]
        for name, cmd in apps:
            tk.Button(self.start_menu, text=f" 📂 {name}", 
                      command=lambda c=cmd: [c(), self.toggle_start_menu()],
                      anchor="w", relief="flat", font=("Arial", 10)).pack(fill="x", padx=5, pady=2) 

    def toggle_start_menu(self):
        if self.start_menu.winfo_viewable():
            self.start_menu.place_forget()
        else:
            # Menu pops up above the taskbar
            self.start_menu.place(x=0, y=self.root.winfo_height() - 40 - 250)

    def show_notification(self, title, msg):
        notif = tk.Toplevel(self.root)
        notif.overrideredirect(True)
        notif.geometry(f"220x70+{self.root.winfo_width()-230}+{self.root.winfo_height()-120}")
        notif.config(bg="#333", padx=8, pady=8)
        tk.Label(notif, text=title, font=("Arial", 10, "bold"), bg="#333", fg="#8ab4f8").pack(anchor="w")
        tk.Label(notif, text=msg, font=("Arial", 9), bg="#333", fg="#fff", wraplength=200).pack(anchor="w")
        self.root.after(4000, notif.destroy)

    def create_window(self, title, width=400, height=300):
        win = NirWindow(self.desktop, title, width, height, self.colors[self.theme])
        return win

    def open_terminal(self):
        win = self.create_window("Terminal")
        term_text = tk.Text(win.content, bg="#000", fg="#0f0", insertbackground="#0f0", font=("Courier", 10))
        term_text.pack(fill="both", expand=True)
        term_text.insert("end", f"NirOS Kernel [Authenticated: {self.req_user}]\nType 'help' for commands\n> ")

        def handle_command(event):
            line = term_text.get("end-2c linestart", "end-1c").split(">")[-1].strip()
            res = ""
            if line == "help": res = "Available: help, clear, time, echo, whoami"
            elif line == "whoami": res = f"Current User: {self.req_user}"
            elif line == "clear": 
                term_text.delete("1.0", "end")
                res = ""
            elif line == "time": 
                res = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif line.startswith("echo "): res = line[5:]
            
            term_text.insert("end", f"\n{res}\n> " if res else "\n> ")
            term_text.see("end")
            return "break"

        term_text.bind("<Return>", handle_command)

    def open_calculator(self):
        win = self.create_window("Calculator", 280, 350)
        ent = tk.Entry(win.content, font=("Arial", 20), justify="right", bd=5)
        ent.pack(fill="x", padx=10, pady=10)

        btn_frame = tk.Frame(win.content, bg="white")
        btn_frame.pack()

        def calc():
            try: 
                result = eval(ent.get())
                ent.delete(0, "end")
                ent.insert(0, str(result))
            except: 
                ent.delete(0, "end")
                ent.insert(0, "Error")

        tk.Button(btn_frame, text="Calculate (=)", command=calc, width=20, bg="#8ab4f8").grid(row=0, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="Clear (C)", command=lambda: ent.delete(0, "end"), width=20).grid(row=1, column=0, columnspan=2)

    def open_notepad(self):
        win = self.create_window("Notepad", 500, 400)
        text = tk.Text(win.content, undo=True, font=("Arial", 11), padx=5, pady=5)
        text.pack(fill="both", expand=True)

    def open_settings(self):
        win = self.create_window("Settings", 300, 220)
        tk.Label(win.content, text="Change System Display Name:", bg="white").pack(pady=10)
        name_ent = tk.Entry(win.content, justify="center")
        name_ent.pack()
        name_ent.insert(0, self.system_name)

        def save():
            self.system_name = name_ent.get()
            self.show_notification("System", "Display name updated.")

        tk.Button(win.content, text="Apply Changes", command=save, bg="#eee").pack(pady=10)
        tk.Button(win.content, text="Switch Theme",
                  command=lambda: [setattr(self, "theme", "light" if self.theme == "dark" else "dark"), self.apply_theme()]).pack()

    def open_sys_info(self):
        win = self.create_window("System Information", 320, 280)
        uptime = datetime.datetime.now() - self.start_time
        info = (f"Machine Name: {self.system_name}\n"
                f"User: {self.req_user}\n"
                f"CPU: i9-15900K\n"
                f"RAM: 32.0 GB\n"
                f"Uptime: {str(uptime).split('.')[0]}\n"
                f"Storage: 5 TB SSD")
        tk.Label(win.content, text=info, justify="left", font=("Courier", 10), bg="white", padx=15, pady=20).pack()

class NirWindow:
    def __init__(self, parent, title, width, height, colors):
        self.frame = tk.Frame(parent, relief="raised", bd=2, bg=colors["taskbar"])
        self.frame.place(x=random.randint(50, 150), y=random.randint(50, 150), width=width, height=height)

        self.title_bar = tk.Frame(self.frame, bg=colors["accent"], height=28)
        self.title_bar.pack(fill="x")

        tk.Label(self.title_bar, text=title, bg=colors["accent"], fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=8)
        tk.Button(self.title_bar, text="✕", command=self.close, bg="#f44336", fg="white", relief="flat", font=("Arial", 8)).pack(side="right", padx=2)

        self.content = tk.Frame(self.frame, bg="white")
        self.content.pack(fill="both", expand=True)

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.frame.winfo_x() + deltax
        new_y = self.frame.winfo_y() + deltay
        self.frame.place(x=new_x, y=new_y)

    def close(self):
        self.frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NirOS(root)
    root.mainloop()