#Author:Chaitanya CH
#FileName: canvas.py

#This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.

from PyQt4 import QtCore, QtGui
from PyQGLViewer import *
from objects import *
import OpenGL.arrays.vbo as glvbo
import numpy as np
from filehandler import FileHandler
#from neuroey import Neuroey

class GLCanvas(QGLViewer):

    def __init__(self, parent=None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.MoogliState.xml')
        self.scale = 'micro'
        #self.neuro = Neuroey()
        
        #self.points_data = np.array((0, 0, 0, 0, 0, 0, 0), dtype=np.float32)
        self.lines_data = np.array((), dtype=np.float32)
        self.triangles_data = np.array((), dtype=np.float32)

    def init(self):
        self.restoreStateFromFile()
        self.setBackgroundColor(QtGui.QColor(255, 255, 255, 255))
        self.setSceneRadius(10.0)

    def place_object(self, name, start_pos, dia=1.0, draw_as='Point'):
        if draw_as == 'Point':
            #cmpt = Point(name, position=(np.array(start_pos, dtype=float32)+np.array(end_pos,dtype=float32))/2, dia)
            cmpt = Point(name, position=np.array((start_pos), dtype=float32)/100.0, dia=dia)
            try:
                self.points_data = np.vstack((self.points_data, cmpt.data))
            except AttributeError:
                self.points_data = np.array((cmpt.data))
        #print self.points_data[:,:3]
    
    def refresh_canvas(self):
        self.vbo_points = glvbo.VBO(self.points_data)

        self.points_count = self.points_data.shape[0]
        print self.points_count, 'Points'
        self.lines_count = self.lines_data.shape[0]
        self.triangles_count = self.triangles_data.shape[0]

    def read_file(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro'
            return f.parsed_list_dict
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.vbo_points.bind()
	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_COLOR_ARRAY)
	glVertexPointer(3, GL_FLOAT, 28, self.vbo_points)
	glColorPointer(4, GL_FLOAT, 28, self.vbo_points+12)
	glDrawArrays(GL_POINTS, 0, self.points_count)
        self.vbo_points.unbind()
        #this is not even the best method out there, see http://pyopengl.sourceforge.net/context/tutorials/shader_2.xhtml
