import time

from printbuddies import print_in_place

from noiftimer import Timer


def main():
    timer = Timer(subsecond_resolution=False).start()
    while True:
        try:
            print_in_place(f" {timer.elapsed_str}")
            time.sleep(1)
        except Exception as e:
            break


if __name__ == "__main__":
    main()
