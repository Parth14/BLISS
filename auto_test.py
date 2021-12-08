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

t_vals = [6e7/100 * x for x in range(100)]
t_sail = [6e6/10 * x for x in range(10)]
t_year = [3e6/5 * x for x in range(5)]
angles = [0, 0.5, 1.0, 1.57, 3.0]
angles_list = []

for a in angles:
    for b in angles:
        for c in angles:
            for d in angles:
                for e in angles:
                    angles_list.append([a, b, c, d, e])


venus = solve_ivp(Fsun, [0, 6e7], [0.72*AU, 0, 0, 35], rtol=1e-8, t_eval=t_vals)
earth = solve_ivp(Fsun, [0, 6e7], [AU, 0, 0, 30], rtol=1e-8, t_eval=t_vals)
mars = solve_ivp(Fsun, [0, 6e7], [1.5*AU, 0, 0, 24], rtol=1e-8, t_eval=t_vals)

sail_in_x = []
sail_in_y = []
count = 0
# angle = float(input("Enter the initial cone angle: "))
# increment = abs(float(input("Enter cone angle increment: ")))

prev_sail = solve_ivp(Fsail, [0, 6e7], [AU, 0, 0, 30], rtol=1e-8, args=[0], t_eval=[t_year[0], t_year[1]])
sail_in_x.append(prev_sail.y[0][0])
sail_in_y.append(prev_sail.y[1][0])
sail_xy_list = []

count = 0
for i in angles_list:
    sail_temp = []
    for j in range(len(i)):
        prev_sail = solve_ivp(Fsail, [0, 6e6], [prev_sail.y[0][1], prev_sail.y[1][1], prev_sail.y[2][1], prev_sail.y[3][1],], rtol=1e-8, args=[i[j]], t_eval=[t_year[0], t_year[1]])
        sail_temp.append([prev_sail.y[0][0], prev_sail.y[1][0]])
        #sail_temp[j].append(sail_temp[j][2]-1.5*AU)
    #sail_next_year = solve_ivp(Fsail, [0, 6e6], [prev_sail.y[0][1], prev_sail.y[1][1], prev_sail.y[2][1], prev_sail.y[3][1],], rtol=1e-8, args=[j], t_eval=t_year)

    count += 1
    sail_xy_list.append(sail_temp)
    print(count)
#print(sail_xy_list)

sail_dist = []
for i in sail_xy_list:
    # print(i)
    sail_dist.append( abs(math.sqrt(pow(i[4][0], 2) + pow(i[4][1], 2)) - 1.5*AU))
#print(sail_dist)

min_dist = sail_dist[0]
pos = 0

for i in range(len(sail_dist)):
    if sail_dist[i] < min_dist:
        min_dist = sail_dist[i]
        pos = i

print("min dist: ", min_dist)
print("pos: ", pos)
print("steps: ", angles_list[pos])
print("xy: ", sail_xy_list[pos])
print("percentage close: ", min_dist*200/AU)

# def keyclick(event):
    
#     global count 
#     global prev_sail
#     global angle
#     global t_vals
    
#     if event.key == 'left':
#         angle -= increment
#     elif event.key == 'right':
#         angle += increment

#     print(angle)
#     current_sail = solve_ivp(Fsail, [0, 6e6], [prev_sail.y[0][1], prev_sail.y[1][1], prev_sail.y[2][1], prev_sail.y[3][1],], rtol=1e-8, args=[angle], t_eval=t_sail)

#     sail_in_x.append(current_sail.y[0][0])
#     sail_in_y.append(current_sail.y[1][0])

#     plt.clf()
#     #rectangle to adjust axis
#     plt.plot([-2.5e8, -2.5e8, 2.5e8, 2.5e8, -2.5e8], [-2.5e8, 2.5e8, 2.5e8, -2.5e8, -2.5e8], color="white")

#     #sun
#     sun = plt.Circle((0, 0), 5e6, color='yellow')
#     plt.gca().add_patch(sun)

#     #planets full orbit
#     plt.plot(earth.y[0], earth.y[1], color="brown")
#     plt.plot(venus.y[0], venus.y[1], color="brown") 
#     plt.plot(mars.y[0],  mars.y[1], color="brown") 

#     #planets current
#     earth_ball = plt.Circle((earth.y[0][count], earth.y[1][count]), 5e6, color='blue')
#     plt.gca().add_patch(earth_ball)

#     venus_ball = plt.Circle((venus.y[0][count], venus.y[1][count]), 5e6, color='orange')
#     plt.gca().add_patch(venus_ball)

#     mars_ball = plt.Circle((mars.y[0][count], mars.y[1][count]), 5e6, color='red')
#     plt.gca().add_patch(mars_ball)

#     #current sail path
#     plt.plot(sail_in_x, sail_in_y, color="black") 
#     sail_ball = plt.Circle((sail_in_x[-1], sail_in_y[-1]), 5e6, color='black')
#     plt.gca().add_patch(sail_ball)

#     #sail future tracjectory with current angle
#     plt.plot(current_sail.y[0], current_sail.y[1], color="gray")
    
#     plt.draw()

#     prev_sail = current_sail
#     count += 1

# fig,ax=plt.subplots()
# fig.canvas.mpl_connect('key_press_event',keyclick)

# plt.show()
# plt.draw()
