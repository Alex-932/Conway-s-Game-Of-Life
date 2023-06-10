#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TGoL Go Fast edition

@author : alex-merge
@version : 0.1
"""

import numpy as np
from scipy.signal import convolve2d
import time
import matplotlib.pyplot as plt
from matplotlib import animation


world_shape = ((90, 160))

world_kernel = np.ones((3,3))
world_kernel[1,1] = 0

max_iter = 300
max_search_depth = 10000
upscaling_factor = 4
prob = .2
similarity_threshold = .999
matching_threshold = 8
search_best = False
mode = "gosper_gun"

## Patterns
unbounded = np.array(
    [[1, 1, 1, 0, 1],
     [1, 0, 0, 0, 0],
     [0, 0, 0, 1, 1],
     [0, 1, 1, 0, 1],
     [1, 0, 1, 0, 1]]
    )

gosper_gun = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

patterns = {
    "unbounded": unbounded,
    "gosper_gun": gosper_gun,
    "random": prob
    }

def year_zero(mode, shape):
    if mode == "random" :
        world = np.random.choice([0, 1], 
                                 size = shape, 
                                 p=[1-patterns[mode], patterns[mode]])
    else :
        world = np.zeros(shape)
        pattern_shape = patterns[mode].shape
        world[
            (shape[0]//2-pattern_shape[0]//2):(shape[0]//2-pattern_shape[0]//2+pattern_shape[0]),
            (shape[1]//2-pattern_shape[1]//2):(shape[1]//2-pattern_shape[1]//2+pattern_shape[1])
            ] = patterns[mode]
        
    return world

def simulation():
    
    
    kron_kernel = np.ones((upscaling_factor, upscaling_factor))
        
    world = year_zero(mode, world_shape)
    world_timelapse = [world]
    start_time = time.time()
        
    for i in range(max_iter):
        next_world = convolve2d(world, world_kernel, mode = 'same', boundary='wrap')
        next_world += 10*world
    
        world = np.where(
            (next_world == 13) | (next_world == 12) | (next_world == 3), 
            1, 
            0,
        )
        world_timelapse.append(world)
        
        if i%10 == 0 and i != 0:
            checks = np.array([np.mean(world == world_timelapse[k]) 
                               for k in range(-10, -1)])
            if np.any(checks == 1):
                print(f"Simulation stopped at the {i}th step with full matching")
                break
            elif np.sum(checks >= similarity_threshold) >= matching_threshold : 
                print(f"Simulation stopped at the {i}th step with high percentage matching")
                break
            
    
    end_time = time.time()
    dtime = end_time-start_time
    
    print(f"World timelapse took {dtime} s")

    start_time = time.time()
    world_timelapse = np.array(world_timelapse)
    
    return world_timelapse

def updatefig(i):
    print(f"\r{i} images done.", end ="")
    img.set_array(world_timelapse[i])
    return img

n = 0
for k in range(max_search_depth):
    world_timelapse = simulation()
    n = len(world_timelapse)
    
    if n >= max_iter or search_best == False:
        break

print(f"Number of frames : {n}")

## Creating the video
fig = plt.figure(figsize = (16, 9), dpi=160)
plt.axis('off')
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

img = plt.imshow(world_timelapse[0], cmap = 'bone', interpolation='nearest', animated=True, aspect='auto')

ani = animation.FuncAnimation(fig, updatefig, frames=world_timelapse.shape[0])
ani.save(f'TGoL_{mode}.mp4', writer="ffmpeg", fps=30)
