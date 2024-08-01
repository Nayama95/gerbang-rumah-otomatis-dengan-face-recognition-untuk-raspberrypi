
import gpiod
import time
import subprocess

GPIO_CHIP = "gpiochip4"
GPIO_LINE_1 = 23
GPIO_LINE_2 = 4
GPIO_LINE_3 = 24
GPIO_LINE_4 = 17
STEPS_PER_REVOLUTION = 540
DELAY = 0.001

direction = -1 
revolutions = 10 

def set_output(lines, a, b, c, d):
    values = [a, b, c, d]
    lines.set_values(values)

def reverse_direction():
    global direction
    if direction == 1:
        direction = -1
    elif direction == -1:
        direction = 1

def set_direction(d):
    global direction
    if d == 1 or d == -1:
        direction = d

def set_revolutions(r):
    global revolutions
    if isinstance(r, int):
        revolutions = r

chip = gpiod.Chip(GPIO_CHIP)
if chip is None:
    print("gpiod.Chip open failed")
    exit(-1)

lines = chip.get_lines([GPIO_LINE_1, GPIO_LINE_2, GPIO_LINE_3, GPIO_LINE_4])
if lines is None:
    print("gpiod.Chip get_lines failed")
    chip.close()
    exit(-1)

status = lines.request(consumer="stepper", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0, 0, 0, 0])
if status is not None and status < 0:
    print("gpiod.Line request failed")
    chip.close()
    exit(-1)

steps = STEPS_PER_REVOLUTION * abs(revolutions) 
for i in range(steps):
    if direction == 1:
        if i % 8 == 0:
            set_output(lines, 1, 0, 0, 0)
        elif i % 8 == 1:
            set_output(lines, 1, 1, 0, 0)
        elif i % 8 == 2:
            set_output(lines, 0, 1, 0, 0)
        elif i % 8 == 3:
            set_output(lines, 0, 1, 1, 0)
        elif i % 8 == 4:
            set_output(lines, 0, 0, 1, 0)
        elif i % 8 == 5:
            set_output(lines, 0, 0, 1, 1)
        elif i % 8 == 6:
            set_output(lines, 0, 0, 0, 1)
        elif i % 8 == 7:
            set_output(lines, 1, 0, 0, 1)
    elif direction == -1:
        if i % 8 == 0:
            set_output(lines, 1, 0, 0, 1)
        elif i % 8 == 1:
            set_output(lines, 0, 0, 0, 1)
        elif i % 8 == 2:
            set_output(lines, 0, 0, 1, 1)
        elif i % 8 == 3:
            set_output(lines, 0, 0, 1, 0)
        elif i % 8 == 4:
            set_output(lines, 0, 1, 1, 0)
        elif i % 8 == 5:
            set_output(lines, 0, 1, 0, 0)
        elif i % 8 == 6:
            set_output(lines, 1, 1, 0, 0)
        elif i % 8 == 7:
            set_output(lines, 1, 0, 0, 0)
    time.sleep(DELAY)

set_output(lines, 0, 0, 0, 0)
lines.release()
chip.close()
p = subprocess.run(["python", "programcounter.py"])
