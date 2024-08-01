import gpiod
import time

# Konfigurasi pin GPIO
chip = gpiod.Chip('gpiochip4')  # Ganti dengan nama chip GPIO yang sesuai
motor_pins = [23, 4, 24, 17]  # Ganti dengan pin GPIO yang terhubung ke driver ULN2003

# Konfigurasi mode pin sebagai output
for pin in motor_pins:
    line = chip.get_line(pin)
    line.request(consumer='my_motor', type=gpiod.LINE_REQ_DIR_OUT)

# Urutan langkah motor (CW dan CCW)
steps_forward = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

steps_backward = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
]

try:
    while True:
        # Maju
        for step in steps_forward:
            for i, pin in enumerate(motor_pins):
                line = chip.get_line(pin)
                line.set_value(step[i])
            time.sleep(1)  # Waktu antar langkah

        # Mundur
        for step in steps_backward:
            for i, pin in enumerate(motor_pins):
                line = chip.get_line(pin)
                line.set_value(step[i])
            time.sleep(1)  # Waktu antar langkah

except KeyboardInterrupt:
    pass
finally:
    # Bersihkan pin GPIO
    for pin in motor_pins:
        line = chip.get_line(pin)
        line.release()

# Tutup koneksi ke chip GPIO
chip.close()
