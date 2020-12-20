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
from tkcalendar import *
import sqlite3


# global variable declaration
is_speaking = False
r = None
audio = None
engine = pyttsx3.init()
engine.setProperty('rate', 125)
tasks = []

conn = sqlite3.connect("listboxapp.db")
c = conn.cursor()

def newFile():
    global file
    root.title("Untitled - NOTE-iT")
    file = None
    TextArea.delete(1.0, END)

def newWindow():
    pass

def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - NOTE-iT")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()

def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            # Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - NOTE-iT")
            print("File Saved")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp():
    root.destroy()

def cut():
    TextArea.event_generate(("<<Cut>>"))

def copyy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

def delete():
    TextArea.delete(1.0, END)

def selectAll(event=None):
    global TextArea
    TextArea.tag_add('sel', 1.0, END)


def currentDate():
    now = datetime.datetime.now()
    a = str(now.strftime("%y-%m-%d %H:%M %p"))
    TextArea.insert(INSERT, a)

def chooseColor_fg():
    my_color = colorchooser.askcolor()[1]
    global TextArea
    TextArea["fg"] = my_color
    TextArea.config(insertbackground=my_color)
    return my_color

def chooseColor_bg():
    my_color = colorchooser.askcolor()[1]
    global TextArea
    TextArea["bg"] = my_color
    return my_color

def searchBing():
    wb.open("https://www.bing.com/?scope=web&mkt=en-IN")

def viewHelp():

    # wb.open("https://www.bing.com/search?q=get+help+with+notepad+in+windows+10&filters=guid:%224466414-en-dia%22%20lang:%22en%22&form=T00032&ocid=HelpPane-BingIA")
    # wb.open("https://github.com/shubham-rn/Note-iT/blob/master/README.md")
    wb.open("file:///C:/Users/ShubhamN/Desktop/test.html")

def about():
    # tmsg.showinfo("About NOTE-iT", "NOTE-iT IS UNDER DEVELOPMENT")
    abt = Tk()
    abt.title("About Note-iT")
    abt.geometry("400x100")
    l1 = Label(abt, text="Note-iT version 1.0.1")
    l2 = Label(abt, text="")
    l1.pack()
    l2.pack()
    b1 = Button(abt, text="Ok", command=abt.destroy)
    b1.pack(side=BOTTOM, anchor="se")
    abt.mainloop()

def setDark():
    global TextArea
    global f1
    TextArea["bg"] = "black"
    TextArea["fg"] = "white"
    TextArea.config(insertbackground="white")

def setLight():
    global TextArea
    TextArea["background"] = "white"
    TextArea["foreground"] = "black"
    TextArea.config(insertbackground="black")

def callstart(event):
    t1 = threading.Thread(target=startSpeak)
    t1.start()

def callstop(event):
    # t2 = threading.Thread(target=stopSpeak)
    # t2.start()
    stopSpeak()

def startSpeak():
    global is_speaking
    global r
    global audio
    is_speaking = True
    # print("speaking")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("speak anything")
        engine.runAndWait()
        audio = r.listen(source)

def stopSpeak():
    global is_speaking
    global r
    is_speaking = False
    try:
        text = ' ' + r.recognize_google(audio)
        TextArea.insert(INSERT, text)
    except:
        engine.say("Sorry could not recognize what you said")
        engine.runAndWait()
    # print("stopped speaking")

def callstt():
    # engine.say("speak anything")
    # engine.runAndWait()
    t1 = threading.Thread(target=stt)
    t1.start()


def stt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = ' ' + r.recognize_google(audio)
            # print("You said : {}".format(text))
            TextArea.insert(INSERT, text)
        except:
            # print("Sorry could not recognize what you said")
            engine.say("Sorry could not recognize what you said")
            engine.runAndWait()


def startRead():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(TextArea.get("1.0", END))
    engine.runAndWait()


def main():
    pass

# create functions

def update_listbox():
    # clear the current list
    clear_listbox()
    # populate the listbox
    for task in tasks:
        lb_tasks.insert(END, task)

def clear_listbox():
    lb_tasks.delete(0, END)


def add_task():
    conn = sqlite3.connect("listboxapp.db")
    c = conn.cursor()

   # get the task to add
    task = txt_input.get()

    # make sure the task is not empty
    if task != "":
        c.execute("INSERT INTO listbox VALUES(:task)",
                  {
                      'task': txt_input.get()
                  })
        conn.commit()
        conn.close()
        # append to the list
        # tasks.append(task)
        # update the listbox
        # update_listbox()
    else:
        lbl_display["text"] = "please enter a task"
    txt_input.delete(0, END)

def display_tasks():
    conn = sqlite3.connect("listboxapp.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM listbox")
    records = c.fetchall()
    # print(records)
    if len(records) != 0:
        tasks.clear()
        for record in records:
            task = record[0] + " " + "oid=" + str(record[1])
            tasks.append(task)
        update_listbox()
        tasks.clear()
        lbl_display["text"] = ""
        conn.commit()
        conn.close()
    else:
        lbl_display["text"] = "listbox is empty"

