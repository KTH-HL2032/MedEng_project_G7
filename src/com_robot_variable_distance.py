from niryo_one_tcp_client import *
from pynput import keyboard
import time


niryo_one_client = NiryoOneClient()
niryo_one_client.connect("10.10.10.10")  # WLAN: 10.10.10.10; LAN: 169.254.200.200


initial_pose = None


def on_key_release(key):  #Everything happens when the button is released so it knows how long the button was pressed
    time_taken = round(time.time() - t, 3)  #calculates the time difference
    print(key.char, time_taken)  #char is necessary otherwise the if statements below do not work

    if key.char == 'l':  #Gets current position as array [x,y,z,roll,pitch,yaw]
        status, data = niryo_one_client.get_pose()
        if status is True:
            print(PoseObject.to_list(data))
        else:
            print("Error: " + data)

    if key.char == 'w':  #moves to robot in the positive x-axis
        print("up")
        status, data = niryo_one_client.shift_pose(RobotAxis.X, time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 's':  #moves the robot in the negative x-axis
        print("down")
        status, data = niryo_one_client.shift_pose(RobotAxis.X, -time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 'a':  #moves the robot in the positive y-axis
        print("left")
        status, data = niryo_one_client.shift_pose(RobotAxis.Y, time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 'd':  #moves the robot in the negative y-axis
        print("right")
        status, data = niryo_one_client.shift_pose(RobotAxis.Y, -time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 'n':  #moves the robot in the positive z-axis (UP)
        print("up")
        status, data = niryo_one_client.shift_pose(RobotAxis.Z, time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 'm':  #moves the robot in the negative z-axis (DOWN)
        print("down")
        status, data = niryo_one_client.shift_pose(RobotAxis.Z, -time_taken*0.1)
        if status is False:
            print("Error: " + data)

    if key.char == 'p':  #the robot goes into learning mode (otherwise the robot stays on and is loud)

        print("stop")
        status, data = niryo_one_client.set_learning_mode(True)

        if status is False:
            print("Error: " + data)

    return False  #only one input at a time is allowed


def on_key_press(key):  #This function just detects that the button was pressed but nothing else. Can be modified if necessary
    return False


while True:

    with keyboard.Listener(on_press=on_key_press) as press_listener:  #The listener just records if a button is pressing down or released
        press_listener.join()

    t = time.time()  #Sets current time

    with keyboard.Listener(on_release=on_key_release) as release_listener:
        release_listener.join()
