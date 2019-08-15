#!/usr/bin/python
# Application:  Countdown Timer for Raspberry Pi
# Description:  Provides a countdown timer with reset and alternate time buttons.
# Author:       Jack-Daniyel Strong <jack@jdstrong.com>
# Date:         09-Aug-2019
# Version:      0.1
# ==============================================================================

try:
    # for Python 3
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font
except ImportError:
    # for Python 2
    import Tkinter as tk
    import ttk
    import tkFont as font

import time
import datetime
from math import floor

global endTime, warnTime, stopTime 

# Handle someone clicking the X to close the Tkinter window
def quit(*args):
    root.destroy()

# Handle and format the TimeDelta (preferred value in as total seconds)
# From https://stackoverflow.com/questions/13409682/how-can-i-format-timedelta-for-display/13409760#13409760
def format_timedelta(value, time_format="{hours}:{minutes2}:{seconds2}"):

    if hasattr(value, 'seconds'):
        seconds = value.seconds + value.days * 24 * 3600
    else:
        seconds = int(value)
        # Stop the 24 hour countdown and count up instead (Doesn't help past 24 hours)
        if value < 0:
            seconds = 24 * 3600 - seconds

    seconds_total = seconds

    minutes = int(floor(seconds / 60))
    minutes_total = minutes
    seconds -= minutes * 60

    hours = int(floor(minutes / 60))
    hours_total = hours
    minutes -= hours * 60

    days = int(floor(hours / 24))
    days_total = days
    hours -= days * 24

    years = int(floor(days / 365))
    years_total = years
    days -= years * 365

    return time_format.format(**{
        'seconds': seconds,
        'seconds2': str(seconds).zfill(2),
        'minutes': minutes,
        'minutes2': str(minutes).zfill(2),
        'hours': hours,
        'hours2': str(hours).zfill(2),
        'days': days,
        'years': years,
        'seconds_total': seconds_total,
        'minutes_total': minutes_total,
        'hours_total': hours_total,
        'days_total': days_total,
        'years_total': years_total,
    })    

# This is what handles displaying and updating the TimeDelta and Current Time
def show_time():
    # Get Current time
    currentTime = datetime.datetime.now()
    # Get the time remaining until the event
    remainder = endTime - currentTime
    # remove the microseconds part
    remainder = remainder - datetime.timedelta(microseconds=remainder.microseconds)
    # Show the time left
    txt.set(format_timedelta(remainder.total_seconds()))
    # Update Current Time Clock
    ctTxt.set(currentTime.strftime('%X'))
    # If in warning timeframe, set background
    if currentTime > warnTime:
        root.configure(background='orange')
        lbl.configure(foreground='white', background='orange')
        ctLbl.configure(foreground='green', background='orange')
        if currentTime > stopTime:
            root.configure(background='red')
            lbl.configure(foreground='black', background='red')
            ctLbl.configure(foreground='white', background='red')
            if currentTime > endTime:
                if (currentTime.second % 2) == 0:
                    root.configure(background='black')
                    lbl.configure(foreground='white', background='black')
                    ctLbl.configure(foreground='purple', background='black')
                else:
                    root.configure(background='purple')
                    lbl.configure(foreground='white', background='purple')
                    ctLbl.configure(foreground='black', background='purple')
    # Trigger the countdown after 1000ms
    root.after(1000, show_time)

# Give us a way to restart the clock
def resetTime(end=40, warn=8, stop=1):
    global endTime, warnTime, stopTime, root, lbl 
    valEnd = int(end)
    valWarn = int(warn)
    valStop = int(stop)

    # Set the end date and time for the countdown
    #endTime = datetime.datetime(2017, 9, 19, 9, 0, 0)
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=valEnd)
    warnTime = endTime - datetime.timedelta(minutes=valWarn)
    stopTime = endTime - datetime.timedelta(minutes=valStop)
    root.configure(background='black')
    lbl.configure(foreground='white', background='black')
    ctLbl.configure(foreground='green', background='black')

    print("End: " + str(endTime) + " - warnTime: "+ str(warnTime))

# Let's assemple some functions to call from the buttons for ease.
# Allow Button to Set Timer to 5 minutes
def setTime5():
    resetTime(5, 2, 1)
# Allow Button to Set Timer to 10 minutes
def setTime10():
    resetTime(10, 3, 1)
# Allow Button to Set Timer to 15 minutes
def setTime15():
    resetTime(15, 3, 1)
# Allow Button to Set Timer to 50 minutes
def setTime50():
    resetTime(50, 10, 1)
# Allow Button to Set Timer to 15 minutes
def setTime3():
    resetTime(3, 2, 1)

# Use tkinter lib for showing the clock
root = tk.Tk()
# Make the window fill the screen
root.attributes("-fullscreen", True)
# Set background to black
root.configure(background='black')
# enable closing the window to call the quit() function
root.bind("x", quit)
# wait a minute and then call show_time to get things rolling
root.after(1000, show_time)

# Get Screen Width to dynamically determine font size
screenWidth = root.winfo_screenwidth()

# Force Classic tKinter style for proper formatting
style = ttk.Style()
style.theme_use('classic') # Any style other than aqua.

# Let's make a label for the countdown
fnt = font.Font(family='Helvetica', size=int(screenWidth/6), weight='bold')
txt = tk.StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="white", background="black")
lbl.place(relx=0.5, rely=0.5, anchor="center")

# Configure Current Time Label
fnt = font.Font(family='Helvetica', size=int(screenWidth/12), weight='normal')
ctTxt = tk.StringVar()
ctLbl = ttk.Label(root, textvariable=ctTxt, font=fnt, foreground="green", background="black")
ctLbl.place(relx=0.5, rely=0.1, anchor="center")

# Let's place the buttons using relative placement (may overlap on smaller screens)
# Reset Button
b = ttk.Button(root, text="Reset", command=resetTime)
b.place(relx=0.95,rely=0.95, anchor='center')
# 5 min Button
b5 = ttk.Button(root, text="5 Mins", command=setTime5)
b5.place(relx=0.85,rely=0.95, anchor='center')
# 10 min Button
b10 = ttk.Button(root, text="10 Mins", command=setTime10)
b10.place(relx=0.8,rely=0.95, anchor='center')
# 15 min Button
b15 = ttk.Button(root, text="15 Mins", command=setTime15)
b15.place(relx=0.75,rely=0.95, anchor='center')
# 50 min Button
b50 = ttk.Button(root, text="50 Mins", command=setTime15)
b50.place(relx=0.7,rely=0.95, anchor='center')
# 3 min Button
# b3 = ttk.Button(root, text="3 Mins", command=setTime3)
# b3.place(relx=0.75,rely=0.9, anchor='center')
# Exit/Quit Button
bq = ttk.Button(root, text="Exit", command=quit)
bq.place(relx=0.05,rely=0.95, anchor='center')

# Call resetTime to kick things off.
resetTime()

# Loop until we quit.
root.mainloop()
