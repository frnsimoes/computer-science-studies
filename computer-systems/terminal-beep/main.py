import sys
import time


def beep():
    number = sys.stdin.read(1)
    if number == 0:
        return
    try:
        number = int(number)
    except Exception:
        sys.stdout.write('not a number')
        return

    for _ in range(number):
        sys.stdout.buffer.write(b'\x07')
        sys.stdout.buffer.flush()
        time.sleep(1)


beep()
