import pyfirmata
import time
import realtime
import subprocess
import os

db_dir = realtime.encoding

frame = realtime.ImageTk

unknown_img_path = './.tmp.png'
realtime.cv2.imwrite(unknown_img_path, frame)

output = subprocess.check_output(['face_recognition', db_dir, unknown_img_path])
print(output)

def perluangan ():

    if True in output :
        print('high')
        time.sleep(1)
    else:
        print('low')
        time.sleep(1)

os.remove(unknown_img_path)