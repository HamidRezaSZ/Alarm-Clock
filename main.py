import datetime
import re
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from playsound import playsound

alarms = {}
values = 1


def alarmSound():
    while True:
        for alarm in alarms.keys():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            time = re.search("([\d]+):([\d]+) ([A-Z]+)", alarm.cget("text"))
            hour = int(time.group(1))
            minute = time.group(2)
            if len(time.group(2)) == 1:
                minute = "0"+time.group(2)
            if time.group(3) == "PM":
                hour += 12
            set_alarm = f"{hour}:{minute}:00"
            if current_time == set_alarm:
                playsound('sounds/mixkit-alarm-tone-996.wav')
                messagebox.showwarning("Alarm", 'Time to Wake up')
                break


def editTimer():
    if selected.get() in alarms.values():
        editWindow = Tk()
        editWindow.title("Edit Alarm")
        hourLabel = Label(editWindow, text="Hour:")
        hourSpin = Spinbox(editWindow, from_=1, to=12, width=4)
        minuteLabel = Label(editWindow, text="Minute:")
        minuteSpin = Spinbox(editWindow, from_=0, to=59, width=4)
        for alarm, value in alarms.items():
            if value == int(selected.get()):
                time = re.search("([\d]+):([\d]+) ([A-Z]+)",
                                 alarm.cget("text"))
                hourSpin.set(int(time.group(1)))
                minuteSpin.set(int(time.group(2)))
                combo = Combobox(editWindow, width=3)
                combo['values'] = ("AM", "PM")
                if time.group(3) == "AM":
                    combo.current(0)
                else:
                    combo.current(1)
                combo.grid(column=1, row=2)
        hourLabel.grid(column=0, row=0)
        hourSpin.grid(column=1, row=0)
        minuteLabel.grid(column=0, row=1)
        minuteSpin.grid(column=1, row=1)

        def createTimer():
            global values
            if (int(hourSpin.get()) >= 1 and int(hourSpin.get()) <= 12 and int(minuteSpin.get()) >= 0 and int(minuteSpin.get()) <= 59):
                radioBtn = Radiobutton(window, text=hourSpin.get(
                )+':'+minuteSpin.get()+" "+combo.get(), value=values, variable=selected)
                alarms[radioBtn] = values
                values += 1
                editWindow.destroy()
                deleteAlarm()
                printAlarms()
            else:
                messagebox.showerror(
                    "Error", 'Please enter correct hour and minute')

        def cancelWindow():
            editWindow.destroy()

        cancelBtn = Button(editWindow, text="Cancel", command=cancelWindow)
        editBtn = Button(editWindow, text="Edit",
                         command=createTimer)
        cancelBtn.grid(column=0, row=3)
        editBtn.grid(column=1, row=3)
        editWindow.mainloop()


def printAlarms():
    sortDict()
    counter = 1
    for alarm in alarms.keys():
        alarm.grid(column=1, row=counter)
        counter += 1


def deleteAlarm():
    for alarm, value in alarms.items():
        if value == int(selected.get()):
            alarms.pop(alarm)
            alarm.destroy()
            break
    sortDict()


def sortDict():
    global alarms
    alarms = dict(sorted(alarms.items(), key=lambda t: t[0].cget("text")))


def addTimer():
    addWindow = Tk()
    addWindow.title("Add Alarm")
    hourLabel = Label(addWindow, text="Hour:")
    hourSpin = Spinbox(addWindow, from_=1, to=12, width=4)
    hourSpin.set(6)
    minuteLabel = Label(addWindow, text="Minute:")
    minuteSpin = Spinbox(addWindow, from_=0, to=59, width=4)
    minuteSpin.set(0)
    hourLabel.grid(column=0, row=0)
    hourSpin.grid(column=1, row=0)
    minuteLabel.grid(column=0, row=1)
    minuteSpin.grid(column=1, row=1)
    combo = Combobox(addWindow, width=3)
    combo['values'] = ("AM", "PM")
    combo.current(0)
    combo.grid(column=1, row=2)

    def createTimer():
        global values
        if (int(hourSpin.get()) >= 1 and int(hourSpin.get()) <= 12 and int(minuteSpin.get()) >= 0 and int(minuteSpin.get()) <= 59):
            radioBtn = Radiobutton(window, text=hourSpin.get(
            )+':'+minuteSpin.get()+" "+combo.get(), value=values, variable=selected)
            alarms[radioBtn] = values
            values += 1
            addWindow.destroy()
            printAlarms()
        else:
            messagebox.showerror(
                "Error", 'Please enter correct hour and minute')

    def cancelWindow():
        addWindow.destroy()

    cancelBtn = Button(addWindow, text="Cancel", command=cancelWindow)
    saveBtn = Button(addWindow, text="Add",
                     command=createTimer)
    cancelBtn.grid(column=0, row=3)
    saveBtn.grid(column=1, row=3)
    addWindow.mainloop()


window = Tk()
window.title("Alarm Clock")
addBtn = Button(window, text="Add", command=addTimer)
editBtn = Button(window, text="Edit", command=editTimer)
deleteBtn = Button(window, text="Delete", command=deleteAlarm)
addBtn.grid(column=0, row=0)
editBtn.grid(column=1, row=0)
deleteBtn.grid(column=2, row=0)
selected = IntVar()
p1 = PhotoImage(file='icons/Very-Basic-Alarm-Clock-icon.png')
window.iconphoto(False, p1)
t = Thread(name='daemon', target=alarmSound)
t.setDaemon(True)
t.start()
window.mainloop()
