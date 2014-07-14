import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
from l_systems import Lindenmayer, LindenmayerException


## To fill filebrowswer
from os import makedirs
from os.path import expanduser, isdir, basename, join
from glob import glob
    
class Main(tk.Frame):

    w = 600
    h = 600
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.parent.title("L System Equations Rendering Tool for Tkinter")

        ### variables ###
        self.iterations = tk.StringVar()
        self.angle = tk.StringVar()
        self.axiom = tk.StringVar()
        self.rule1 = tk.StringVar()
        self.rule2 = tk.StringVar()
        self.rule3 = tk.StringVar()
        self.rule4 = tk.StringVar()
        self.constants = tk.StringVar()

        self.color1 = "#000000"
        self.color2 = "#dd0000"
        self.color3 = "#00dd00"
        self.color4 = "#0000dd"

        self.lsf_dir = expanduser(join("~", "lsf-files"))
        if not isdir(self.lsf_dir):
            from shutil import copytree
            from os.path import dirname
            examples = join(dirname(__file__),"examples")
            copytree(examples, self.lsf_dir)

        self.entries = tk.Frame(self)
        self.entries.grid(row=0, column=0, sticky=tk.N)
        ### Labels ###
        tk.Label(self.entries, text="Settings", font="Helvetica 14 bold").grid(column=0, row=0, sticky=tk.W)
        tk.Label(self.entries, text="Iterations").grid(column=0,row=1, padx=5, pady=5)
        tk.Label(self.entries, text="angle").grid(column=0,row=2, padx=5, pady=5)
        tk.Label(self.entries, text="axiom").grid(column=0,row=3, padx=5, pady=5)
        tk.Label(self.entries, text="rule1").grid(column=0,row=4, padx=5, pady=5)
        tk.Label(self.entries, text="rule2").grid(column=0, row=5, padx=5, pady=5)
        tk.Label(self.entries, text="rule3").grid(column=0, row=6, padx=5, pady=5)
        tk.Label(self.entries, text="rule4").grid(column=0, row=7, padx=5, pady=5)
        tk.Label(self.entries, text="constants").grid(column=0, row=8, padx=5, pady=5)
        tk.Label(self.entries, text="Color Values", font="Helvetica 14 bold").grid(column=0, row=9, padx=5, pady=5)
        tk.Label(self.entries, text="default (color 1):").grid(column=0, row=10, padx=5, pady=5)
        tk.Label(self.entries, text="color 2:").grid(column=0, row=11, padx=5, pady=5)
        tk.Label(self.entries, text="color 3:").grid(column=0, row=12, padx=5, pady=5)
        tk.Label(self.entries, text="color 4:").grid(column=0, row=13, padx=5, pady=5)

        
        ### Entries ###
        tk.Entry(self.entries, textvariable=self.iterations).grid(column=1,row=1)
        tk.Entry(self.entries, textvariable=self.angle).grid(column=1,row=2)
        tk.Entry(self.entries, textvariable=self.axiom).grid(column=1,row=3)
        tk.Entry(self.entries, textvariable=self.rule1).grid(column=1,row=4)
        tk.Entry(self.entries, textvariable=self.rule2).grid(column=1, row=5)
        tk.Entry(self.entries, textvariable=self.rule3).grid(column=1, row=6)
        tk.Entry(self.entries, textvariable=self.rule4).grid(column=1, row=7)
        tk.Entry(self.entries, textvariable=self.constants).grid(column=1, row=8)
        ## Color settings
        self.c1_label = tk.Label(self.entries, text=self.color1, bg=self.color1);self.c1_label.grid(column=1, row=10)
        self.c2_label = tk.Label(self.entries, text=self.color2, bg=self.color2);self.c2_label.grid(column=1, row=11)
        self.c3_label = tk.Label(self.entries, text=self.color3, bg=self.color3);self.c3_label.grid(column=1, row=12)
        self.c4_label = tk.Label(self.entries, text=self.color4, bg=self.color4);self.c4_label.grid(column=1, row=13)

        self.c1_label.bind("<Button-1>", lambda _: self.pick_color("color1", self.c1_label))
        self.c2_label.bind("<Button-1>", lambda _: self.pick_color("color2", self.c2_label))
        self.c3_label.bind("<Button-1>", lambda _: self.pick_color("color3", self.c3_label))
        self.c4_label.bind("<Button-1>", lambda _: self.pick_color("color4", self.c4_label))

        ### Function Buttons ###
        self.buttons = tk.Frame(self)
        self.buttons.grid(row=1, column=1)
        tk.Button(self.buttons, text="render", command=self.render_image).grid(column=0, row=0)
        tk.Button(self.buttons, text="save", command=self.save_to_file).grid(column=1, row=0)
        tk.Button(self.buttons, text="load", command=self.load_from_file).grid(column=2, row=0)
        tk.Button(self.buttons, text="save image", command=self.save_image).grid(column=3, row=0)
        
        ### File List ###
        self.right = tk.Frame(self)
        self.right.grid(row=0, column=2)
        self.filebrowser = tk.Listbox(self.right)
        self.filebrowser.grid(row=0, column=0)
        self.filebrowser.bind("<<ListboxSelect>>", self.load_selected_file)
        self.fill_file_browser()

        ### Canvas ###
        self.cv = tk.Canvas(self, width=self.w, height=self.h, bg='white')
        self.cv.grid(column=1, row=0)

        self.grid()

    def load_selected_file(self, event):
        sel = self.filebrowser.curselection()
        fpath = self.files[self.filebrowser.get(sel[0])]
        self.load_from_file(fpath)

    def fill_file_browser(self):
        self.files = {}
        print("globbing",join(self.lsf_dir, "*.lsf"))
        for f in glob(join(self.lsf_dir, "*.lsf")):
            fname = basename(f)
            self.files[fname] = f
            self.filebrowser.insert(0,fname)

    def pick_color(self, colorname, label):

        old_color = getattr(self, colorname)

        # discard (r,g,b) and use #rrggbb instead
        _, new_color = tk.colorchooser.askcolor(initialcolor=old_color, title="Pick a color")
        
        setattr(self, colorname, new_color)

        label['text'] = new_color
        label['bg']   = new_color

    def save_to_file(self):

        fn = tk.filedialog.asksaveasfilename(initialdir=self.lsf_dir,
                                             filetypes=(('L-System Formula File','*.lsf'), ('All files', '*.*')))

        if fn:
            if not fn.endswith(".lsf"):
                fn += ".lsf"

        
        with open(fn,"w") as f:
            f.write("\n".join((self.iterations.get(),
                              self.angle.get(),
                              self.axiom.get(),
                              self.rule1.get(),
                              self.rule2.get(),
                              self.rule3.get(),
                              self.rule4.get(),
                              self.constants.get(),
                               "EOF")))

    def load_from_file(self, fname=None):
        if not fname:
            fname = tk.filedialog.askopenfilename(initialdir=self.lsf_dir,
                                                  filetypes = (("L-System Formula","*.lsf"),("all files","*.*")))

        with open(fname, "r") as f:

            x = f.readlines()
            print(x)
            self.iterations.set(x[0].strip())
            self.angle.set(x[1].strip())
            self.axiom.set(x[2].strip())
            self.rule1.set(x[3].strip())
            self.rule2.set(x[4].strip())
            self.rule3.set(x[5].strip())
            self.rule4.set(x[6].strip())
            self.constants.set(x[7].strip())

        self.render_image()

    def save_image(self):

        with tk.filedialog.asksaveasfile(filetypes=(('Jpeg Image','*.jpg;*.jpeg;*.JPEG;*.JPG'),
                                                    ('Bitmap Image','*.bmp'),
                                                    ('Png Image','*.png'))) as f:
            self.active_pimage.save(f)

        

    def get_rules(self):
        rules = dict()
        
        for r in ("rule1","rule2","rule3","rule4"):
            text = getattr(self,r).get()
            if ":" in text:
                kv = text.split(":")
                rules[kv[0]] = "".join(kv[1:])

        return rules

    def render_image(self):
        temp = Image.new("RGB", (self.w, self.h), (255,255,255))
        lin = Lindenmayer(temp)

        try:

            lin.init(
                iterations = int(self.iterations.get()),
                angle      = int(self.angle.get()),
                axiom      = self.axiom.get(),
                rules      = self.get_rules(),
                constants  = self.constants.get(),
                color1     = self.color1,
                color2     = self.color2,
                color3     = self.color3,
                color4     = self.color4
            )

        except LindenmayerException as e:

            tk.messagebox.showwarning("Bir hata oluştu",e)
            return

        self.active_pimage = temp # Use this to save to file

        self.active_image = ImageTk.PhotoImage(temp)
        self.cv.create_image((self.w/2,self.h/2), image=self.active_image)

    def fill_entries(self, it="", ang="", cons="", axi="", r1="", r2="", r3="", r4=""):

        self.iterations.set(it)
        self.angle.set(ang)
        self.constants.set(cons)
        self.axiom.set(axi)
        self.rule1.set(r1)
        self.rule2.set(r2)
        self.rule3.set(r3)
        self.rule4.set(r4)

    def run(self):

        self.parent.mainloop()

if __name__ == "__main__":

    root = tk.Tk()
    app = Main(root)
    root.bind("<Return>", lambda _: app.render_image())
    app.run()
