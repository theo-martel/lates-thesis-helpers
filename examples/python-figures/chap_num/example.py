try:
    figure
except:
    import matplotlib.pyplot as plt
    figure = plt.figure()
    plt.rcdefaults()

import numpy as np
from scipy.stats import linregress

data = np.load("dataset.npy")

ax = figure.subplots()
ax.scatter(*data)
ax.set_ylabel("$I_{meas}$ (dBm)")
ax.set_xlabel("$P$ (dBm)")
ax.text(0.03,0.96,"(a)",ha='left',va='top',transform = ax.transAxes)
res = linregress(*data)
ax.plot(data[0],res.intercept+res.slope*data[0],color='tab:orange')
ax.text(data[0,-1],res.intercept+res.slope*data[0,-1]-2,f"$R^2 = {res.rvalue**2:.2}$",
         fontsize='small',ha='right',va='top',rotation=np.arctan(res.slope)*180/np.pi,rotation_mode='anchor',color='#cb5f00',transform_rotates_text=True)
