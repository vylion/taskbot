
from datetime import datetime, timedelta
from calendar import monthrange

class Task(object):
    def __init__(self, name, repeat=0, hour=0, day=0, month=0, year=0):
        self.name = name
        self.repeat = repeat
        self.setDate(hour, day, month, year)

    def setDate(self, h, d, m, y):
        date = datetime.now()
        date.replace(year=max(date.year, y))

        if m > 0 and datetime.now() > datetime(date.year, m, date.day):
            date.replace(year=(date.year+1))
        date.replace(month=max(date.month, m))

        if d > 0 and datetime.now() > datetime(date.year, date.month, d):
            _, delta = monthrange(date.year, date.month)
            date += timedelta(delta) # Days of date.month
        date.replace(day=max(date.day, d))

        if h > 0 and datetime.now() > datetime(date.year, date.month, date.day, h):
            date += timedelta(1)
        self.date = datetime(date.year, date.month, date.day, max(date.hour, h))

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def __str__(self):
        s = "Task " self.name + ":\n"
        s += "Date: " + " " + str(self.date.day) + "/" + str(self.date.year) + "/" + str(self.date.month) + "\n"
        if self.repeat > 0:
            s += "Repeats every " + self.repeat + " days."
