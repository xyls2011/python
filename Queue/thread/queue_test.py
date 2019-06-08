import threading
import queue
import random
import time

class Producer(threading.Thread):

    def __init__(self, queue):
        super(Producer,self).__init__()
        self.queue = queue

    def run(self):
        while True:
            integer = random.randint(0, 1000)
            self.queue.put(integer)
            print('%d put to queue by %s' % (integer, self.name))
            time.sleep(1)


class Consumer(threading.Thread):

    def __init__(self, queue):
        super(Consumer, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            integer = self.queue.get()
            print('%d popped from list by %s' % (integer, self.name))
            self.queue.task_done()


if __name__ == '__main__':

    queue = queue.Queue()
    t1 = Producer(queue)
    t2 = Consumer(queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()