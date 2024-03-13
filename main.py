# main.py
import tkinter as tk
import calendar
from frontend import LoginScreen
import tkinter as tk
from tkinter import messagebox, ttk
from my_calendar import PersonalizedCalendar
import backend as be
import sqlite3
import tkinter.messagebox as messagebox
from datetime import datetime

def main():
    login_screen = LoginScreen()
    login_screen.mainloop()

if __name__ == '__main__':
    main()
