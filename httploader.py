import time

__author__ = 'mathieubolla'

class Task():
    time = None
    where = None

    def __init__(self, time, where):
        self.time = time
        self.where = where

    def schedule(self):
        return self.time

    def where_is(self):
        return self.where

    def process(self, tasks, strand):
        print 'Reading colors from ', self.where_is()
        from_app = read_from_app(self)

        for line in from_app['data']:
            strand.print_color(line['line'], line['led'], line['color1'], line['color2'])

class Planning():
    where = None
    time = None

    def __init__(self, where, delta = 0):
        self.time = time.time() + delta
        self.where = where

    def schedule(self):
        return self.time

    def where_is(self):
        return self.where

    def process(self, tasks, strand):
        print 'Reading planing from ', self.where_is()
        from_url = read_from_url(self.where_is())
        from_url_tasks_ = from_url['tasks']
        planning = Planning(self.where_is(), 30)

        tasks.put((planning.schedule(), planning))

        for from_url_task_ in from_url_tasks_:
            print 'Pushing a task on queue'
            tasks.put((from_url_task_[0], Task(from_url_task_[0], from_url_task_[1])))

def read_from_url(url):
    import urllib2

    value = None

    while value == None:
        try:
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            value = resp.read()
        except urllib2.URLError:
            pass

    import json
    from StringIO import StringIO

    return json.load(StringIO(value))

def read_from_app(task):
    return read_from_url(task.where_is())

def main(args):
    import strand
    import serial
    import Queue

    strand = strand.Strand(serial.Serial('/dev/tty.usbserial-A601EQIH', 57600, timeout=1))
    tasks = Queue.PriorityQueue()
    planning = Planning('http://localhost:8080/')
    tasks.put((planning.schedule(), planning))

    while True:
        scheduled, task = tasks.get()
        wait_time_ = task.schedule() - time.time()
        time.sleep(wait_time_ if wait_time_ > 0 else 0)
        task.process(tasks, strand)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])