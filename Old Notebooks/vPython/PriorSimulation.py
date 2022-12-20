from vpython import *
import numpy as np
import random

# wall: the assumed boundary of the view
wall_thickness = .1
wall_opacity = 0.5

# surface: simulated rectangle
surface_thickness = .1

num_surfaces = 500

smallest_surface = 0.2
largest_surface = 18

view_width = 300 
view_height = 25
human_height = 1.65

shortest_distance = 2.5
furtherest_distance = 300

# the x-coord, y-coord, distance of each simulated surface
# store 4 corners to locate each surface
surfaces_left_top = np.empty(shape=(3, num_surfaces))
surfaces_left_bottom = np.empty(shape=(3, num_surfaces))
surfaces_right_top = np.empty(shape=(3, num_surfaces))
surfaces_right_bottom = np.empty(shape=(3, num_surfaces))
surfaces = [] # store the surface objects to visualise in 3D

for i in range(num_surfaces):
    surface_size = random.uniform(smallest_surface, largest_surface)
    coord_x = random.uniform(-view_width/2, view_width/2)
    coord_y = random.uniform(-human_height, view_height - human_height) # CK: for Yang and Purves the camera is at a height of 1.65 m. I think we should put the camera at the origin (height 0) and adjust the simulation so that the "ground" is at -1.65 m
    distance = random.uniform(shortest_distance, furtherest_distance) 

    left_top_x = coord_x - surface_size/2
    left_top_y = coord_y + surface_size/2
    left_bottom_x = coord_x - surface_size/2
    left_bottom_y = coord_y - surface_size/2
    right_top_x = coord_x + surface_size/2
    right_top_y = coord_y + surface_size/2
    right_bottom_x = coord_x + surface_size/2
    right_bottom_y = coord_y - surface_size/2
    
    surfaces_left_top[0][i] = left_top_x
    surfaces_left_top[1][i] = left_top_y
    surfaces_left_top[2][i] = distance
    surfaces_left_bottom[0][i] = left_bottom_x
    surfaces_left_bottom[1][i] = left_bottom_y
    surfaces_left_bottom[2][i] = distance
    surfaces_right_top[0][i] = right_top_x
    surfaces_right_top[1][i] = right_top_y
    surfaces_right_top[2][i] = distance
    surfaces_right_bottom[0][i] = right_bottom_x
    surfaces_right_bottom[1][i] = right_bottom_y
    surfaces_right_bottom[2][i] = distance

    surfaces.append(box(pos=vector(coord_x, coord_y, distance), size=vector(surface_size, surface_size, surface_thickness), color=color.white))    


ground = box(pos=vector(0, -human_height, furtherest_distance/2), size=vector(view_width, wall_thickness, furtherest_distance), color=color.white)
leftwall = box(pos=vector(-view_width/2, 0, furtherest_distance/2), opacity=wall_opacity, size=vector(wall_thickness, view_height, furtherest_distance), color=color.white)
rightwall = box(pos=vector(view_width/2, 0, furtherest_distance/2), opacity=wall_opacity, size=vector(wall_thickness, view_height, furtherest_distance), color=color.white)
