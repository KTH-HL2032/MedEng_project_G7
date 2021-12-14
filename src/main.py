from src.niryo_prc.niryocore import NiryoCore
from oBCI_prc.obcicore import *


def run():

    verbose = True
    niryocore_instance = NiryoCore()
    niryocore_instance.connect()

    obcicore_instance = ObciCore()
    p = obcicore_instance.processing()

    while True:
        time_diff_ch1, time_diff_ch2, time_diff_ch3, activation_ch1, activation_ch2, activation_ch3, loop_time, muscle_activated_3 = next(p)
        time.sleep(loop_time)
        if verbose:
            # print("Channel 1\n", "time diff", time_diff_ch1, "activated", activation_ch1)
            # print("Channel 2\n", "time diff", time_diff_ch2, "activated", activation_ch2)
            print("Channel 3\n", "time diff", time_diff_ch3, "Msucle activated", muscle_activated_3, "Robot activated",activation_ch3)

        niryocore_instance.processing(time_diff_ch3)


if __name__ == '__main__':
    run()




