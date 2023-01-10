from vpython import *
import numpy as np
import random

# wall: the assumed boundary of the view
wall_thickness = .1
wall_opacity = 0.5

# surface: simulated rectangle
surface_thickness = .1

lighthouse_height = 30
human_height = 1.65

# This defines the distance between the location of view and the lighthouse
distance = 350  # CHANGE HERE

scene.camera.pos = vector(0, human_height, 0)

# ground = box(pos=vector(0, -human_height, 0), opacity=0.4, size=vector(50, wall_thickness, -1000), color=color.white)
lighthouse = cone(pos=vector(0, -human_height, distance),
                  axis=vector(0, lighthouse_height, 0), radius=5)
lightbeam = cylinder(pos=vector(0, lighthouse_height-human_height, distance),
                     color=color.white, axis=vector(0, 0, -10000), radius=0.4)

delta_angle = radians(0.1)
angle = radians(0)

while True:
    rate(80)
    angle = angle + delta_angle
    if angle > radians(15) or angle < radians(-15):
        delta_angle = delta_angle * (-1)
    print(angle)
    lightbeam.rotate(angle=delta_angle, axis=vector(0, 1, 0),
                     origin=vector(0, lighthouse_height-human_height, distance))
