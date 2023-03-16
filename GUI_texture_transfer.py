import glob
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import ImageTk, Image
from texture_Transfer import main
import cv2

class GUI_texture_transfer:
    txt1, txt2 = None, None
    k = 2
    alpha = 1.2
    beta = -20
    root_path = None
    filter_path = None
    out_image = None
    list_output_image = []

    def __init__(self, master):
        self.master = master
        self.font_style = tkFont.Font(family="Cousine", weight="bold", size=13)
        self.color_bg = "#D9D9D9"

    def __call__(self):
        # container
        self.input1_frame = Frame(master=self.master, width=342,
                                  height=360, background="#D9D9D9")
        self.input1_frame.place(x=340, y=0)
        self.input2_frame = Frame(master=self.master, width=342,
                                  height=360, background="#CBE4DE")
        self.input2_frame.place(x=682, y=0)
        self.action_frame = Frame(master=self.master, width=340,
                                  height=160, background="#B7ABFF")
        self.action_frame.place(x=0, y=200)
        self.output_frame = Frame(
            master=self.master, width=1024, height=360, background="#0E8388")
        self.output_frame.place(x=0, y=360)

        # Create a canvas and scrollbar
        self.canvas = Canvas(self.output_frame, width=1024, height=300)
        self.canvas.place(x=0, y=50)
        self.scrollbar = Scrollbar(
            self.output_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")
        self.show_image_in_canvas()

        # buttons
        self.process_button = Button(
            self.action_frame, text="Process", font=self.font_style, command=self.process)
        self.process_button.config(bg=self.color_bg)
        self.process_button.place(x=20, y=12, width=300, height=40)

        self.save_image_button = Button(
            self.action_frame, text="Save lastest output image", font=self.font_style, command=self.save_image)
        self.save_image_button.config(bg=self.color_bg)
        self.save_image_button.place(x=20, y=64, width=300, height=40)

        self.save_image_button = Button(
            self.action_frame, text="Clear all", font=self.font_style, command=self.clear_output)
        self.save_image_button.config(bg=self.color_bg)
        self.save_image_button.place(x=20, y=116, width=300, height=40)

        output_title = Label(self.output_frame, text="RESULT SEQUENCE",
                             font=self.font_style, background="#0E8388")
        output_title.place(x=0, y=0, width=1024, height=40)
        self.create_components()

    def create_components(self):
        # button1 & image window 1
        self.button1 = Button(
            self.input1_frame, text="Input image Texture", font=self.font_style, command=self.open_file_1)
        self.button1.config(bg=self.color_bg)
        self.button1.place(x=0, y=0, width=342, height=40)
        self.image_window_1 = Frame(self.input1_frame)
        self.image_window_1.pack()
        self.image_window_1.place(x=10, y=50, width=322, height=260)

        # button2 & image window 2
        self.button2 = Button(
            self.input2_frame, text="Input image for Texture Transfer", font=self.font_style, command=self.open_file_2)
        self.button2.config(bg=self.color_bg)
        self.button2.place(x=0, y=0, width=342, height=40)
        self.image_window_2 = Frame(self.input2_frame)
        self.image_window_2.pack()
        self.image_window_2.place(x=10, y=50, width=322, height=260)

        # texts
        text0 = Label(self.master, text="K",
                      font=self.font_style)
        text0.place(x=340, y=320, width=114, height=40)
        text1 = Label(self.master, text="Alpha",
                      font=self.font_style)
        text1.place(x=340+114*2, y=320, width=114, height=40)
        text2 = Label(self.master, text="Beta", font=self.font_style)
        text2.place(x=340+114*4, y=320, width=114, height=40)

        # text boxs
        text = StringVar()
        text.set(f"{self.k}")
        self.txt0 = Entry(self.master, font=self.font_style, textvariable=text)
        self.txt0.place(x=340+114*1, y=320, width=114, height=40)
        text = StringVar()
        text.set(f"{self.alpha}")
        self.txt1 = Entry(self.master, font=self.font_style, textvariable=text)
        self.txt1.place(x=340+114*3, y=320, width=114, height=40)
        text = StringVar()
        text.set(f"{self.beta}")
        self.txt2 = Entry(self.master, font=self.font_style, textvariable=text)
        self.txt2.place(x=340+114*5, y=320, width=114, height=40)

    def open_file_1(self):
        self.filter_path = filedialog.askopenfilename(
            initialdir=".\Inputs\Texture")
        image = Image.open(self.filter_path)
        image.thumbnail((322, 260))
        image_tk = ImageTk.PhotoImage(image)
        self.image_window_1 = Frame(self.input1_frame)
        self.image_window_1.pack()
        self.image_window_1.place(x=10, y=50, width=322, height=260)
        label = Label(self.image_window_1)
        label.image = image_tk
        label.configure(image=image_tk)
        label.pack()

    def open_file_2(self):
        self.root_path = filedialog.askopenfilename(
            initialdir=".\Images")
        image = Image.open(self.root_path)
        image.thumbnail((322, 260))
        image_tk = ImageTk.PhotoImage(image)
        self.image_window_2 = Frame(self.input2_frame)
        self.image_window_2.pack()
        self.image_window_2.place(x=10, y=50, width=322, height=260)
        label = Label(self.image_window_2)
        label.image = image_tk
        label.configure(image=image_tk)
        label.pack()

    def process(self):
        try:
            self.k = float(self.txt0.get())
        except:
            pass
        try:
            self.alpha = float(self.txt1.get())
        except:
            pass
        try:
            self.beta = float(self.txt2.get())
        except:
            pass

        self.out_image = main.blending(
            root_path=self.root_path, filter_path=self.filter_path, k=self.k, alpha=self.alpha, beta=self.beta)
        img = self.out_image.copy()
        img = cv2.putText(img, f'k = {self.k}', (
            10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        img = cv2.putText(img, f'alpha = {self.alpha}', (
            10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        img = cv2.putText(img, f'beta = {self.beta}', (
            10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imwrite(filename="tmp.png", img=img)
        self.show_output()

    def save_image(self):
        cv2.imwrite(
            filename=f"outputs/{len(glob.glob('outputs/*'))}.png", img=self.out_image)

    def clear_output(self):
        self.list_output_image = []
        self.__call__()

    def show_output(self):
        image = Image.open("tmp.png")
        self.list_output_image.append(image)
        self.show_image_in_canvas()
        
    def show_image_in_canvas(self):
        self.image_container = Frame(self.canvas)
        self.image_container.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window(
            (0, 0), window=self.image_container, anchor="center", height=300)
        for img in self.list_output_image:
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            label = Label(self.image_container, image=photo, height= 300, width=300)
            label.image = photo
            label.pack(side="left")
