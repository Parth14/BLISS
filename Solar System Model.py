# source /Users/parth/Desktop/BLISS/simulations/bin/activate

import matplotlib.pyplot as plt
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

#print(len(earth.y[0]), len(venus.y[0]), len(mars.y[0]))

#print(earth.y)

#sail_in_1 = solve_ivp(Fsail, [0, 3.2e7], [AU, 0, 0, 30], rtol=1e-8, args=[-0.5])
#sail_in_2 = solve_ivp(Fsail, [0, 3.2e7], [AU, 0, 0, 30], rtol=1e-8, args=[-0.75])
#sail_in_3 = solve_ivp(Fsail, [0, 3.2e7], [AU, 0, 0, 30], rtol=1e-8, args=[-1])

#sail_out = solve_ivp(Fsail, [0, 5e7], [AU, 0, 0, 30], rtol=1e-8, args=[1.])
#print(len(venus.y[0]))
#plt.plot(venus.y[0], venus.y[1])
#plt.plot(earth.y[0], earth.y[1])
#plt.plot(mars.y[0], mars.y[1])

#plt.plot(sail_in_3.y[0], sail_in_3.y[1])
#plt.plot(sail_out.y[0], sail_out.y[1])

#plt.show()


venus_x = []
venus_y = []
earth_x = []
earth_y = []
# sail_in_1_x = []
# sail_in_1_y = []
# sail_in_2_x = []
# sail_in_2_y = []
# sail_in_3_x = []
# sail_in_3_y = []
sail_in_x = [0]
sail_in_y = [0]
count = 0
angle = -1
# def onclick(event):
#     if event.button == 1:
#          venus_x.append(venus.y[0][0])
#          venus_y.append(venus.y[1][0])
#          #print(venus_x)
#          venus.y = np.delete(venus.y, [0], axis=1)
#     #clear frame
#     plt.clf()#
#     plt.plot(earth.y[0], earth.y[1])
#     plt.plot(venus_x, venus_y); #inform matplotlib of the new data
#     plt.draw() #redraw

prev_sail = solve_ivp(Fsail, [0, 5e7], [AU, 0, 0, 30], rtol=1e-8, args=[-1], t_eval=t_vals)
print(prev_sail.t)
#prev_sail.y = [ [AU], [0], [0], [30] ]
sail_in_x.append(prev_sail.y[0][0])
sail_in_y.append(prev_sail.y[1][0])

def keyclick(event):
    #if event.key == 'up':
         #venus_x.append(venus.y[0][0])
         #venus_y.append(venus.y[1][0])
         #print(venus_x)
         #venus.y = np.delete(venus.y, [0], axis=1)
    #clear frame
    global count 
    global prev_sail
    global angle
    global t_vals
    #venus_x.append(venus.y[0][0])
    #venus_y.append(venus.y[1][0])
    #venus.y = np.delete(venus.y, [0], axis=1)

    # earth_x.append(earth.y[0][0])
    # earth_y.append(earth.y[1][0])
    # earth.y = np.delete(earth.y, [0], axis=1)

    if event.key == 'left':
        angle += -0.05
        
    elif event.key == 'right':
        angle += 0.05
    elif event.key == 'up':
        angle += 0.0


    #print("lenx", len(sail_in_x))
    #print("leny", len(sail_in_y))
    #dist = pow(sail_in_x[len(sail_in_x)-1]**2 + sail_in_y[len(sail_in_y)-1]**2 , 0.5)
    print(angle)
    current_sail = solve_ivp(Fsail, [0, 5e5], [prev_sail.y[0][1], prev_sail.y[1][1], prev_sail.y[2][1], prev_sail.y[3][1],], rtol=1e-8, args=[angle], t_eval=[0, 5e5])
    #current_sail = solve_ivp(Fsail, [0, 3.2e7], [AU, 0, 0, 30], rtol=1e-8, args=[angle])

    sail_in_x.append(current_sail.y[0][0])
    sail_in_y.append(current_sail.y[1][0])


    plt.clf()#
    plt.plot(mars.y[0], mars.y[1])
    plt.plot(earth.y[0][:count], earth.y[1][:count])
    plt.plot(venus.y[0][:count], venus.y[1][:count]) 
    plt.plot(sail_in_x, sail_in_y)
    #print(sail_in_x, sail_in_y)
    plt.draw() #redraw
    prev_sail = current_sail
    count += 1

fig,ax=plt.subplots()
#ax.scatter(venus_x, venus_y)
#fig.canvas.mpl_connect('button_press_event',onclick)
fig.canvas.mpl_connect('key_press_event',keyclick)

plt.show()
plt.draw()
