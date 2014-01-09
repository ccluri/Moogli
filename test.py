from moogli import Moogli
from filehandler import FileHandler
import numpy as np
import os
from PyQt4 import QtGui

class TestMoogli():
    def __init__(self, parent=None):
        self.mgl = Moogli()
        #self.test_point()
        #self.test_points() #
        #self.test_line()
        #self.test_lines() #
        #self.test_cylinder()
        #self.test_cylinders() #
        #self.test_sphere() 
        #self.test_spheres() #
        #self.test_cell_line()
        #self.test_cell_cylinder()
        #self.test_cell_lines() #
        #self.test_cell_cylinders() #

        # # marked are not in place yet

    def test_point(self):
        """If place_points in canvas is correct. 1000 random points are displayed in a unit cube, colored - red"""
        self.mgl.canvas.clear_all()
        points_pos = np.random.rand(1000,3)
        for ii,point_pos in enumerate(points_pos):
            self.mgl.canvas.place_point(str(ii), point_pos)
        self.mgl.show()
        self.assertTrue(self.ask_for_correctness("1000 points in red, inside unit sphere"))

    def test_line(self):
        """If place_lines in canvas is correct. a square at z=1 plane, colored red"""
        self.mgl.canvas.clear_all()
        self.mgl.canvas.place_line('line1',[1,1,1],[1,-1,1],[1,0,0,1])
        self.mgl.canvas.place_line('line2',[1,-1,1],[-1,-1,1],[1,0,0,1])
        self.mgl.canvas.place_line('line3',[-1,-1,1],[-1,1,1],[1,0,0,1])
        self.mgl.canvas.place_line('line4',[-1,1,1],[1,1,1],[1,0,0,1])
        self.mgl.show()
        self.assertTrue(self.ask_for_correctness("4 lines at z=1 plane, making a square, colored-red"))

    def test_cylinder(self):
        """If place_cylinders in canvas is correcnt. 4 cylinders, one on x,y and z, and another between 111 and 222, colored red"""
        self.mgl.canvas.clear_all()
        self.mgl.canvas.place_cylinder('Xaxis', [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], 1.0, [1.,0.,0.,1.])
        self.mgl.canvas.place_cylinder('X1axis', [1.0, 0.0, 0.0], [2.0, 0.0, 0.0], 0.5, [0.,1.,0.,1.])
        self.mgl.canvas.place_cylinder('Zaxis', [0.0, 0.0, 1.0], [0.0, 0.0, 4.0], 1.5, [0.,0.,1.,1.])
        self.mgl.canvas.place_cylinder('Yaxis', [0.0, 1.0, 0.0], [0.0, 2.0, 0.0], 0.7, [1.,0.,0.,1.])
        self.mgl.canvas.place_cylinder('freeBird', [1.0, 1.0, 1.0], [2.0, 2.0, 2.0], 1.0, [0.,1.,0.,1.])
        self.mgl.show()
        self.assertTrue(self.ask_for_correctness("4 cylinders, 3 on axis and 1 between 111 and 222"))

    def test_sphere(self):
        """if spheres are displayed correctly, one at 111 of unit radius"""
        self.mgl.canvas.clear_all()
        self.mgl.canvas.place_sphere('Z_axis', [1.0, 1.0, 1.0], 2.0)
        self.mgl.show()
        self.assertTrue(self.ask_for_correctness("A sphere (30 vertex polyhedra) at 111"))

    def test_cell_line(self):
        """if a mitral cell is displayed as lines"""
        self.mgl.canvas.clear_all()
        fh = FileHandler(os.path.abspath(os.path.join('.','samples','purk2.xml')))
        parsed_vals = fh.get_values()
        del fh
        for cmp_name,cmp_pos in parsed_vals.iteritems():
            self.mgl.canvas.place_line(cmp_name,
                                       [ii*1e3 for ii in cmp_pos[:3]],
                                       [ii*1e3 for ii in cmp_pos[3:6]],
                                       [1.0, 0.0, 0.0, 1.0])
        self.mgl.show()

    def test_cell_cylinder(self):
        """if a mitral cell is displayed as cylinders"""
        self.mgl.canvas.clear_all()
        fh = FileHandler(os.path.abspath(os.path.join('.','samples','purk2.xml')))
        parsed_vals = fh.get_values()
        del fh
        for cmp_name,cmp_pos in parsed_vals.iteritems():
            self.mgl.canvas.place_cylinder(cmp_name, 
                                           [ii*1e4 for ii in cmp_pos[:3]],
                                           [jj*1e4 for jj in cmp_pos[3:6]], 
                                           cmp_pos[6]*1e4, 
                                           [1.,0.,0.,1.])
        self.mgl.show()


    def ask_for_correctness(item_name):
        reply = QtGui.QMessageBox.question(self.mgl.window, 'Message', item_name, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            print 'Passed test', item_name
            return True
        else:
            print 'Failed test', item_name
            return False

if __name__ == '__main__':
    TestMoogli()
