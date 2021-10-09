import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
from scipy.integrate import solve_ivp
mu = 1.327e20 /1e9 # mu in km^3/s^2
AU = 1.496e11 /1e3 # AU in km
beta = 0.15

# s = [x, y, vx, vy]
# F returns s_dot = [vx, vy, ax, ay]
# r = [x, y]
# a = -mu/|r|**2 r_hat = -mu/|r|**3 [x,y]
def Fsun(t,s):
    rcubed = (s[0]**2+s[1]**2)**(3/2)
    ax = -mu*s[0]/rcubed
    ay = -mu*s[1]/rcubed
    return [s[2], s[3], ax, ay]

def Fsail(t,s,cone):
    rsquared = s[0]**2 + s[1]**2
    rcubed = (rsquared)**(3/2)
    asunx = -mu*s[0]/rcubed
    asuny = -mu*s[1]/rcubed
    theta = math.atan2(s[1],s[0])
    asail = beta*mu/rsquared*math.cos(cone)**2
    asailx = asail*math.cos(theta+cone)
    asaily = asail*math.sin(theta+cone)
    return [s[2], s[3], asunx+asailx, asuny+asaily]

t_vals = [5e7/100 * x for x in range(100)]

venus = solve_ivp(Fsun, [0, 5e7], [0.72*AU, 0, 0, 35], rtol=1e-8, t_eval=t_vals)
earth = solve_ivp(Fsun, [0, 5e7], [AU, 0, 0, 30], rtol=1e-8, t_eval=t_vals)
mars = solve_ivp(Fsun, [0, 5e7], [1.5*AU, 0, 0, 24], rtol=1e-8, t_eval=t_vals)

sail_in_x = []
sail_in_y = []
count = 0
angle = -1

prev_sail = solve_ivp(Fsail, [0, 5e7], [AU, 0, 0, 30], rtol=1e-8, args=[-1], t_eval=t_vals)
print(prev_sail.t)
sail_in_x.append(prev_sail.y[0][0])
sail_in_y.append(prev_sail.y[1][0])

def keyclick(event):
    
    global count 
    global prev_sail
    global angle
    global t_vals
    
    if event.key == 'left':
        angle += -0.05
    elif event.key == 'right':
        angle += 0.05

    print(angle)
    current_sail = solve_ivp(Fsail, [0, 5e5], [prev_sail.y[0][1], prev_sail.y[1][1], prev_sail.y[2][1], prev_sail.y[3][1],], rtol=1e-8, args=[angle], t_eval=[0, 5e5])

    sail_in_x.append(current_sail.y[0][0])
    sail_in_y.append(current_sail.y[1][0])


    plt.clf()
    plt.plot([-2.5e8, -2.5e8, 2.5e8, 2.5e8, -2.5e8], [-2.5e8, 2.5e8, 2.5e8, -2.5e8, -2.5e8], color="white")
    plt.plot(earth.y[0][:count], earth.y[1][:count])
    plt.plot(venus.y[0][:count], venus.y[1][:count]) 
    plt.plot(mars.y[0][:count],  mars.y[1][:count]) 
    plt.plot(sail_in_x, sail_in_y)
    plt.draw()
    prev_sail = current_sail
    count += 1

fig,ax=plt.subplots()
fig.canvas.mpl_connect('key_press_event',keyclick)

plt.show()
plt.draw()
