import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

def animate(i):
    data = pd.read_csv('data_sets/data.csv')
    x = data['x_value']
    y1 = data['total_1']


    plt.cla()
    plt.plot(x, y1, label='Channel 1')


    plt.legend(loc = 'upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval = 5)

plt.tight_layout()
plt.show()