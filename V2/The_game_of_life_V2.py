# -*- coding: utf-8 -*-
"""
Conway's game of life
Created on Fri Mar  4 17:28:41 2022

@author: Alex-932
@Version : 2.0 (20/03/22)
"""
import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
import os
import cv2 as cv

##Idée optimisation : ne pas calculer dans les zones où il n'y a pas de 
##mouvement

#We get the dimensions and general information
Y = int(input("Y dimension (cell) : "))
X = int(input("X dimension (cell) : "))
Percentage = int(input("Living cell starting percentage ? "))/100
Name = input("Name of the output file (without extension): ")
Limit = int(input("Maximum cycle number : "))

#We create the grid that will be the world of our game
the_world = Grid(X, Y, value=[1,0], dist="random", rep=Percentage)

fig, ax = plt.subplots(figsize=(16, 16))

the_world.compute_neighbors(length=1)

def cycle():
    """
    Simulate the next step of the simulation.

    Returns
    -------
    None.

    """
    global the_world
    the_world.save()
    list_kill = []
    list_born = []
    for (x, y) in the_world.coord:
        neighbors_alive = sum(the_world.get_neighbors_values(x, y))
        cell_state = the_world.get_value(x, y)
        if cell_state and neighbors_alive in [0,1,4,5,6,7,8] :
            list_kill.append((x, y))
        if not cell_state and neighbors_alive == 3 :
            list_born.append((x, y))
    the_world.set_value(list_kill, 0)
    the_world.set_value(list_born, 1)
    
def check_movement(turn):
    """
    Compare the 3 last array of the simulation to check if there is still
    movements. The check happens every 50 cycle.
    
    Parameters
    ----------
    turn : Int
        The simulation cycle.

    Returns
    -------
    bool
        Return if there is movement or not.

    """
    global the_world, X, Y
    #Check only if there is more than 0 cycle and every 50 cycles.
    if not turn%50 and turn > 0 :
        #Get the 3 last arrays
        check_list = the_world.saved[-3:]
        check_order = [(0,1),(1,2),(0,2)]
        for (i,j) in check_order :
            if np.sum(check_list[i] == check_list[j]) == X*Y :
                return False
    return True
            
        
def images_saver(factor=9):
    """
    Save every array of the simulation (1 per cycle) as an jpg image.

    Parameters
    ----------
    factor : Int, optional
        Upscaling factor. The default is 9.

    Returns
    -------
    None.

    """
    global Name
    #We make sure to create the folder to save the images.
    if not os.path.exists(Name): 
        os.makedirs(Name)
    for k in range(len(the_world.saved)):
        upscaled = Grid.upscale(the_world.saved[k], factor)
        #Due to the listdir method, we add 10000 to the image index in order
        #not to mess up the classification.
        plt.imsave(Name+'/'+Name+'_'+str(10000+k)+'.jpg',\
                   upscaled, dpi=800, cmap="bone")

def film_saver():
    """
    Generate a .avi video using the images created using the images_saver. 
    method.
    
    Slightly modified from the code available at :
    https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    
    Returns
    -------
    None.

    """
    global Name
    img_array = []
    #We import all the images into a list : img_array.
    file_list = os.listdir(Name)
    file_list.sort()
    for filename in file_list:
        img = cv.imread(Name+'/'+filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv.VideoWriter(Name+'.avi',cv.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()    

def life_cycle():
    """
    Main function which run the simulation.

    Returns
    -------
    None.

    """
    global the_world 
    turn = 0
    #Conditions (in appearing order) :
        #There are alive cells.
        #The cycle limit is not exceeded.
        #The check_movement function did detect movement between cycles.
            #i.e. The simulation is not on a stagnating state.
    while np.sum(the_world) != 0 and turn <= Limit and check_movement(turn) :
        cycle()
        turn += 1
        #print(turn)

life_cycle()
images_saver()
film_saver()

