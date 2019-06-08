import threading
import random
import time


class Producer(threading.Thread):

  def __init__(self, integers, condition):
    super(Producer,self).__init__()
    self.integers = integers
    self.condition = condition

  def run(self):
    while True:
      integer = random.randint(0, 1000)
      self.condition.acquire()  #获取条件锁
      print('condition acquired by %s' % threading.current_thread().name)
      self.integers.append(integer)
      print('%d appended to list by %s' % (integer, threading.current_thread().name))
      print('condition notified by %s' % threading.current_thread().name)
      self.condition.notify()   #唤醒消费者线程
      print('condition released by %s' % self.name)
      self.condition.release()  #释放条件锁
      time.sleep(1)


class Consumer(threading.Thread):

  def __init__(self, integers, condition):
    super(Consumer,self).__init__()
    self.integers = integers
    self.condition = condition

  def run(self):
    while True:
      self.condition.acquire()  #获取条件锁
      print('condition acquired by %s' % self.name)
      while True:
        if self.integers:
          integer = self.integers.pop()
          print('%d popped from list by %s' % (integer, self.name))
          break
        print('condition wait by %s' % self.name)
        self.condition.wait()   #等待状态，等待被唤醒，才会继续执行

      print('condition released by %s' % self.name)
      self.condition.release()  #最后释放条件锁



if __name__ == '__main__':

  integers = []
  condition = threading.Condition()
  t1 = Producer(integers, condition)
  t2 = Consumer(integers, condition)
  t1.start()
  t2.start()
  t1.join()
  t2.join()