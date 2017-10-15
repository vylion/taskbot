from task import *

class Chat(object):
    def __init__(self, ident, name):
        self.id = ident
        self.tasks = {}
        self.name = name

    def addTask(self, name, repeat=0, hour=0, day=0, month=0, year=0):
        t = Task(name, repeat, hour, day, month, year)
        if name in self.tasks:
            raise ValueError('duplicate key "' + name + '" found')
        self.tasks[name] = t
        print('new task ' + t.name + ' added:')
        print(str(t) + '\n')
        return t

    def getTasksRange(self, d=0, m=0, y=0, d2=0, m2=0, y2=0):
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
        dateEnd = datetime(y2, m2, d2, 23)
        resultTasks = []
        for t in self.tasks:
            task = self.tasks[t]
            print(task)
            if task.getDate() >= dateIni and task.getDate() <= dateEnd:
                resultTasks.append(task)
        return resultTasks

    def getTasks(self):
        resultTasks = []
        for _, v in self.tasks.items():
            resultTasks.append(v)
        return resultTasks

    def deleteTask(self, name):
        if name in self.tasks:
            del self.tasks[name]
            return True
        return False

    def markDone(self, name):
        if name in self.tasks:
            t = self.tasks[name]
            if t.repeat > 0:
                t.date += timedelta(t.repeat)
            else:
                del self.tasks[name]
            return True
        return False
