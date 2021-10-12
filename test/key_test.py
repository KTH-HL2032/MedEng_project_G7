import win32api
import time

while True:
  up = win32api.GetKeyState(0x57)
  down = win32api.GetKeyState(0x53)
  left = win32api.GetKeyState(0x41)
  right = win32api.GetKeyState(0x44)

  if up<0:
    print("up")
    time.sleep(0.1)

  if down<0:
    print("down")
    time.sleep(0.1)

  if left<0:
    print("left")
    time.sleep(0.1)

  if right<0:
    print("right")
    time.sleep(0.1)

