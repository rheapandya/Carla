import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import numpy as np
import cv2

actor_list = []
# logic and action creation
try:
    # connect to server
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    # get world
    world = client.get_world()

    # access blueprints
    blueprint_library = world.get_blueprint_library()
    
    # gets car
    bp = blueprint_library.filter('model3')[0]
    
    # get spawn points and spawn car
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp,spawn_point)

    # control car
    vehicle.apply_control(carla.VehicleControl(throttle = 1.0, steer = 0.0))

    # add car to list of actors being tracked then cleaned up
    actor_list.append(vehicle)

    # sleep for 5 seconds then finish
    time.sleep(45)

# cleaning things up
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("done.")