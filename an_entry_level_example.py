import time
from dataclasses import dataclass
from pyclbr import Function
from queue import Queue
from random import randrange
from threading import Thread
import datetime
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

available_work = Queue()  # Global FIFO thread safe queue (maxsize=0 as the world truly is our oyster)
daily_profit = 0


class Human(Thread):
    """
    The human in our factory is considered a thread of execution; each human has repeatable mundane tasks to be
    carried out in order for the factory to prosper.  Humans are lazy; only when their manager has work for them to do
    will they actually do any, times are hard for the factory owner and business orders are few and far between!

    Unfortunately humans are 'expendable' to the factory and that is why we mark them as 'daemon'.  This essentially
    means even tho they might have work to do, at any given time the factory can just close the doors and cease trading!
    Protests won't be allowed and nothing the humans can block the factory from locking up.
    """
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        """
        When a piece of work is available for our factory worker, they will get motivated and begin doing it!
        """
        logger.info(f"Human: {self.ident} has found some work to do...!")
        while True:
            # we will run forever until the factory closes up shop
            current_task = available_work.get()
            current_task.work()
            time.sleep(current_task.time_to_complete)
            logger.info(f"{self.ident} completed a task and earned the business ${current_task.net_profit:.2f}")
            logger.info(f"Task was {current_task}")
            global daily_profit
            daily_profit += current_task.net_profit
            logger.info(f"current daily profit: ${daily_profit:.2f}")
            available_work.task_done()


class Factory:
    """
    This is our factory; the building in which workers reside throughout the day, carrying out their tasks
    """
    def __init__(self, workers: int = 8, multiplier: int = 8):
        self.workers = workers
        self.total_seconds_open = (60 * 60 * 8) / multiplier

    def generate_success(self):
        current_time = time.time()
        for _ in range(self.workers):
            worker = Human()
            worker.start()

            logger.info(f"Scanning the marker for new trade deals... we will work our staff into the ground!")
            closing_time = current_time + self.total_seconds_open
            logger.info(f"Factory is open for business until {datetime.datetime.utcfromtimestamp(closing_time)}")
            available_work.join()
            while current_time < closing_time:
                get_new_deals()
            else:
                logger.info(f"Factory has closed for the day, total profit today was: ${daily_profit:.2f}")


@dataclass(repr=True)
class Task:
    """
    This is a simple task; a task indicates how long a worker would take to complete it, but also how much it can
    net gain for the factory upon completion
    """
    work: Function = lambda: logger.info(f"Task is being executed with a uuid of: {uuid.uuid4()}")
    net_profit: float = 0.0
    time_to_complete: int = 0


def get_new_deals():
    if randrange(100) % 2 == 0:
        """
        With a 1 in 2 chance of generating a sweet new deal with an offshore partner, the factory is destined for great
        success!  Fail to negotiate tho and theres a hefty price to pay, you will be banned from the market for 10 secs
        The plot thickens however; some tasks are more lucrative than others and like everything in this world, it is
        completely random!  Tasks range from $100 - $15,000 and can take upwards of 10 seconds to complete!
        """
        logger.info(f"Deal secured... adding the tasks to the factories queue")
        available_work.put(Task(net_profit=randrange(100, 15000), time_to_complete=randrange(10)))

    else:
        logger.error(f"Sales manager failed to secure a deal; we are blacklisted for 10 seconds from the market")
        time.sleep(10)


def main():
    """
    This is the entry point, where it all begins;  Each day at exactly 8:00 sharp the factory opens its doors and for
    a period of 8 hours, can attempt to generate as much money as possible!  Ofcourse we don't want to wait for 8 hours
    at runtime, so we will use a speed up multiplier!
    """
    nike_factory = Factory(workers=32, multiplier=64)
    nike_factory.generate_success()


if __name__ == '__main__':
    main()
