from subprocess import call
import sys


# As headless rendering is not supported and the visualisation window be iteratively opened
iteration = 1000
for i in range(iteration):
    print(i)
    call(["python", "open3D/PriorSimulation.py"])
