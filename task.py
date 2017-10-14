
from datetime import datetime, timedelta
from calendar import monthrange

class Task(object):
    def __init__(self, name, repeat=0, hour=0, day=0, month=0, year=0):
        self.name = name
        self.repeat = repeat
        self.setDate(hour, day, month, year)

    def setDate(self, h, d, m, y):
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour)
        date = datetime(now.year, now.month, now.day, now.hour)
        fixed = (y > 0 and m > 0 and d > 0)
        if y > 0:
            date = date.replace(year=y)

        if m > 0:
            while now >= datetime(date.year, m, date.day, date.hour) and not fixed:
                date = date.replace(year=(date.year+1))
            date = date.replace(month=m)

        if d > 0:
            if now >= datetime(date.year, date.month, d, date.hour) and not fixed:
                _, delta = monthrange(date.year, date.month)
                date += timedelta(delta) # Days of date.month
            date = date.replace(day=d)

        if h > 0:
            if now >= datetime(date.year, date.month, date.day, h) and not fixed:
                date += timedelta(1)
            date = datetime(date.year, date.month, date.day, h)

        while now >= date and self.repeat > 0:
            date += timedelta(self.repeat)
        self.date = date

    def getDate(self):
        return self.date

    def getName(self):
        return self.name

    def __str__(self):
        s = "Task " + self.name + ":\n"
        s += "Date: " + " " + str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year)
        s += " at " + str(self.date.hour) + ":00\n"
        if self.repeat > 0:
            s += "Repeats every " + str(self.repeat) + " days."
        return s
