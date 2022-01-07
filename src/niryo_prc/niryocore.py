from niryo_one_tcp_client import *
import math


class NiryoCore:

    def __init__(self):
        self.time_diff_cha1 = 0
        self.time_diff_cha2 = 0
        self.time_diff_cha3 = 0
        self.activation_cha1 = False
        self.activation_cha2 = False
        self.activation_cha3 = False
        self.time_taken = 0
        self.channel = 0
        self.niryo_one_client = NiryoOneClient()

        self.verbose = True

    def connect(self):
        print("Start")
        self.niryo_one_client.connect("10.10.10.10")  # WLAN: 10.10.10.10; LAN: 169.254.200.200

        status, data = self.niryo_one_client.calibrate(CalibrateMode.AUTO)
        if status is False:
            print("Error: " + data)

        status, data = self.niryo_one_client.move_joints(0.0, -0.73, -0.787, 0.0, 0.0, 0.0) #Starting point of the robot
        if status is False:
            print("Error: " + data)

    def rom_calc(self, pos_list, time_diff, channel):  # Calculates the shift and checks if the end position of the end
        # effector is still in the allowed area

        in_rad = 0.16
        o_rad = 0.3

        if channel == 3:
            # move left
            pre1 = 1
            pre_i = -1
            pre_o = 1
            changing_index = 1
            fix_index = 0

        elif channel == 2:
            # move right
            pre1 = -1
            pre_i = 1
            pre_o = -1
            changing_index = 1
            fix_index = 0

        else:
            print("No direction key")
            return False

        shift = pre1 * time_diff * 0.1  # sets shift amount
        changing_dir = shift + pos_list[changing_index]  # computes end position changing axis
        fix_dir = pos_list[fix_index]  # end position on fix axis
        if math.sqrt(changing_dir ** 2 + fix_dir ** 2) <= in_rad:  # checks if end_position is beyond set inner radius
            changing_dir = math.sqrt(in_rad ** 2 - fix_dir ** 2)  # computes new min end position on changing axis
            shift = pre_i * changing_dir - pos_list[
                changing_index]  # computes new max shift that is still allowed to keep
            # the arm above inner radius

        if math.sqrt(changing_dir ** 2 + fix_dir ** 2) >= o_rad:  # checks if end_position is beyond set outer radius
            changing_dir = math.sqrt(o_rad ** 2 - fix_dir ** 2)  # computes new max end position on changing axis
            shift = pre_o * changing_dir - pos_list[
                changing_index]  # computes new max shift that is still allowed to keep
            # the arm in below outer radius
        return shift

    def processing(self, time_diff_ch2, time_diff_ch3):

        status_pos, data_pos = self.niryo_one_client.get_pose()
        pos_list = PoseObject.to_list(data_pos)

        if time_diff_ch3 > 0 and time_diff_ch2 == 0:  # moves the robot in the positive y-axis
            ch = 3
            if self.verbose:
                print("left")
                print(self.rom_calc(pos_list, time_diff_ch3, ch))
            status, data = self.niryo_one_client.shift_pose(RobotAxis.Y, self.rom_calc(pos_list, time_diff_ch3, ch))
            if status is False:
                print("Error: " + data)

        elif time_diff_ch2 > 0 and time_diff_ch3 == 0:  # moves the robot in the negative y-axis
            ch = 2
            if self.verbose:
                print("right")
                print(self.rom_calc(pos_list, time_diff_ch2, ch))
            status, data = self.niryo_one_client.shift_pose(RobotAxis.Y, self.rom_calc(pos_list, time_diff_ch2, ch))
            if status is False:
                print("Error: " + data)

