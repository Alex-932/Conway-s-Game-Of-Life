# -*- coding: utf-8 -*-
"""
The game of life
Created on Fri Mar  4 17:28:41 2022

@author: Alex
@Version : 1.0 (08/03/22)
"""
import numpy as np
from pylab import *
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

#We get the dimensions
Y = int(input("Dimension Y : "))
X = int(input("Dimension X : "))
Pourcentage = int(input("Pourcentage de cellules vivantes ? "))/100
Name = input("Nom du fichier de sortie (avec extension): ")
Limit = int(input("Nombre de cycle : "))

#We create the grid that will be the world of our game
the_world = np.random.choice([0, 1], size=[Y, X], p=[(1-Pourcentage), Pourcentage])

#List that will contain all state of the grid
film = [the_world]

#We initialize a figure
fig, ax = plt.subplots(figsize=(16, 16))
ax.imshow(the_world)
ax.set_axis_off()

#We get a list of the coordinates of the neighbor cells
def get_neighbors(y, x):
    global the_world
    neighbors = []
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if (i, j) != (y, x) :
                neighbors.append((i%the_world.shape[0], j%the_world.shape[1]))
    return int(sum([the_world[y,x] for y,x in neighbors]))
    
def update():
    global the_world, film
    future_world = the_world.copy()
    for x in range(the_world.shape[1]):
        for y in range(the_world.shape[0]):
            alive = get_neighbors(y, x)
            if the_world[y, x] == 0 and alive == 3 :
                future_world[y, x] = 1
            if the_world[y, x] == 1 and alive in [0,1,4,5,6,7,8] :
                future_world[y, x] = 0
    film.append(future_world)
    the_world = future_world.copy()
                    
def check_movement(cycle):
    global film, X, Y
    if len(film) >= 5 and cycle%5 == 0 :
        sets = film[-5:]
        if np.sum(sets[-1]==sets[-2]) == X*Y \
            or np.sum(sets[-1]==sets[-3]) == X*Y \
            or np.sum(sets[-1]==sets[-4]) == X*Y :
            return False
    return True
      
def life_cycle():
    global the_world 
    cycle = 0
    while np.sum(the_world) != 0 and cycle <= Limit and check_movement(cycle):
        update()
        cycle += 1
        print(cycle)
        
def aff_update(i):
    global film, ax
    print("Jour {}".format(i))
    im = film[i]
    ax.imshow(im)
    ax.set_title("Jour n°{}".format(i), fontsize=20)
    ax.set_axis_off()

life_cycle()
anim = FuncAnimation(fig, aff_update, frames=np.arange(0, len(film)), interval=50)
anim.save(Name, fps=30)#, codec=['-vcodec', 'libx264'])
#anim.save('The game of life.gif', dpi=80, writer='Pillow')
plt.close()
    
