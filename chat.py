from task import *
class Chat(object):
    def __init__(self, ident, name):
        self.id = ident
        self.tasks = []
        self.name = name

    def addTask(self, name, repeat=0, hour=0, day=0, month=0, year=0):
        t = Task(name, repeat, hour, day, month, year)
        self.tasks.append(t)
        print('task ' + self.tasks[-1].name + ' added')
        return t

    def getTasks(self, y=0, d=0, m=0, y2=0, d2=0, m2=0):
        dateNow = datetime.now()
        if y == 0:
            y = dateNow.year
        if m == 0:
            m = dateNow.month
        if d == 0:
            d = dateNow.day
        if y2 == 0:
            y2 = dateNow.year
        if m2 == 0:
            m2 = dateNow.month
        if d2 == 0:
            d2 = dateNow.day
        dateIni = datetime(y, m, d)
        dateEnd = datetime(y2, m2, d2)
        resultTasks = []
        for t in self.tasks:
            print(t)
            if t.getDate() >= dateIni and t.getDate() <= dateEnd:
                resultTasks.append(t)
        return resultTasks

    def getChatName(self):
        return self.name
