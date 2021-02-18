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
    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Untitled - NOTE-iT")
        self.wm_iconbitmap("ai1.ico")
        self.geometry("580x644")

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
        FileMenu.add_command(label="New")#, command=newFile)
        # FileMenu.add_command(label="New Window", command=newWindow)
        # To Open already existing file
        FileMenu.add_command(label="Open")#, command=openFile)

        # To save the current file

        FileMenu.add_command(label="Save")#, command=saveFile)
        FileMenu.add_separator()
        FileMenu.add_command(label="Exit")#, command=quitApp)
        self.MenuBar.add_cascade(label="File", menu=FileMenu)
        # File Menu ends

        # Edit Menu Starts
        EditMenu = Menu(self.MenuBar, tearoff=0)
        # To give a feature of cut, copy and paste
        EditMenu.add_command(label="undo")#, command=TextArea.edit_undo)
        # EditMenu.add_command(label="redo", command=TextArea.edit_redo)
        EditMenu.add_separator()
        EditMenu.add_command(label="Cut")#, command=cut)
        EditMenu.add_command(label="Copy")#, command=copyy)
        EditMenu.add_command(label="Paste")#, command=paste)
        EditMenu.add_command(label="delete")#, command=delete)
        EditMenu.add_separator()
        EditMenu.add_command(label="Search with Bing")#, command=searchBing)
        EditMenu.add_separator()
        EditMenu.add_command(label="Select All")#, command=selectAll)
        EditMenu.add_command(label="Date/Time")#, command=currentDate)

        self.MenuBar.add_cascade(label="Edit", menu=EditMenu)

        # Edit Menu Ends

        # Format menu starts
        FormatMenu = Menu(self.MenuBar, tearoff=0)
        # FormatMenu.add_command(label="Font")
        FormatMenu.add_command(label="Text Color")#, command=chooseColor_fg)
        FormatMenu.add_command(label="Background Color")#, command=chooseColor_bg)
        self.MenuBar.add_cascade(label="Format", menu=FormatMenu)
        # Format menu ends

        # Help Menu Starts
        HelpMenu = Menu(self.MenuBar, tearoff=0)
        HelpMenu.add_command(label="View Help")#, command=viewHelp)
        HelpMenu.add_separator()
        HelpMenu.add_command(label="About NOTE-iT")#, command=about)
        self.MenuBar.add_cascade(label="Help", menu=HelpMenu)

        # Help Menu Ends

        # options menu starts
        OptionMenu = Menu(self.MenuBar, tearoff=0)
        ModeMenu = Menu(OptionMenu, tearoff=0)
        ModeMenu.add_command(label="dark")#, command=setDark)
        ModeMenu.add_command(label="light")#, command=setLight)
        OptionMenu.add_cascade(label="Mode", menu=ModeMenu)
        # OptionMenu.add_command(label="set reminder", command=set_reminder)
        self.MenuBar.add_cascade(label="Option", menu=OptionMenu)
        # option menu ends

        self.config(menu=self.MenuBar)

        self.ScrollV = Scrollbar(self.TextArea)
        self.ScrollV.pack(side=RIGHT, fill=Y)
        self.ScrollV.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=self.ScrollV.set)

    def createbutton(self, inptext):
        Button(text=inptext, command=self.click).pack()

    def click(self):
        print("button clicked")



if __name__ == '__main__':
    w = Window()

    w.mainloop()

