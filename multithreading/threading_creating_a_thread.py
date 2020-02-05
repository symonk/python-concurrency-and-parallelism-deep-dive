from threading import Thread

"""
Creating a python thread can be done through two simple methods
 - Subclassing the Thread class and overriding the run() method
 - Passing a callable to target= when instantiating a new instance of Thread
"""


class CustomThread(Thread):
    def __init__(self):
        """
        Important: No other methods apart from init or run should be overridden in a subclass!
        """
        super().__init__()

    def run(self):
        print('running')


thread_subclass = CustomThread()
thread_subclass.start()

thread_target = Thread(target=lambda: print('running'))
thread_target.start()

"""
Notice how we invoke .start() here and not .run() itself.  This is because calling start() in itself invokes .run()
in a seperate thread of control
"""

