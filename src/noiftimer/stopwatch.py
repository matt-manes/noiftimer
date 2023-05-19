import threading
import time

from printbuddies import print_in_place

from noiftimer import Timer

QUIT = False


def input_(prompt: str = ""):
    global QUIT
    value = input(prompt)
    if value == "q":
        QUIT = True


def stopwatch():
    input_thread = threading.Thread(target=input_, daemon=True)
    input_("Press enter to start. ")
    if not QUIT:
        print("Press enter to stop.")
    timer = Timer(subsecond_resolution=False).start()
    input_thread.start()
    while input_thread.is_alive() and not QUIT:
        print_in_place(f" {timer.elapsed_str} ")
        time.sleep(1)


def main():
    print("Press 'q' and then enter to quit at any time.")
    while not QUIT:
        stopwatch()


if __name__ == "__main__":
    main()
