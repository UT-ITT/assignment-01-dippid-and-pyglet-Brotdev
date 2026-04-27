import socket
import numpy as np
import time

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0
while True:
    # Toggle button on and off repeatedly
    btn1_msg = f'{{"button_1": {counter % 2}}}'

    # Generate continous accelerometer data with small
    # gaussian noise
    noise = np.random.normal(0, 0.05, 3)
    accl_x = 0.1 * np.sin(time.time() * 0.5)  + noise[0]
    accl_y = 0.2 * np.sin(time.time() * 0.75) + noise[1]
    accl_z = 1.0 + 0.1 * np.sin(time.time())  + noise[2]
    accl_msg = f'{{"accelerometer": {{"x":{accl_x},"y":{accl_y},"z":{accl_z}}} }}'

    print(btn1_msg)
    print(accl_msg)

    sock.sendto(btn1_msg.encode(), (IP, PORT))
    sock.sendto(accl_msg.encode(), (IP, PORT))

    counter += 1
    time.sleep(0.1)
