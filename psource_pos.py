from moogli import Moogli
import time
import numpy as np
import os
from PyQt4 import QtGui
import pickle

class show_points():
    def __init__(self, parent=None):
        self.mgl = Moogli()
        #self.draw_lines()
        #self.draw_points()
        #self.draw_slice()
        self.draw_cylinders()
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

    def draw_lines(self):
        f = open('olfactory_dict.pkl','r')
        #f = open('point_pos_dict.pkl','r')
        pp = pickle.load(f)
        f.close()
        self.mgl.canvas.clear_all()
        tic = time.clock()
        for ii, point_pos in pp.iteritems():
            #print point_pos[:3], point_pos[3:6]
            # if ii.find('2') == 0 or ii.find('3') == 0 or ii.find('4') == 0 or ii.find('9') == 0 or ii.find('10') == 0 or ii.find('11') == 0:
            #     self.mgl.canvas.place_line(str(ii),[1e-2*kk for kk in point_pos[:3]],[1e-2*kk for kk in point_pos[3:6]],[1.,0.,0.,1.0]) 
            # else:
            #     self.mgl.canvas.place_line(str(ii),[1e-2*kk for kk in point_pos[:3]],[1e-2*kk for kk in point_pos[3:6]],[0.,0.,1.,0.3]) 
            #self.mgl.canvas.place_line(str(ii), [1e-3*kk for kk in point_pos[:3]],[kk*1e-3 for kk in point_pos[3:6]],[1.,0.,0.,1.0]) 
            self.mgl.canvas.place_line(str(ii), [1e2*kk for kk in point_pos[:3]],[kk*1e2 for kk in point_pos[3:6]],[1.,0.,0.,1.0]) 
        toc = time.clock() - tic
        print toc

    def draw_cylinders(self):
        #f = open('point_pos_dict.pkl','r')
        f = open('olfactory_dict.pkl','r')
        pp = pickle.load(f)
        f.close()
        #self.mgl.canvas.initialize_numpy(len(pp), 'cylinders')
        self.mgl.canvas.clear_all()
        tic = time.clock()
        self.mgl.canvas.place_cylinders(pp, [1.,0.,0.,1.])
        #for ii, point_pos in pp.iteritems():
        #    self.mgl.canvas.place_cylinder(str(ii), [1e3*kk for kk in point_pos[:3]],[1e3*kk for kk in point_pos[3:6]],point_pos[6]*1e3,[1.,0.,0.,1.0])
        toc = time.clock() - tic
        print toc
            
        
    def draw_points(self):
        f = open('point_pos_dict.pkl','r')
        pp = pickle.load(f)
        f.close()
        self.mgl.canvas.clear_all()
        count = 0
        for ii, point_pos in pp.iteritems():
            self.mgl.canvas.place_point(str(ii), [1e-2*kk for kk in point_pos]) 
            #if ii.find('2_') == 0 or ii.find('0_') == 0 or ii.find('1_') == 0 or ii.find('3_') == 0 or ii.find('4_') == 0:
            #if ii.find('5_') == 0:
            #if ii.find('6_') == 0 or ii.find('7_') == 0:
            #if ii.find('proby1_nodes == 0:
            #if ii.find('9_') == 0 or ii.find('10_') == 0 or ii.find('11_') == 0:

            # if int(ii.split('/')[1]) <= 1000:
            #     if int(ii.split('/')[2]) == 1:
            #         count += 1
            #         self.mgl.canvas.place_point(str(ii), [1e-2*kk for kk in point_pos]) 
            #         print point_pos

        print count

if __name__ == '__main__':
   show_points()
