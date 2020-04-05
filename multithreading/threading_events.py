
"""
Threading events are a very simple concept; one thread emits an event while other threads are waiting to see such event
In a nutshell, Events are used for inter-thread communication.

Thread A signals an 'event' and Thread B waits for it.  Core functionality of a Threading.Event is built into the set() and clear() methods
which both respectively set and clear a flag to True/False.  The method wait() is blocking until set() has set the flag to True
"""

from threading import Thread
from threading import Event


class CustomEvent(Event):
  pass

event = CustomEvent()
event.is_set() # False
event.set() # set the self._flag (private!) to True
event.wait() # This will return immediately
event.clear()
event.wait(timeout=10) # This will timeout after 10 seconds!
event.wait() # uh oh! this will wait indefinitely.. the flag is never set! 



"""
Lets have a look at a more multi threaded concrete example
"""

class CustomThread(Thread):
    def __init__(self):
        super().__init__(name='Custom')
        self.event = CustomEvent()

    def run(self):
        while not self.event.is_set():
            print('Waiting for the event')
            self.event.wait()


class OtherThread(Thread):
    def __init__(self, custom):
        super().__init__(name='Other')
        self.custom_thread = custom

    def run(self):
        time.sleep(30)
        print('triggering the event flag from thread two')
        self.custom_thread.event.set()


thread_one = CustomThread()
thread_two = OtherThread(thread_one)
thread_one.start()
thread_two.start()
# What should we expect? after the 30 seconds, thread_two will terminate thread 1 by triggering its self.event flag to True
# forcing its run method to terminate the thread

"""
Waiting for the event
Waiting for the event
Waiting for the event
Waiting for the event
Waiting for the event
Waiting for the event
triggering the event from thread two

Process finished with exit code 0
"""

"""
A closer look at the interface of threading.Event
"""

def is_set()
def isSet() 
# java style getters(these are pretty common throughout the python3 threading api, prefer is_set())
# isSet() is just a reference to is_set() handled via => isSet = is_set
# Returns true only if the internal (self._flag) is True

def set()
# Awakens all threads that are waiting for it to be True
# sets self._flag = True and calls notify_all() on the condition (self._cond)
# Uses Condition(RLock()) .notify_all()

def clear()
# sets self._flag = False
# Subsequently all threads calling wait() will block until set() has been called

def wait(timeout: float = None) -> bool
# waits for the self._flag to be True
# if the self._flag is already True on initial check; return (True) immediately
# By default will wait indefinitely, tho overridable timeout arg can be specified
# Timeout should be a floating point number, specifies a timeout in seconds (or fractions thereof)
# Returns True unless the timeout is provided and expires; then returning False

# A bigger scale example, here we will have 10 threads waiting for the lock of another, to see how notify_all() will function.

class Overlord(Thread):
    def __init__(self):
        super().__init__(name='overlord')
        self.event = CustomEvent()

    def run(self):
        time.sleep(60)
        print('insert overlord jargon speech here')
        self.event.set()


class Minion(Thread):
    def __init__(self, overlord: Overlord):
        super().__init__(name='Minion')
        self.overlord = overlord

    def run(self):
        print('minion will begin waiting for the overlords commands!')
        self.overlord.event.wait()
        print('/n', 'overlord has spoken! terminating')


overlord_thread = Overlord()
waiting_threads = [Minion(overlord_thread) for _ in range(10)]
overlord_thread.start()
for thread in waiting_threads:
    thread.start()
    
"""
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
minion will begin waiting for the overlords commands!
insert overlord jargon speech here
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
overlord has spoken! terminating
"""

