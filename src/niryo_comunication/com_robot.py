import win32api
import time
from niryo_one_tcp_client import *

niryo_one_client = NiryoOneClient()
niryo_one_client.connect("10.10.10.10") # WLAN: 10.10.10.10; LAN: 169.254.200.200


initial_pose = None


status, data = niryo_one_client.calibrate(CalibrateMode.AUTO)
if status is False:
    print("Error: " + data)


status, data = niryo_one_client.get_pose()
if status is True:
    initial_pose = data
else:
    print("Error: " + data)

status, data = niryo_one_client.shift_pose(RobotAxis.X, 0.5)



while True:
  up = win32api.GetKeyState(0x57)
  down = win32api.GetKeyState(0x53)
  left = win32api.GetKeyState(0x41)
  right = win32api.GetKeyState(0x44)
  stopp = win32api.GetKeyState(0x20)
  nach_l = win32api.GetKeyState(0x11)

  if up<0:
    print("up")
    status, data = niryo_one_client.shift_pose(RobotAxis.X, 0.025)
    if status is False:
        print("Error: " + data)


  if down<0:
    print("down")
    status, data = niryo_one_client.shift_pose(RobotAxis.X, -0.025)
    if status is False:
        print("Error: " + data)


  if left<0:
    print("left")
    status, data = niryo_one_client.shift_pose(RobotAxis.Y, 0.1)
    if status is False:
        print("Error: " + data)


  if right<0:
    print("right")
    status, data = niryo_one_client.shift_pose(RobotAxis.Y, -0.025)
    if status is False:
        print("Error: " + data)

  if stopp<0:
    print("stop")
    status, data = niryo_one_client.set_learning_mode(True)
    if status is False:
        print("Error: " + data)

"""
  if right<0:
    start_time=time.time()
  elif right>=0:
    end_time=time.time()-start_time

"""