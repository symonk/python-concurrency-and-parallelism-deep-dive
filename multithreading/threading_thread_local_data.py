"""
threading.local is a simple dictionary namespace that permits storing thread specific data.  This is a very
simple concept and is outlined nicely below
"""

import threading
import time


# Lets create our own local subclass!
class CustomThreadOnlyData(threading.local):
    def __init__(self):
        self.x = 2

    def __repr__(self):
        return str(self.x)


DATA = CustomThreadOnlyData()


# 10 threads all accessing the data and printing the default value.
def read_it():
    DATA.x *= threading.get_ident()
    print(f"{threading.get_ident()}: is reading the DATA: {DATA}")


threads = [threading.Thread(target=read_it) for _ in range(20)]
for thread in threads:
    time.sleep(0.2)
    thread.start()

"""
Produces the output of:
15344: is reading the DATA: 30688
8732: is reading the DATA: 17464
11296: is reading the DATA: 22592
2448: is reading the DATA: 4896
6312: is reading the DATA: 12624
7080: is reading the DATA: 14160
15044: is reading the DATA: 30088
3608: is reading the DATA: 7216
11840: is reading the DATA: 23680
6564: is reading the DATA: 13128
1352: is reading the DATA: 2704
1796: is reading the DATA: 3592
13480: is reading the DATA: 26960
11288: is reading the DATA: 22576
7740: is reading the DATA: 15480
568: is reading the DATA: 1136
15132: is reading the DATA: 30264
10304: is reading the DATA: 20608
4984: is reading the DATA: 9968
1684: is reading the DATA: 3368

as we can see, each thread multiplies its own copy of `x` by its thread identifer.  Each thread here
is freely able to access and modify the values in its own local thread safe namespace.
"""