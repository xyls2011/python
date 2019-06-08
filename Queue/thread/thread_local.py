import threading


local_var = threading.local()

def get_name():
    name = local_var.name
    print('Hello, %s (in %s)' % (name, threading.current_thread().name))

def def_name(name):
    local_var.name = name
    get_name()

if __name__ == '__main__':
    t1 = threading.Thread(target= def_name, args=('zhangsan',))
    t2 = threading.Thread(target= def_name, args=('lisi',))

    t1.start()
    t2.start()
    t1.join()
    t2.join()