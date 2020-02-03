import time
from threading import Thread


def blocks_main_thread_for_10_seconds():
    """
    Setting the daemon as False forces the main thread to have to wait (blocked-by) the deamon thread running.
    """
    print_meta_data(blocks_main_thread_for_10_seconds.__name__)
    non_daemon_thread = Thread(daemon=False, target=lambda: time.sleep(10))
    non_daemon_thread.start()


def main_thread_is_not_blocked():
    """
    Setting the daemon as True signals that when the main execution of the program has done its work it should not
    wait for daemon threads to finish; however it is possible to call .join() which will infact block on the daemon
    thread.
    """
    print_meta_data(main_thread_is_not_blocked.__name__)
    daemon_thread = Thread(daemon=True, target=lambda: time.sleep(10))
    daemon_thread.start()


def non_daemon_but_blocking():
    """
    Setting the daemon as True signals that when the main execution of the program has done its work it should not
    wait for daemon threads to finish; however it is possible to call .join() which will infact block on the daemon
    thread.
    """
    print_meta_data(non_daemon_but_blocking.__name__)
    daemon_thread = Thread(daemon=True, target=lambda: time.sleep(10))
    daemon_thread.start()
    daemon_thread.join()


def print_meta_data(function_name):
    print(f"Executing: {function_name}")


def main():
    blocks_main_thread_for_10_seconds()  # will sleep for 10 seconds
    main_thread_is_not_blocked()  # will end immediately
    non_daemon_but_blocking()  # will sleep for 10 seconds even on a daemon


if __name__ == '__main__':
    main()
