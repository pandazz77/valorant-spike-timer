import tkinter as tk

class Overlay:
    def __init__(self,root=tk.Tk()):
        self.root = root
        self.x = 0
        self.y = 0
        self.set_geometry(None,None)
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.fg = "green3"
        self.bg = "grey19"
        self.label = tk.Label(self.frame,font=("Consolas",14),text="",fg=self.fg,bg=self.bg)
        self.root.overrideredirect(True)
        self.root.lift()
        self.root.wm_attributes("-topmost",True)
        self.label.grid(column=0, row=0)
        self.visible = False

    def loop(self):
        self.root.mainloop()

    def set_label(self,text):
        if self.visible: self.show_label()
        else: self.visible = True
        self.label.configure(text=text,fg=self.fg,bg=self.bg)
    
    def set_geometry(self,x,y):
        if x: self.x = x
        if y: self.y = y
        self.root.geometry("+%d+%d" % (self.x,self.y))

    def hide_label(self):
        if self.visible:
            self.root.attributes("-alpha",0)
            self.visible = False

    def show_label(self):
        self.visible = True
        self.root.attributes("-alpha",1)