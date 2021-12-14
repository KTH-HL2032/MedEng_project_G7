from src.oBCI_prc.obcicore import ObciCore
import time

start = True
P = ObciCore()
p = P.processing()

while start == True:
    time_diff_cha1, time_diff_cha2, time_diff_cha3, activation_cha1, activation_cha2, activation_cha3, loop_time,  muscle = next(p)
    time.sleep(loop_time)
    #print("Channel 1\n", "time diff", time_diff_cha1, "activated", activation_cha1)
    #print("Channel 2\n", "time diff", time_diff_cha2, "activated", activation_cha2)
    print("Channel 3\n", "time diff", time_diff_cha3, "Msucle activated", muscle, "Robot activated", activation_cha3)

#N = Niryo(time_diff_cha1, time_diff_cha2, time_diff_cha3, activation_cha1, activation_cha2, activation_cha3)