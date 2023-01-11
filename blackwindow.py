import tkinter as tk

# --- constants --- (UPPER_CASE_NAMES)

BUTTON_FOREGROUND = "#222222"
BUTTON_BACKGROUND = "black"
BUTTON_FOREGROUND_HOVER = BUTTON_FOREGROUND
BUTTON_BACKGROUND_HOVER = "red"

# window colors
WINDOW_BACKGROUND = "black"
WINDOW_FOREGROUND = "black"

WINDOW_TITLE = " "

# --- classes --- (CamelCaseNames)

class CloseButton(tk.Button):

    def __init__(self, master, text=" ", command=None, **kwargs):
        super().__init__(master, bd=0, font="bold", padx=10, pady=10, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=BUTTON_BACKGROUND_HOVER,
                         activeforeground=BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command)
        master.pack(expand=True, fill="x")
        self.pack(side="top", anchor="ne")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self["bg"] = BUTTON_BACKGROUND_HOVER

    def on_leave(self, event):
        self["bg"] = BUTTON_BACKGROUND

class ResizeButton(tk.Button):
    
    def __init__(self, master, text=" ", command=None, **kwargs):
        super().__init__(master, bd=0, font="bold", padx=10, pady=10, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=BUTTON_BACKGROUND_HOVER,
                         activeforeground=BUTTON_FOREGROUND_HOVER, 
                         highlightthickness=0, 
                         text=text,
                         command=command)
        master.pack(expand=True, fill=f"x")
        self.pack(side="bottom", anchor="se")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<B1-Motion>", lambda event, master=master:self.on_motion(event,master))

    def on_enter(self, event):
        self["bg"] = BUTTON_BACKGROUND_HOVER

    def on_leave(self, event):
        self["bg"] = BUTTON_BACKGROUND

    def on_motion(self, event, master):
        abs_x = master.winfo_pointerx() - master.winfo_rootx() + 10
        abs_y = master.winfo_pointery() - master.winfo_rooty() + 10
        abs_x = abs_x if abs_x < master.winfo_screenwidth() else master.winfo_screenwidth()
        abs_y = abs_y if abs_y < master.winfo_screenheight() else master.winfo_screenheight()
        
        if abs_x >0 and abs_y >0:
            master.master.geometry("%sx%s" % (abs_x,abs_y))
        

class MyCanvas(tk.Canvas):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, bg=WINDOW_BACKGROUND,
                         highlightthickness=0)

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", lambda event, master=master:self.on_move(event,master))
        
        self.close_button = CloseButton(self, text=f"\u274C", command=master.destroy)
        self.resize_button = ResizeButton(self, text=f"\u21F2")

    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def on_release(self, event):
        pass

    def on_move(self, event, master):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        min_x = 0
        min_y = 0
        max_x = master.winfo_screenwidth() - master.winfo_width()
        max_y = master.winfo_screenheight() - master.winfo_height()
        x = min_x if x < min_x else x
        y = min_y if y < min_y else y
        x = x if x < max_x else max_x
        y = y if y < max_y else max_y
        self.master.geometry(f"+{x}+{y}")


# --- main ---

root = tk.Tk()
# turns off title bar, geometry
root.overrideredirect(True)

# set new geometry
w=root.winfo_screenwidth()
root.geometry(f"{w}x100+0+0")

# a canvas for the main area of the window
window = MyCanvas(root)

# pack the widgets
window.pack(expand=True, fill="both")

root.attributes("-topmost",True)

root.config(cursor="none")

root.mainloop()