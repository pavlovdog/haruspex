import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys
import env_data
from scipy import polyval, polyfit

# followings = env_data.count_followings()
# followers = env_data.count_followers()
# media = env_data.count_media()

age = env_data.list_ages()



# PLOTTING
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.plot(media, age, 'bo')
ax1.set_ylabel("Ages")

plt.grid(True)

plt.show()
