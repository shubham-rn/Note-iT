from tkinter import *
import sqlite3

root = Tk()

tasks = []

conn = sqlite3.connect("list_book.db")
c = conn.cursor()

# created database for list book

# conn = sqlite3.connect("list_book.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE listbook(
#     task text,
#     priority integer)""")
# conn.commit()
# conn.close()

# adding functions to list book database

# listbox functions
def update_listbox():
    # clear the current list
    clear_listbox()
    # populate the listbox
    for task in tasks:
        lb_tasks.insert(END, task)

def clear_listbox():
    lb_tasks.delete(0, END)


def submit():
    conn = sqlite3.connect("list_book.db")
    c = conn.cursor()

    task = e1.get() + " " + str(e2.get())

    if task != " ":
        c.execute("INSERT INTO listbook VALUES(:task, :priority)",
                  {
                      'task': e1.get(),
                      'priority': e2.get()

                  })
        conn.commit()
        conn.close()
        # append to the list
        # tasks.append(task)
        # update the listbox
        # update_listbox()
    else:
        print("enter a task")   # update label here

    e1.delete(0, END)
    e2.delete(0, END)

def displaytasks():
    conn = sqlite3.connect("list_book.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM listbook")
    records = c.fetchall()
    # print(records)
    tasks.clear()
    for record in records:
        task = record[0] + " " + str(record[1]) + " " + "oid=" + str(record[2])
        tasks.append(task)
    update_listbox()
    tasks.clear()

    conn.commit()
    conn.close()


def del_one():
    try:
        conn = sqlite3.connect("list_book.db")
        c = conn.cursor()

        c.execute("DELETE from listbook WHERE oid= " + e3.get())
        c.execute("SELECT *, oid FROM listbook")
        records = c.fetchall()
        print(records)

        tasks.clear()
        for record in records:
            task = record[0] + " " + str(record[1]) + " " + "oid=" + str(record[2])
            tasks.append(task)
        update_listbox()
        tasks.clear()

        e3.delete(0, END)
        conn.commit()
        conn.close()
    except Exception:
        pass

def del_all():
    conn = sqlite3.connect("list_book.db")
    c = conn.cursor()

    c.execute("DELETE from listbook")
    tasks.clear()
    clear_listbox()

    conn.commit()
    conn.close()

root.geometry("400x240")
e1 = Entry(root)
e1.grid(row=0, column=0)
e2 = Entry(root)
e2.grid(row=1, column=0)
b1 = Button(root, text="submit", command=submit)
b1.grid(row=2, column=0)
b2 = Button(root, text="show tasks", command=displaytasks)
b2.grid(row=3, column=0)
e3 = Entry(root)
e3.grid(row=4, column=0)
b3 = Button(root, text="delete one", command=del_one)
b3.grid(row=5, column=0)
b4 = Button(root, text="delete all", command=del_all)
b4.grid(row=6, column=0)

lb_tasks = Listbox(root)
lb_tasks.grid()



root.mainloop()