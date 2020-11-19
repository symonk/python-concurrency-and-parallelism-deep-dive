import time
from threading import Timer

"""
threading.Timer is a subclass of Thread itself.  In simple terms it permits delaying the thread execution by
a number of seconds prior to executing the Threads target.

args:
    interval (float)
    function (callable function to be executed as part of the timers run() invocation)
    args (Optional iterable[Any] or empty list if not provided)
    kwargs (Optional Mapping[str, Any] or empty dictionary if not provided)
    
Timers use a threading.Event under the hood to control the finished waiting state.  When instantiated each
Timer instances creates an Event instance which it tracks internally through the self.finished instance attr.

"""


def the_callable(*args, **kwargs):
    print(args)
    print('----')
    print(kwargs)


five_second_delay_timer = Timer(interval=5.00, function=the_callable, args=(10, 20, 30), kwargs={'foo': 'bar'})
five_second_delay_timer.start()

"""
Pseudo Output:
[timer thread started...].
[timer thread delays the interval of 5seconds].
[args are printed (10, 20, 30)].
[---- printed].
[{'foo': 'bar'} printed].
"""

# Cancelling a timer before the event has finished the interval during run.
t = Timer(60, the_callable)
t.start()
time.sleep(5)
t.cancel()

# The run method & the Event delay
# When a timers run() method is called, initially the self.finished (`Event` instance is asked to. wait(interval).
# Note: see threading_event.py for more information on events.
"""
    def run(self):
        # Wait until an event is_set() == True, otherwise time out after the floating point interval.
        self.finished.wait(self.interval)
        # if the event has not been set(), invoke the function with the args & kwargs
        if not self.finished.is_set(): 
            self.function(*self.args, **self.kwargs)
        # mark the event as set() True
        self.finished.set()"""
