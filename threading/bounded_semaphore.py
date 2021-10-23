"""
In simple terms, a semaphore manages an internal counter which is decremented for each acquire() call it receives.
Incrementing the counter for every release() call it receives.  Worth noting the internal counter is prohibited from
dipping below 0 and when creating a Semaphore instance, an initial value can be specified via the value=x attr.

Note: A semaphore is prohibited from going below 0, if the initial counter (_value) is on 0 and a acquire() call is
performed it will block indefinitely, unless blocking=False is provided to the acquire() call.
"""

from threading import Semaphore


class CustomSemaphore(Semaphore):
    def __init__(self, value: int):
        super().__init__(value)

    @property
    def value(self) -> int:
        return self._value


def custom_semaphore():
    sema = CustomSemaphore(value=10)
    print(sema.value)  # 10
    for _ in range(5):
        sema.acquire()
    print(sema.value)  # 5
    for _ in range(100):
        sema.release()
    print(sema.value)  # 105

    # Now call it down to 0, without calling it again to avoid blocking forever.
    for _ in range(105):
        sema.acquire()
    print(sema.value)  # 0 (Note: if we call this again, it will block waiting for a `release()` call

    sema.acquire(blocking=False)


def semaphore_ctx():
    # Semaphores can be used as context managers!
    # This example is much better managed with a BoundedSemaphore!
    max_connections = 5
    with CustomSemaphore(value=max_connections) as sema:
        # do_something()
        ...


def semaphore_valuerror():
    CustomSemaphore(value=-10)


if __name__ == '__main__':
    custom_semaphore()
    semaphore_ctx()
    semaphore_valuerror()