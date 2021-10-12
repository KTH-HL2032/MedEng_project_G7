from niryo_one_tcp_client import *
import win32api
import time
import math

niryo_one_client = NiryoOneClient()
niryo_one_client.connect("10.10.10.10") # WLAN: 10.10.10.10; LAN: 169.254.200.200


i_radius = 0.16
a_radius = 0.30
a=0

def check_FOM(x_co, y_co, alt_var):
    radius = x_co**2+y_co**2

    if radius >= i_radius and radius <= a_radius:
        return x_co, y_co
    elif radius > a_radius and alt_var == 1:
        x_neu = math.sqrt(a_radius)-y_co**2
        return x_neu, y_co
    elif radius > a_radius and alt_var == 1:
        y_neu = math.sqrt(a_radius) - x_co ** 2
        return x_co, y_neu


while True:
  up = win32api.GetKeyState(0x57)
  down = win32api.GetKeyState(0x53)
  left = win32api.GetKeyState(0x41)
  right = win32api.GetKeyState(0x44)
  stopp = win32api.GetKeyState(0x20)





