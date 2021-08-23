# ----------------------------------- IMPORTS -------------------------------------- #
from tkinter.ttk import *
from win10toast import ToastNotifier
from tkinter import *
import math

# ---------------------------- CONSTANTS AND VARIABLES ------------------------------- #

COUNTER_VELOCITY = 1000
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#FFF7AE"
PURPLE = "#1A2849"
PURPLE_2 = "#11052C"
WORK_BG_C = "#170A19"
BREAK_BG_C = "#0F3057"
L_BREAK_BG_C = YELLOW
L_BREAK_FONT_C = GREEN
BREAK_FONT_C = "white"
BUTTON_C = RED
FONT_NAME = "Lato"
TIMER_FONT = YELLOW
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
reps = 0
long = False
notify = True
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    """Reset the timer and the design to the original one"""

    global reps
    button_reset.grid_forget()
    button_play.grid(column=1, row=3)
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00", fill="white")
    title_label.config(text="Timer", bg=WORK_BG_C, fg=RED)
    label_check.config(text="", bg=WORK_BG_C)
    window.config(bg=WORK_BG_C)
    canvas.config(bg=WORK_BG_C)
    button_reset.config(bg=RED, fg=YELLOW)
    button_not.config(bg=canvas["background"],
                      fg=button_reset["background"],
                      activebackground=canvas["background"])

    reps = 0


# ---------------------------- NOTIFICATION METHODS ------------------------------- #

#SHOW THE NOTIFICATION WHEN CALLED AND PUT THE WINDOW ON TOP OF OTHERS
my_notification = ToastNotifier()


def note_mute():
    global notify
    if notify == False:
        notify = True
        button_not.config(text="Disable Notifications")
    else:
        notify = False
        button_not.config(text="Enable Notifications")


def focus_window():
    window.deiconify()
    window.focus_force()
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)


def notification_work():
    my_notification.show_toast(
        "Pymodoro",
        "Your break time is over, it's time to work!",
        icon_path=".\\tomato_icon.ico",
        threaded=True,
        duration=8)
    focus_window()


def notification_sbreak():
    my_notification.show_toast(
        "Pymodoro",
        "Your working time is over, take a break now.",
        icon_path=".\\tomato_icon.ico",
        threaded=True,
        duration=8)
    focus_window()


def notification_lbreak():
    my_notification.show_toast(
        "Pymodoro",
        "You've worked for a long time, now it's time to rest.",
        icon_path=".\\tomato_icon.ico",
        threaded=True,
        duration=8)
    focus_window()


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    """Start the timer, change the design and the time mode,
                and call the notifications methods."""
    global reps
    global long
    global timer
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    long = False
    long2 = False

    if reps % 2 != 0:
        countdown(work_sec)
        if reps != 1 and notify == True and long2 == True:
            notification_work()
            long2 = False
        label_check.config(bg=WORK_BG_C, fg="white")
        title_label.config(text="Work", bg=WORK_BG_C, fg=RED)
        window.config(bg=WORK_BG_C)
        canvas.config(bg=WORK_BG_C)
        button_reset.config(bg=RED, fg=YELLOW)
        canvas.itemconfig(timer_text, fill=YELLOW)

    elif reps % 8 == 0:
        countdown(long_break_sec)
        if notify == True:
            notification_lbreak()
        label_check.config(bg=L_BREAK_BG_C, fg=GREEN)
        title_label.config(fg=L_BREAK_FONT_C, text="Break", bg=L_BREAK_BG_C)
        window.config(bg=L_BREAK_BG_C)
        canvas.config(bg=L_BREAK_BG_C)
        button_reset.config(bg=GREEN, fg=YELLOW)
        canvas.itemconfig(timer_text, fill=YELLOW)
        long = True
        long2 = True
        reps = 0

    elif reps % 2 == 0:
        countdown(short_break_sec)
        if notify == True:
            notification_sbreak()
        label_check.config(bg=BREAK_BG_C, fg="white")
        title_label.config(text="Break", bg=BREAK_BG_C, fg=BREAK_FONT_C)
        window.config(bg=BREAK_BG_C)
        canvas.config(bg=BREAK_BG_C)
        button_reset.config(bg="white", fg=BREAK_BG_C)
        canvas.itemconfig(timer_text, fill="white")
    
    button_not.config(bg=canvas["background"],
    fg=button_reset["background"],
    activebackground=canvas["background"])


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    """Show time in legible format and control another things."""
    global reps
    global long
    global timer
    button_play.grid_forget()
    button_reset.grid(column=1, row=3)
    count_min = count // 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(COUNTER_VELOCITY, countdown, count - 1)
    else:
        start_timer()
        check_count = ""
        for _ in range(math.floor(reps / 2)):
            check_count += "✔"
        label_check.config(text=check_count)
        if long == True:
            label_check.config(text="✔✔✔✔")


# ---------------------------- UI SETUP ------------------------------- #

#ALMOST EVERYTHING ABOUT UI IS HERE
#WINDOW SETUP
window = Tk()
window.title("Pymodoro")
window.config(padx=75, pady=50, bg=WORK_BG_C)
window.minsize(100, 100)
window.resizable(False, False)

#TOMATO AND TIME CANVAS
canvas = Canvas(width=201, height=250, highlightthickness=0, bg=WORK_BG_C)
tomato_img = PhotoImage(file=".\\tomato.png")
window.iconphoto(False, tomato_img)
canvas.create_image(100, 135, image=tomato_img)
timer_text = canvas.create_text(100,
                                150,
                                text="00:00",
                                font=(FONT_NAME, 36, "bold"),
                                fill=TIMER_FONT)

#BUTTONS
button_play = Button(text="Start",
                     padx=36,
                     pady=6,
                     highlightthickness=0,
                     command=start_timer,
                     activebackground=PINK,
                     bg=RED,
                     fg=YELLOW,
                     font=(FONT_NAME, 20, "bold"),
                     relief="flat")

button_reset = Button(text="Reset",
                      padx=36,
                      pady=6,
                      bg=BUTTON_C,
                      fg=YELLOW,
                      highlightthickness=0,
                      command=reset_timer,
                      activebackground=PINK,
                      font=(FONT_NAME, 20, "bold"),
                      relief="flat")

button_not = Button(text="Disable Notifications",
                    bg=canvas["background"],
                    fg=button_reset["background"],
                    highlightthickness=0,
                    command=note_mute,
                    activebackground=canvas["background"],
                    font=(FONT_NAME, 9, "bold"),
                    relief="flat")

#TIMER LABEL
title_label = Label(
    text="Timer",
    font=(FONT_NAME, 48, "bold"),
    fg=RED,
    bg=WORK_BG_C,
)

#CHECK MARK
label_check = Label(text="",
                    bg=WORK_BG_C,
                    fg="white",
                    font=("Arial", 16, ""),
                    pady=20)

#GRID
canvas.grid(column=1, row=1)
button_play.grid(column=1, row=3)
title_label.grid(column=1, row=0)
label_check.grid(column=1, row=2)
button_not.grid(column=1, row=4)

#MAINLOOP
window.mainloop()
