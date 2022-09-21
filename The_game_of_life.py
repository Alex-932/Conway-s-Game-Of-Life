# -*- coding: utf-8 -*-
"""
Conway's game of life

@author: alex-merge
@version : 3.0
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
# import cv2 as cv

## Getting settings with parser
arg_parser = argparse.ArgumentParser(description='Set the game.')
arg_parser.add_argument(
    "--output",
    "-o",
    dest = "savepath",
    default = r"Output/",
    required = False,
    type = str,
    help = "Savepath as follow dir1/../dir3/. (Default is Output/)")
arg_parser.add_argument(
    "--size",
    "-s",
    dest = "size",
    default = (100, 100),
    nargs = "+",
    type = int,
    required = False,
    help = "Size of the world (X, Y). (Default is 100 100)")
arg_parser.add_argument(
    "--limit",
    "-l",
    dest = "limit",
    default = 100,
    type = int,
    required = False,
    help = "Maximum number of iterations. (Default is 100)")
arg_parser.add_argument(
    "--spf",
    "-spf",
    dest = "spf",
    default = 5,
    type = int,
    required = False,
    help = "Second per frame. (Default is 5)")
args = arg_parser.parse_args()


Name = args.savepath
if not os.path.isdir(Name):
    os.mkdir(Name)
Limit = args.limit
(X, Y) = tuple(args.size)
Scaling_factor = max(int(2000/Y), int(2000/X))

## Creating the numpy array
world = np.random.randint(2, size = (Y, X))
old_world = world.copy()
very_old_world = world.copy()

def cycle(world):
    """
    Simulate the next step of the simulation.

    """
    next_world = world.copy()
    for x in range(world.shape[1]):
        for y in range(world.shape[0]):
            arr = np.array([[world[i, k] for i in [(y-1)%Y, y, (y+1)%Y]] 
                            for k in [(x-1)%X, x, (x+1)%X]])
            alive_neighbors = sum(sum(arr))
            if alive_neighbors in [0,1,4,5,6,7,8] :
                next_world[y, x] = 0
            elif alive_neighbors == 3 :
                next_world[y, x] = 1
    return next_world

condition, t = True, 0
while condition and t <= Limit :
    plt.imsave(r"{0}img_{1}.jpg".format(Name, str(t)), 
               arr = np.kron(world, np.ones((Scaling_factor, Scaling_factor))), 
               dpi = 1000,
               cmap = "bone")
    
    next_world = cycle(world)
    
    if np.equal(world, next_world).all() or np.equal(old_world, next_world).all()\
        or np.equal(very_old_world, next_world).all():
        condition = False
    
    very_old_world = old_world.copy()
    old_world = world.copy()
    world = next_world.copy()
    
    t += 1
    print(t)

from PIL import Image

images = [Image.open("{0}img_{1}.jpg".format(Name, str(tp))) for tp in range(t)]

images[0].save(Name+'Animation.gif', save_all=True, append_images=images[1:], 
               duration=args.spf, loop=10)