def del_all():
    conn = sqlite3.connect("listboxapp.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM listbox")
    records = c.fetchall()
    # print(records)

    if len(records) == 0:
        tmsg.showinfo("Info", "The List is Empty")
    else:
        confirmed = tmsg.askyesno("please confirm", "do you really want to delete all?")
        if confirmed == True:
            c.execute("DELETE from listbox")
            tasks.clear()
            clear_listbox()
            conn.commit()
            conn.close()


def del_one():
    try:
        conn = sqlite3.connect("listboxapp.db")
        c = conn.cursor()
        c.execute("SELECT *, oid FROM listbox")
        records = c.fetchall()
        # print(records)

        if len(records) == 0:
            # update the display label
            lbl_display["text"] = "list is empty"
        else:
            # get the text of currently selected item
            task = lb_tasks.get(ANCHOR)     # OR task = lb_tasks.get("active")
            # print(type(task))
            # print(task)
            c.execute("DELETE from listbox WHERE oid= " + task[-1])
            c.execute("SELECT *, oid FROM listbox")
            records = c.fetchall()
            tasks.clear()
            for record in records:
                task = record[0] + " " + "oid=" + str(record[1])
                tasks.append(task)
            update_listbox()
            tasks.clear()
            conn.commit()
            conn.close()
    except:
        pass


def sort_asc():
    if len(tasks) == 0:
        # update the display label
        lbl_display["text"] = "list is empty"
    # sort the list
    tasks.sort()
    # update the listbox
    update_listbox()

def sort_desc():
    if len(tasks) == 0:
        # update the display label
        lbl_display["text"] = "list is empty"
    # here we first sort the list ascending then reverse the list
    # sort the list
    tasks.sort()
    # reverse the tasks list
    tasks.reverse()
    # update the listbox
    update_listbox()

def choose_random():
    # choose a random task
    conn = sqlite3.connect("listboxapp.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM listbox")
    records = c.fetchall()
    # print(records)

    if len(records) == 0:
        # update the display label
        lbl_display["text"] = "listbox is empty"
    else:
        for record in records:
            task = record[0]
            tasks.append(task)

        task = str(random.choice(tasks))
        # print(type(task))
        # print(task)
        lbl_display["text"] = task


def show_number_of_tasks():
    conn = sqlite3.connect("listboxapp.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM listbox")
    records = c.fetchall()
    # get the number of tasks
    number_of_tasks = len(records)
    # create and format the message
    msg = "number of tasks: %s" %number_of_tasks
    # display the message
    lbl_display["text"] = msg
    conn.commit()
    conn.close()

# reminder functions
def notif(title, message, e1, e2):
    notification.notify(
        title=title,
        message=message,
        app_icon="ai1.ico",
        timeout=6
    )
    e1.delete(0, END)
    e2.delete(0, END)

def reminderWindow():
    def temp():
         threading.Thread(target=notif(e1.get(), e2.get(), e1, e2))


    top = Tk()
    top.geometry("300x180")
    title_var = StringVar()
    text_var = StringVar()
    l1 = Label(top, text="Reminder Title")
    l2 = Label(top, text="Reminder text")
    l1.grid(row=0, column=0, padx=2)
    l2.grid(row=1, column=0, padx=2)
    e1 = Entry(top, textvariable=title_var)
    e2 = Entry(top, textvariable=text_var)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    b1 = Button(top, text="Set", width=10, command=temp)
    b1.grid(row=2, column=0, padx=2)
    top.mainloop()

def set_reminder():
    def grab_date():
        l1.config(text="reminder is set for " + cal.get_date() + " at " + datetime.datetime.now().strftime("%H:%M:%S"))

    rem = Tk()
    rem.geometry("540x380")

    cal = Calendar(rem, selectmode="day", year=2020, month=5, day=22)
    cal.pack(pady=20, fill=BOTH, expand=True)
    b1 = Button(rem, text="set", command=grab_date)
    b1.pack(pady=20, side=BOTTOM, anchor="sw")
    l1 = Label(rem, text="")
    l1.pack(pady=20)

    rem.mainloop()



