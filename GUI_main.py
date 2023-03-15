from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog
from GUI_texture_synthesis import GUI_texture_synthesis
from GUI_texture_transfer import GUI_texture_transfer

class menu_frame:
    def __init__(self, master):
        self.master = master
        self.font_style = tkFont.Font(family="Cousine", weight="bold", size=13)
        self.synthesis = GUI_texture_synthesis(master)
        self.transfer = GUI_texture_transfer(master)
        self.color_bg = "#D9D9D9"
        self.color_clicked = '#2CDE3E'
        self.frame = Frame(master=self.master, width=340,
                           height=200, background="#FFEAE1")
        self.frame.place(x=0, y=0)
        self.create_buttons()

    def create_buttons(self):
        self.button1 = Button(
            self.frame, text="Texture Synthesis", font=self.font_style, command=self.func1)
        self.button1.config(bg=self.color_bg)
        self.button1.place(x=20, y=20, width=300, height=40)

        self.button2 = Button(
            self.frame, text="Texture Transfer", font=self.font_style, command=self.func2)
        self.button2.config(bg=self.color_bg)
        self.button2.place(x=20, y=80, width=300, height=40)

        self.button3 = Button(
            self.frame, text="Both", font=self.font_style, command=self.func3)
        self.button3.config(bg=self.color_bg)
        self.button3.place(x=20, y=140, width=300, height=40)

    def func1(self):
        self.button1.config(bg=self.color_clicked)
        self.button2.config(bg=self.color_bg)
        self.button3.config(bg=self.color_bg)
        self.synthesis()

    def func2(self):
        self.button1.config(bg=self.color_bg)
        self.button2.config(bg=self.color_clicked)
        self.button3.config(bg=self.color_bg)
        self.transfer()

    def func3(self):
        self.button1.config(bg=self.color_bg)
        self.button2.config(bg=self.color_bg)
        self.button3.config(bg=self.color_clicked)


if __name__ == "__main__":
    window = Tk()
    window.title('Project IMP301')
    window.geometry('1024x720')

    menu = menu_frame(window)

    window.mainloop()