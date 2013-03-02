from moogli import Moogli
from filehandler import FileHandler
import pickle as pkl
import time
import numpy as np
def main(filename):
    #f = open(filename, 'r')
    #point_pos_dict = pkl.load(f)
    #f.close()

    #f = FileHandler('./samples/purk2.morph.xml')
#    point_pos_dict = f.process_file('./samples/purk2.morph.xml')
#    ii = 0
    mgl = Moogli()
#    for name,locations in point_pos_dict.iteritems():
#        if locations[:3] != locations[3:6]:
#            ii += 1
#            mgl.canvas.place_cylinder(name, locations[:3], locations[3:6], locations[6])

#    print ii
#        mgl.canvas.place_point(name, locations)
#        mgl.canvas.place_line(name, locations[:3],locations[3:6])


    # mgl.canvas.place_cylinder('Z_axis', start_pos=[0.0, 0.0, 3.0], end_pos=[0.0, 0.0, 4.0], dia=1.0)
    # mgl.canvas.place_cylinder('Y_axis', start_pos=[0.0, 1.0, 0.0], end_pos=[0.0, 2.0, 0.0], dia=1.0)
    # mgl.canvas.place_cylinder('X_axis', start_pos=[0.0, 0.0, 0.0], end_pos=[1.0, 0.0, 0.0], dia=1.0)
    # mgl.canvas.place_cylinder('JLTln', start_pos=[1.0, 1.0, 1.0], end_pos=[2.0, 2.0, 2.0], dia=1.0)

    mgl.canvas.place_sphere('Z_axis', start_pos=[1.0, 1.0, 3.0], dia=1.0)

    mgl.show()

main('pointPosDict.pkl')
