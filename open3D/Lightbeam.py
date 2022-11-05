import open3d as o3d
from matplotlib import pyplot as plt
import random
import numpy as np
import sys
from os import path
from vpython import *
import math


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


# because headless rendering not supported
mesh = o3d.geometry.TriangleMesh.create_sphere()
mesh.compute_vertex_normals()
u = o3d.visualization.draw(
    mesh, raw_mode=False, non_blocking_and_return_uid=True)

lighthouse_height = 30
human_height = 1.65

# This defines the distance between the location of view and the lighthouse
distance = 0  # CHANGE HERE

render = o3d.visualization.rendering.OffscreenRenderer(512, 512)
mat = o3d.visualization.rendering.MaterialRecord()
mat.shader = 'defaultLit'

axis = [0, 1, 0]
theta = radians(20)

length = 2000

# Before Rotation
lightbeam_initial = o3d.geometry.TriangleMesh.create_cylinder(
    radius=1, height=length)  # height is the length of the cylinder
lightbeam_initial.compute_vertex_normals()
lightbeam_initial.translate(
    [0, lighthouse_height-human_height, length/2-distance])
lightbeam_initial.rotate(rotation_matrix(axis, theta), center=np.array(
    [0, lighthouse_height-human_height, -distance]))
render.scene.add_geometry("lightbeam_initial", lightbeam_initial, mat)
u = o3d.visualization.draw(
    lightbeam_initial)

# After Rotation
end_theta = radians(-40)
lightbeam_end = lightbeam_initial.rotate(rotation_matrix(axis, end_theta), np.array(
    [0, lighthouse_height-human_height, -distance]))
render.scene.add_geometry("lightbeam_end", lightbeam_end, mat)

# As location signal
# surface = o3d.geometry.TriangleMesh.create_box(
#     width=3, height=3, depth=3)
# surface.compute_vertex_normals()
# surface.translate([0, 20, distance])
# render.scene.add_geometry("surface", surface, mat)


# projected simulation in 2D
width = 512
height = 512

# Camera Settings - CHANGE HERE
f = 16
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
dimg = render.render_to_depth_image(z_in_view_space=True)

filename = 'ThreeCases/lightbeam'
file_index = distance

np.save(filename + '_depth_'+str(file_index), dimg)
np.save(filename + '_loc_'+str(file_index), cimg)

# filename = 'Snapshots-' + str(f)
# file_index = random.randint(1, 1000000)
# while path.exists(filename + '/depth_'+str(file_index)):
#     file_index = random.randint(1, 1000000)

# np.save(filename + '/depth_'+str(file_index), dimg)

plt.subplot(1, 2, 1)
# plt.imshow(cimg)
plt.imshow(cimg, origin="lower")
plt.subplot(1, 2, 2)
# plt.imshow(dimg)
plt.imshow(dimg, origin="lower")
plt.savefig(filename + "_full_"+str(file_index))
plt.show()


# For Animation
# frequency = 0
# angle = radians(20)
# angle = 0
# delta_theta = -radians(0.5)


# while True:
#     # frequency = 80
#     rate(80)
#     frequency += 1
#     angle = angle + delta_theta
#     print(angle)
#     if angle > radians(15) or angle < radians(-15):
#         delta_theta = delta_theta * (-1)
#     # if angle < radians(-20):
#     #     break
#     lightbeam_initial.rotate(rotation_matrix(axis, delta_theta), np.array(
#         [0, lighthouse_height-human_height, -length+distance]))
