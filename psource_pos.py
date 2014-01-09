from moogli import Moogli
import time
import numpy as np
import os
from PyQt4 import QtGui
import pickle

class show_points():
    def __init__(self, parent=None):
        self.mgl = Moogli()
        self.draw_line()
        #self.draw_slice()
        #self.draw_lines()
        #self.draw_points()
        #self.draw_point()

        #self.draw_cylinders()        
        #self.draw_cylinder()
        self.mgl.show()

    def draw_slice(self):
        self.mgl.canvas.place_line('line1',[1.5,5.0,15.0],[1.5,-5.0,15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line2',[1.5,-5.0,15.0],[-1.5,-5.0,15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line3',[-1.5,-5.0,15.0],[-1.5,5.0,15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line4',[-1.5,5.0,15.0],[1.5,5.0,15.0],[0,0,1,1])

        self.mgl.canvas.place_line('line5',[1.5,5.0,-15.0],[1.5,-5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line6',[1.5,-5.0,-15.0],[-1.5,-5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line7',[-1.5,-5.0,-15.0],[-1.5,5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line8',[-1.5,5.0,-15.0],[1.5,5.0,-15.0],[0,0,1,1])

        self.mgl.canvas.place_line('line9',[1.5,5.0,15.0],[1.5,5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line10',[1.5,-5.0,15.0],[1.5,-5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line11',[-1.5,-5.0,15.0],[-1.5,-5.0,-15.0],[0,0,1,1])
        self.mgl.canvas.place_line('line12',[-1.5,5.0,15.0],[-1.5,5.0,-15.0],[0,0,1,1])
        
        self.mgl.canvas.place_line('line23_4',[1.5,5.0,3.0],[1.5,-5.0,3.0],[0,1,0,1])
        self.mgl.canvas.place_line('line4_5',[1.5,5.0,0.0],[1.5,-5.0,0.0],[0,1,0,1])
        self.mgl.canvas.place_line('line5_6',[1.5,5.0,-5.0],[1.5,-5.0,-5.0],[0,1,0,1])

        self.mgl.canvas.place_line('line_cs',[1.5,4.0,15.0],[1.5,4.0,-15.0],[0,1,0,1])

    def draw_line(self):
        #f = open('olfactory_dict.pkl','r')
        #factor = 1e3
        f = open('point_pos_dict.pkl','r')
        factor = 1e-2
        pp = pickle.load(f)
        f.close()
        tic = time.clock()
        for ii, point_pos in pp.iteritems():
            self.mgl.canvas.place_line(str(ii), [kk*factor for kk in point_pos[:3]],[kk*factor for kk in point_pos[3:6]],[1.,0.,0.,1.0]) 
        toc = time.clock() - tic
        print toc

    def draw_lines(self):
        #f = open('olfactory_dict.pkl','r')
        #factor = 1e3
        f = open('point_pos_dict.pkl','r')
        factor = 1e-2
        pp = pickle.load(f)
        f.close()
        tic = time.clock()
        self.mgl.canvas.place_lines(pp, [1.,0.,0.,1.])
        toc = time.clock() - tic
        print toc

    def draw_cylinder(self):
        self.mgl.canvas.place_cylinder('freeBird', [1.0, 1.0, 1.0], [2.0, 2.0, 2.0], 1.0, [0.,1.,0.,1.])

    def draw_cylinders(self):
        #f = open('point_pos_dict.pkl','r')
        #factor = 1e-2
        f = open('olfactory_dict.pkl','r')
        factor = 1e3
        pp = pickle.load(f)
        f.close()
        tic = time.clock()
        self.mgl.canvas.place_cylinders(pp, [1.,0.,0.,1.])
        toc = time.clock() - tic
        print toc
        
    def draw_points(self):
        f = open('point_pos_dict.pkl','r')
        factor = 1e-2
        #f = open('olfactory_dict.pkl','r')
        #factor = 1e3
        pp = pickle.load(f)
        f.close()
        tic = time.clock()
        self.mgl.canvas.place_points(pp, [1,0,0,1], factor)
        toc = time.clock() - tic
        print toc

    def draw_point(self):
        f = open('point_pos_dict.pkl','r')
        factor = 1e-2
        #f = open('olfactory_dict.pkl','r')
        #factor = 1e3
        pp = pickle.load(f)
        f.close()
        tic = time.clock()
        for ii, point_pos in pp.iteritems():
            self.mgl.canvas.place_point(str(ii), [factor*kk for kk in point_pos[:3]],[1.,0.,0.,1.0])        
        toc = time.clock() - tic
        print toc


if __name__ == '__main__':
   show_points()
