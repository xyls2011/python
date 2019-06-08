import threading

num = 0
lock = threading.Lock()
def run(n):
    global num
    for i in range(1000000):
        lock.acquire()
        num = num + n
        num = num - n
        lock.release()


if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=(50,))
    t2 = threading.Thread(target=run,args=(16,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(num)