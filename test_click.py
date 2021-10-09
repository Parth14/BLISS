import matplotlib.pyplot as plt
x = [1];
y = [1];

def onclick(event):
    if event.button == 1:
         x.append(event.xdata)
         y.append(event.ydata)
    #clear frame
    plt.clf()
    plt.scatter(x,y); #inform matplotlib of the new data
    plt.draw() #redraw

fig,ax=plt.subplots()
ax.scatter(x,y)
fig.canvas.mpl_connect('button_press_event',onclick)
plt.show()
plt.draw()
