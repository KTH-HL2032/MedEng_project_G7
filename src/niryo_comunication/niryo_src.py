from niryo_one_tcp_client import *
from src.oBCI_processing.oBCI_prc_class import Processing
import time
import math
from pynput import keyboard


niryo_one_client = NiryoOneClient()
niryo_one_client.connect("10.10.10.10")  # WLAN: 10.10.10.10; LAN: 169.254.200.200


initial_pose = None


#  KEYS FOR MOVING
#  'w': End effector moves in the direction of positive x-axis
#  's': End effector moves in the direction of negative x-axis
#  'a': End effector moves in the direction of positive y-axis
#  'd': End effector moves in the direction of negative y-axis
#  'n': End effector moves in the direction of positive z-axis
#  'm': End effector moves in the direction of negative z-axis

#  SPECIAL KEYS
#  'c': Calibrates the robot
#  'l': Gives end effector position [x,y,z,roll,pitch,yaw]
#  'p': Sets the robot to learning mode


class Niryo:

    def __init__(self):
        self.time_diff_cha1 = 0
        self.time_diff_cha2 = 0
        self.time_diff_cha3 = 0
        self.activation_cha1 = False
        self.activation_cha2 = False
        self.activation_cha3 = False
        self.time_taken = 0
        self.channel = 0

    def rom_calc(self, pos_list):

        in_rad = 0.16
        o_rad = 0.3

        if self.activation_cha1:
            pre1 = 1
            pre_i = -1
            pre_o = 1
            changing_index = 1
            fix_index = 0
            self.time_taken = self.time_diff_cha1

        elif self.activation_cha2:
            pre1 = -1
            pre_i = 1
            pre_o = -1
            changing_index = 1
            fix_index = 0
            self.time_taken = self.time_diff_cha2

        else:
            print("No direction key")
            return False

        shift = pre1*self.time_taken * 0.1  # sets shift amount
        changing_dir = shift + pos_list[changing_index]  # computes end position changing axis
        fix_dir = pos_list[fix_index]  # end position on fix axis
        if math.sqrt(changing_dir ** 2 + fix_dir ** 2) <= in_rad:  # checks if end_position is beyond set inner radius
            changing_dir = math.sqrt(in_rad ** 2 - fix_dir ** 2)  # computes new min end position on changing axis
            shift = pre_i*changing_dir - pos_list[changing_index]  # computes new max shift that is still allowed to keep
            # the arm above inner radius

        if math.sqrt(changing_dir ** 2 + fix_dir ** 2) >= o_rad:  # checks if end_position is beyond set outer radius
            changing_dir = math.sqrt(o_rad ** 2 - fix_dir ** 2)  # computes new max end position on changing axis
            shift = pre_o*changing_dir - pos_list[changing_index]  # computes new max shift that is still allowed to keep
            # the arm in below outer radius
        return shift

    def on_key_release(self,key):  # Everything happens when the button is released so it knows how long the button was pressed

        status_pos, data_pos = niryo_one_client.get_pose()
        pos_list = PoseObject.to_list(data_pos)

        if status_pos is True:
            print(PoseObject.to_list(data_pos))
        else:
            exit()

        if key.char == 'c':
            status, data = niryo_one_client.calibrate(CalibrateMode.AUTO)
            if status is False:
                print("Error: " + data)

        if key.char == 'l':  # Gets current position as array [x,y,z,roll,pitch,yaw] // char is necessary to work
            status, data = niryo_one_client.get_pose()
            if status is True:
                print(PoseObject.to_list(data))
            else:
                print("Error: " + data)

        if key.char == 'p':  # the robot goes into learning mode (otherwise the robot stays on and is loud)

            print("stop")
            status, data = niryo_one_client.set_learning_mode(True)

            if status is False:
                print("Error: " + data)
        return False  # only one input at a time is allowed

    def niryo_processing(self):

        status_pos, data_pos = niryo_one_client.get_pose()
        pos_list = PoseObject.to_list(data_pos)

        if self.time_diff_cha1:  # moves the robot in the positive y-axis
            print("left")

            print(Niryo.rom_calc(pos_list))
            status, data = niryo_one_client.shift_pose(RobotAxis.Y, Niryo.rom_calc(pos_list))
            if status is False:
                print("Error: " + data)

        if self.time_diff_cha2:  # moves the robot in the negative y-axis
            print("right")

            print(Niryo.rom_calc(pos_list))
            status, data = niryo_one_client.shift_pose(RobotAxis.Y, Niryo.rom_calc(pos_list))
            if status is False:
                print("Error: " + data)



while True:

    with keyboard.Listener(on_release=Niryo.on_key_release) as release_listener:
        release_listener.join()
