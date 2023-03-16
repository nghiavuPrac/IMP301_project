import glob
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import ImageTk, Image
import cv2
from texture_Synthesis.main import texture_handler
import time
import numpy as np


class GUI_texture_synthesis():
    txt1, txt2, txt3, txt4 = None, None, None, None
    blocksize = 50
    overlap = 10
    scale = 2
    tolerance = 0.1
    input_image_path = None
    input_image = None
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
        self.canvas.configure(xscrollcommand=self.scrollbar.set, bg='white')
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
        # button1
        self.button1 = Button(
            self.input1_frame, text="Input image for Texture Synthesis", font=self.font_style, command=self.open_file)
        self.button1.config(bg=self.color_bg)
        self.button1.place(x=0, y=0, width=342, height=40)

        # image window
        self.image_window = Frame(self.input1_frame)
        self.image_window.pack()
        self.image_window.place(x=10, y=50, width=322, height=300)

        # texts
        text1 = Label(self.input2_frame, text="Blocksize",
                      font=self.font_style)
        text1.place(x=18, y=40, width=130, height=40)
        text2 = Label(self.input2_frame, text="Overlap", font=self.font_style)
        text2.place(x=18, y=120, width=130, height=40)
        text3 = Label(self.input2_frame, text="Scale", font=self.font_style)
        text3.place(x=18, y=200, width=130, height=40)
        text4 = Label(self.input2_frame, text="Tolerance",
                      font=self.font_style)
        text4.place(x=18, y=280, width=130, height=40)

        # text boxs
        self.txt1 = Entry(self.input2_frame, font=self.font_style)
        self.txt1.place(x=148, y=40, width=170, height=40)
        self.txt2 = Entry(self.input2_frame, font=self.font_style)
        self.txt2.place(x=148, y=120, width=170, height=40)
        self.txt3 = Entry(self.input2_frame, font=self.font_style)
        self.txt3.place(x=148, y=200, width=170, height=40)
        self.txt4 = Entry(self.input2_frame, font=self.font_style)
        self.txt4.place(x=148, y=280, width=170, height=40)

    def open_file(self):
        self.input_image_path = filedialog.askopenfilename(
            initialdir=".\Inputs\Texture")

        self.input_image = Image.open(self.input_image_path)
        img = self.input_image.copy()

        #conver image to numpy array
        self.img_np = np.array(self.input_image.convert('RGB'))

        img.thumbnail((322, 300))
        image_tk = ImageTk.PhotoImage(img)
        self.image_window = Frame(self.input1_frame)
        self.image_window.pack()
        self.image_window.place(x=10, y=50, width=322, height=300)
        label = Label(self.image_window)
        label.image = image_tk
        label.configure(image=image_tk)
        label.pack()

    # lay blocksize = shape image -10 de chay cho le
    def cheating(self):
        blocksize = self.img_np.shape[0]- 10
        overlap = blocksize // 3
        return blocksize, overlap

    def process(self):
        default = True
        try:
            self.blocksize = int(self.txt1.get())
            default = False
        except:
            pass
        try:
            self.overlap = int(self.txt2.get())
            default = False
        except:
            pass
        try:
            self.scale = int(self.txt3.get())
        except:
            pass
        try:
            self.tolerance = float(self.txt4.get())
        except:
            pass

        if default:
            self.blocksize, self.overlap = self.cheating()

        handle = texture_handler(self.img_np, self.blocksize,
                                 self.overlap, self.scale, self.tolerance)
        start = time.time()
        self.out_image = handle.synthesis()
        end = time.time()
        print('Execution time:', (end - start), 'seconds')
        self.show_output()

    def get_concat_h(self, im1, im2):
        dst = Image.new('RGB', (im1.width +  im2.width + 50, im2.height), color=(255,255,255))
        dst.paste(im1, (0, im2.height - im1.height))
        dst.paste(im2, (im1.width + 50, 0))
        return dst
    
    def save_image(self):
        self.out_image.save(f"outputs/{len(glob.glob('outputs/*'))}.jpg")

    def clear_output(self):
        self.list_output_image = []
        self.__call__()

    def show_output(self):
        self.list_output_image.append(self.get_concat_h(self.input_image, self.out_image))
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