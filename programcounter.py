import time
import gpiod
import subprocess

chip = gpiod.Chip("gpiochip4")
line = chip.get_line(14)
line.request(consumer="counter", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN)

counter = 0
state = 0

while True:
    value = line.get_value()
    if value == 1:
        if state == 0:
            counter += 1
            state = 1
            print("Counter:", counter)

            if counter > 1:
                p = subprocess.run(["python", "stepper_searah_jarum_jam.py"])
                line.release()
                chip.close()
    else:
        state = 0
    time.sleep(0.1)