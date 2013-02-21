from moogli import Moogli
from filehandler import FileHandler
import pickle as pkl
import time
import numpy as np
def main(filename):
    #f = open(filename, 'r')
    #point_pos_dict = pkl.load(f)
    #f.close()

    f = FileHandler()
#    point_pos_dict = f.process_file('./samples/purk2.morph.xml')
#    ii = 0
    window = Moogli()
#    for name,locations in point_pos_dict.iteritems():
#        if locations[:3] != locations[3:6]:
#            ii += 1
#            window.canvas.place_cylinder(name, locations[:3], locations[3:6], locations[6])

#    print ii
#        window.canvas.place_point(name, locations)
#        window.canvas.place_line(name, locations[:3],locations[3:6])


    window.canvas.place_cylinder('Z_axis', start_pos=[0.0, 0.0, 3.0], end_pos=[0.0, 0.0, 4.0], dia=1.0)
    window.canvas.place_cylinder('Y_axis', start_pos=[0.0, 1.0, 0.0], end_pos=[0.0, 2.0, 0.0], dia=1.0)
    window.canvas.place_cylinder('X_axis', start_pos=[0.0, 0.0, 0.0], end_pos=[1.0, 0.0, 0.0], dia=1.0)
    window.canvas.place_cylinder('JLTln', start_pos=[1.0, 1.0, 1.0], end_pos=[2.0, 2.0, 2.0], dia=1.0)

    window.show()

main('pointPosDict.pkl')
