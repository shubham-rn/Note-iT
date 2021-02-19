from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import colorchooser
import os
from copy import deepcopy
import webbrowser as wb
import datetime
import time
import speech_recognition as sr
import pyttsx3
import random
from plyer import notification
import threading
# from tkcalendar import *
import sqlite3


class Window(Tk):

    file = None

    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Untitled - NOTE-iT")
        self.wm_iconbitmap("ai1.ico")
        self.geometry("580x644")

        self.create_menubar()



    def createbutton(self, inptext):
        Button(text=inptext, command=self.click).pack()

    def create_menubar(self):
        # Add TextArea
        self.TextArea = Text(self, font="comicscanms 13", undo=True)
        # file = None
        self.TextArea.pack(expand=True, fill=BOTH)

        # self.MenuBar = Menu(self)
        # FileMenu = Menu(self.MenuBar, tearoff=0)
        # FileMenu.add_command(label="New")
        # self.MenuBar.add_cascade(label="File", menu=FileMenu)
        #
        # self.config(menu=self.MenuBar)

        # Lets create a menubar
        self.MenuBar = Menu(self)

        # File Menu Starts
        FileMenu = Menu(self.MenuBar, tearoff=0)
        # To open new file
        FileMenu.add_command(label="New", command=self.newFile)
        # FileMenu.add_command(label="New Window", command=newWindow)
        # To Open already existing file
        FileMenu.add_command(label="Open", command=self.openFile)

        # To save the current file

        FileMenu.add_command(label="Save", command=self.saveFile)
        FileMenu.add_separator()
        FileMenu.add_command(label="Exit", command=self.quitApp)
        self.MenuBar.add_cascade(label="File", menu=FileMenu)
        # File Menu ends
       # Eself.dit Menu Starts
        EditMenu = Menu(self.MenuBar, tearoff=0)
        # To give a feature of cut, copy and paste
        EditMenu.add_command(label="undo", command=self.TextArea.edit_undo)
        # EditMenu.add_command(label="redo", command=TextArea.edit_redo)
        EditMenu.add_separator()
        EditMenu.add_command(label="Cut", command=self.cut)
        EditMenu.add_command(label="Copy", command=self.copyy)
        EditMenu.add_command(label="Paste", command=self.paste)
        EditMenu.add_command(label="delete", command=self.delete)
        EditMenu.add_separator()
        EditMenu.add_command(label="Search with Bing", command=self.searchBing)
        EditMenu.add_separator()
        EditMenu.add_command(label="Select All", command=self.selectAll)
        EditMenu.add_command(label="Date/Time", command=self.currentDate)

        self.MenuBar.add_cascade(label="Edit", menu=EditMenu)

        # Edit Menu Ends

        # Format menu starts
        FormatMenu = Menu(self.MenuBar, tearoff=0)
        # FormatMenu.add_command(label="Font")
        FormatMenu.add_command(label="Text Color", command=self.chooseColor_fg)
        FormatMenu.add_command(label="Background Color", command=self.chooseColor_bg)
        self.MenuBar.add_cascade(label="Format", menu=FormatMenu)
        # Format menu ends

        # Help Menu Starts
        HelpMenu = Menu(self.MenuBar, tearoff=0)
        HelpMenu.add_command(label="View Help", command=self.viewHelp)
        HelpMenu.add_separator()
        HelpMenu.add_command(label="About NOTE-iT", command=self.about)
        self.MenuBar.add_cascade(label="Help", menu=HelpMenu)

        # Help Menu Ends

        # options menu starts
        OptionMenu = Menu(self.MenuBar, tearoff=0)
        ModeMenu = Menu(OptionMenu, tearoff=0)
        ModeMenu.add_command(label="dark", command=self.setDark)
        ModeMenu.add_command(label="light", command=self.setLight)
        OptionMenu.add_cascade(label="Mode", menu=ModeMenu)
        # OptionMenu.add_command(label="set reminder", command=set_reminder)
        self.MenuBar.add_cascade(label="Option", menu=OptionMenu)
        # option menu ends

        self.config(menu=self.MenuBar)

        self.ScrollV = Scrollbar(self.TextArea)
        self.ScrollV.pack(side=RIGHT, fill=Y)
        self.ScrollV.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=self.ScrollV.set)

# ---------------------------------------------------------------------------------------------------------------------

    def newFile(self):
        self.title("Untitled - NOTE-iT")
        Window.file = None
        self.TextArea.delete(1.0, END)

    def newWindow(self):
        w1 = Window()
        w1.mainloop()

    def openFile(self):
        Window.file = askopenfilename(defaultextension=".txt",
                               filetypes=[("All Files", "*.*"),
                                          ("Text Documents", "*.txt")])
        if Window.file == "":
            Window.file = None
        else:
            self.title(os.path.basename(Window.file) + " - NOTE-iT")
            self.TextArea.delete(1.0, END)
            f = open(Window.file, "r")                                      # check
            self.TextArea.insert(1.0, f.read())
            f.close()

    def saveFile(self):
        if Window.file == None:
            Window.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
            if Window.file == "":
                Window.file = None

            else:
                # Save as a new file
                f = open(Window.file, "w")
                f.write(self.TextArea.get(1.0, END))
                f.close()

                self.title(os.path.basename(Window.file) + " - NOTE-iT")
                print("File Saved")
        else:
            # Save the file
            f = open(Window.file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

    def quitApp(self):
        self.destroy()

    def cut(self):
        self.TextArea.event_generate(("<<Cut>>"))

    def copyy(self):
        self.TextArea.event_generate(("<<Copy>>"))

    def paste(self):
        self.TextArea.event_generate(("<<Paste>>"))

    def delete(self):
        self.TextArea.delete(1.0, END)


    def selectAll(self, event=None):
        self.TextArea.tag_add('sel', 1.0, END)

    def currentDate(self):
        now = datetime.datetime.now()
        a = str(now.strftime("%y-%m-%d %H:%M %p"))
        self.TextArea.insert(INSERT, a)

    def chooseColor_fg(self):
        my_color = colorchooser.askcolor()[1]
        self.TextArea["fg"] = my_color
        self.TextArea.config(insertbackground=my_color)
        return my_color

    def chooseColor_bg(self):
        my_color = colorchooser.askcolor()[1]
        self.TextArea["bg"] = my_color
        return my_color

    def searchBing(self):
        wb.open("https://www.bing.com/?scope=web&mkt=en-IN")

    def viewHelp(self):
        wb.open("https://github.com/shubham-rn/Note-iT/blob/master/README.md")
        # wb.open("D:\html programs\html project\project1\index.html")


    def about(self):
        # tmsg.showinfo("About NOTE-iT", "NOTE-iT IS UNDER DEVELOPMENT")
        abt = Tk()
        abt.title("About Note-iT")
        abt.geometry("400x100")
        l1 = Label(abt, text="Note-iT version 1.0.1")
        l2 = Label(abt, text="© Boss Tech 2020")
        l1.pack()
        l2.pack()
        b1 = Button(abt, text="Ok", command=abt.destroy)
        b1.pack(side=BOTTOM, anchor="se")
        abt.mainloop()

    def setDark(self):
        # global f1
        self.TextArea["bg"] = "black"
        self.TextArea["fg"] = "white"
        self.TextArea.config(insertbackground="white")

    def setLight(self):
        self.TextArea["background"] = "white"
        self.TextArea["foreground"] = "black"
        self.TextArea.config(insertbackground="black")







if __name__ == '__main__':
    w = Window()

    w.mainloop()