if __name__ == '__main__':
    # Basic tkinter setup
    root = Tk()
    root.title("Untitled - NOTE-iT")
    root.wm_iconbitmap("ai1.ico")
    root.geometry("580x644")

    # tool bar
    f1 = Frame(root)
    f1.pack(side=TOP, fill=X)
    # adding text to speech and vice-versa buttons to tool bar
    photo_1 = PhotoImage(file="photo1.png")
    p1 = photo_1.subsample(10, 10)
    photo_2 = PhotoImage(file="photo2.png")
    p2 = photo_2.subsample(10, 10)
    photo_3 = PhotoImage(file="photo3.png")
    p3 = photo_3.subsample(41, 41)
    b1 = Button(f1, image=p1, compound=CENTER, width=1, command=callstt)
    # b1.bind('<ButtonPress-1>', callstart)
    # b1.bind('<ButtonRelease-1>', callstop)
    b2 = Button(f1, image=p2, compound=CENTER, width=1, command=startRead)
    # b3 = Button(f1, image=p3, compound=CENTER, width=1, command=reminderWindow)
    b1.pack(side=LEFT, anchor="e")
    b2.pack(side=LEFT, anchor="e")
    # b3.pack(side=LEFT, anchor="e")

    # frame for listbox
    f2 = Frame(root, borderwidth=6, relief=SUNKEN)
    f2.pack(side=LEFT, fill=Y)

    lbl_title = Label(f2, text=" To Do List ")
    lbl_title.pack()

    lbl_display = Label(f2, text="")
    lbl_display.pack()

    txt_input = Entry(f2, width=20)
    txt_input.pack()

    btn_add_task = Button(f2, text="Add Task", width=20, command=add_task)
    btn_add_task.pack()
    btn_del_all = Button(f2, text="delete all", width=20, command=del_all)
    btn_del_all.pack()
    btn_del_one = Button(f2, text="delete one", width=20, command=del_one)
    btn_del_one.pack()
    btn_display_tasks = Button(f2, text="display tasks", width=20, command=display_tasks)
    btn_display_tasks.pack()
    # btn_sort_asc = Button(f2, text="sort asc", width=20, command=sort_asc)
    # btn_sort_asc.pack()
    # btn_sort_desc = Button(f2, text="sort desc", width=20, command=sort_desc)
    # btn_sort_desc.pack()
    btn_choose_random = Button(f2, text="choose random", width=20, command=choose_random)
    btn_choose_random.pack()
    btn_number_of_tasks = Button(f2, text="number of tasks", width=20, command=show_number_of_tasks)
    btn_number_of_tasks.pack()
    # btn_exit = Button(f2, text="Exit", width=20, command=exit)
    # btn_exit.pack()

    lb_tasks = Listbox(f2, height=20)
    lb_tasks.pack()


    # Add TextArea
    TextArea = Text(root, font="comicscanms 13", undo=True)
    file = None
    TextArea.pack(expand=True, fill=BOTH)


    # Lets create a menubar
    MenuBar = Menu(root)

    # File Menu Starts
    FileMenu = Menu(MenuBar, tearoff=0)
    # To open new file
    FileMenu.add_command(label="New", command=newFile)
    # FileMenu.add_command(label="New Window", command=newWindow)
    # To Open already existing file
    FileMenu.add_command(label="Open", command=openFile)

    # To save the current file

    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)
    # File Menu ends

    # Edit Menu Starts
    EditMenu = Menu(MenuBar, tearoff=0)
    # To give a feature of cut, copy and paste
    EditMenu.add_command(label="undo", command=TextArea.edit_undo)
    # EditMenu.add_command(label="redo", command=TextArea.edit_redo)
    EditMenu.add_separator()
    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copyy)
    EditMenu.add_command(label="Paste", command=paste)
    EditMenu.add_command(label="delete", command=delete)
    EditMenu.add_separator()
    EditMenu.add_command(label="Search with Bing", command=searchBing)
    EditMenu.add_separator()
    EditMenu.add_command(label="Select All", command=selectAll)
    EditMenu.add_command(label="Date/Time", command=currentDate)

    MenuBar.add_cascade(label="Edit", menu=EditMenu)

    # Edit Menu Ends

    # Format menu starts
    FormatMenu = Menu(MenuBar, tearoff=0)
    # FormatMenu.add_command(label="Font")
    FormatMenu.add_command(label="Text Color", command=chooseColor_fg)
    FormatMenu.add_command(label="Background Color", command=chooseColor_bg)
    MenuBar.add_cascade(label="Format", menu=FormatMenu)
    # Format menu ends

    # Help Menu Starts
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="View Help", command=viewHelp)
    HelpMenu.add_separator()
    HelpMenu.add_command(label="About NOTE-iT", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # Help Menu Ends

    # options menu starts
    OptionMenu = Menu(MenuBar, tearoff=0)
    ModeMenu = Menu(OptionMenu, tearoff=0)
    ModeMenu.add_command(label="dark", command=setDark)
    ModeMenu.add_command(label="light", command=setLight)
    OptionMenu.add_cascade(label="Mode", menu=ModeMenu)
    OptionMenu.add_command(label="set reminder", command=set_reminder)
    MenuBar.add_cascade(label="Option", menu=OptionMenu)
    # option menu ends

    root.config(menu=MenuBar)

    # Adding Scrollbar using rules from Tkinter lecture no 22
    ScrollV = Scrollbar(TextArea)
    ScrollV.pack(side=RIGHT, fill=Y)
    ScrollV.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=ScrollV.set)

    conn.commit()
    conn.close()

    root.mainloop()
