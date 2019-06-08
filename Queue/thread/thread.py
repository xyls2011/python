import threading
import time

def run(sec):
    print('%s线程开始： ' %threading.current_thread().name)
    time.sleep(sec)
    print('%s线程结束： ' %threading.current_thread().name)

if __name__ == '__main__':

    start_time = time.time()

    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run, args=(i,))
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('主线程结束！' , threading.current_thread().name)
    print('一共用时：', time.time()-start_time)