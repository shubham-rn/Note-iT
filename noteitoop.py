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






if __name__ == '__main__':
    w = Window()

    w.mainloop()

