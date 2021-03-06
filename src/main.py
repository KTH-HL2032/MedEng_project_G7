from src.niryo_prc.niryocore import NiryoCore
from oBCI_prc.obcicore import *


def run():

    verbose = True
    niryocore_instance = NiryoCore()
    niryocore_instance.connect()

    obcicore_instance = ObciCore()
    p = obcicore_instance.processing()

    while True:
        time_diff_ch2, time_diff_ch3, muscle_activated_2, muscle_activated_3, loop_time = next(p)
        time.sleep(loop_time)
        if verbose:
            print("Channel 2\n", "time diff", time_diff_ch2, "Muscle activated", muscle_activated_2)
            print("Channel 3\n", "time diff", time_diff_ch3, "Msucle activated", muscle_activated_3)

        niryocore_instance.processing(time_diff_ch2, time_diff_ch3)


if __name__ == '__main__':
    run()




