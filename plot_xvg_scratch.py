import numpy as np
import matplotlib.pyplot as plt

nstep = []
E_pot = []
with open("potential.xvg") as f:
    for line in f:
        data = line.split()
        if len(data) == 2:
            try:
                nstep.append(float(data[0]))
                E_pot.append(float(data[1]))
            except:
                pass

f1, ax1 = plt.subplots(figsize=(8,6))
ax1.plot(nstep, E_pot)
ax1.set_xlabel("Energy Minimization Step")
ax1.set_ylabel("Potential Energy (kJ/mol)")
ax1.set_title("Energy Minimization, 1AKI, Steepest Descent")
f1.show()

time = []  # time in ps
temp = []  # temp in K
with open("temperature.xvg") as f:
    for line in f:
        data = line.split()
        if len(data) == 2:
            try:
                time.append(float(data[0]))
                temp.append(float(data[1]))
            except:
                pass

f2, ax2 = plt.subplots(figsize=(8,6))
ax2.plot(time, temp)
ax2.set_xlabel("Time (ps)")
ax2.set_ylabel("Temperature (K)")
ax2.set_title("Temperature, 1AKI, NVT Equilibration")
f2.show()

plt.show()