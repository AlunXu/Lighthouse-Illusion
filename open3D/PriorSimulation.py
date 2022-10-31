import open3d as o3d
from matplotlib import pyplot as plt
import random
import numpy as np

# because headless rendering not supported
mesh = o3d.geometry.TriangleMesh.create_sphere()
mesh.compute_vertex_normals()
u = o3d.visualization.draw(
    mesh, raw_mode=False, non_blocking_and_return_uid=True)
# ---------------------------------------
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

surfaces = []  # store the surface objects to visualise in 3D

render = o3d.visualization.rendering.OffscreenRenderer(512, 512)
mat = o3d.visualization.rendering.MaterialRecord()
mat.shader = 'defaultLit'

for i in range(num_surfaces):
    surface_size = random.uniform(smallest_surface, largest_surface)

    coord_x = random.uniform(-view_width/2, view_width/2)
    # sample the mid-bottom point of the rectangle
    # CK: for Yang and Purves the camera is at a height of 1.65 m. I think we should put the camera at the origin (height 0) and adjust the simulation so that the "ground" is at -1.65 m
    coord_y = random.uniform(-human_height, view_height - human_height)

    distance = random.uniform(shortest_distance, furtherest_distance)

    # an average sized square that's sitting on the ground and as close as possible
    #surface_size = 9
    #coord_x = 0
    #coord_y = -human_height
    #distance = 2.5

    surface = o3d.geometry.TriangleMesh.create_box(
        width=surface_size, height=surface_size, depth=surface_thickness)
    surface.compute_vertex_normals()
    surface.translate([coord_x - surface_size/2, coord_y, distance])
    render.scene.add_geometry("surface"+str(i), surface, mat)
    surfaces.append(surface)

# projected simulation in 2D
width = 512
height = 512

# Camera Settings - CHANGE HERE
f = 256
f = 128
px = 256
py = 256

# intrinsic matrix
intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, f, f, px, py)

intrinsic.intrinsic_matrix = [[f, 0, px],
                              [0, f, py],
                              [0, 0,  1]]

cam = o3d.camera.PinholeCameraParameters()
cam.intrinsic = intrinsic

# extrinsic matrix
# need an extra row of (0,0,0,1),
# which allows us to further decompose this matrix into a rotation followed by translation
cam.extrinsic = np.array([[1., 0., 0., 0.],
                          [0., 1., 0., 0.],
                          [0., 0., 1., 0.],
                          [0., 0., 0., 1.]])

# setup_camera(intrinsics, extrinsic_matrix)
render.setup_camera(cam.intrinsic, cam.extrinsic)

cimg = render.render_to_image()
dimg = render.render_to_depth_image()

plt.subplot(1, 2, 1)
plt.imshow(cimg, origin = "lower")
plt.subplot(1, 2, 2)
plt.imshow(dimg, origin = "lower")
plt.show()

# simulation in 3D - it will take some time, uncomment it to see 3D simulation
# u = o3d.visualization.draw_geometries(surfaces)
