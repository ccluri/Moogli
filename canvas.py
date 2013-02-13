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
        self.points_dict = {}

    def init(self):
        self.restoreStateFromFile()
        self.setBackgroundColor(QtGui.QColor(255, 255, 255, 255))
        self.setSceneRadius(10.0)
        self.setAnimationPeriod(100)

    def place_point(self, name, start_pos, dia=1.0):
        #cmpt = Point(name, position=(np.array(start_pos, dtype=float32)+np.array(end_pos,dtype=float32))/2, dia)
        cmpt = Point(name, position=np.array((start_pos), dtype=float32)/1000.0)
        if not self.points_dict.has_key(cmpt.name):
            self.points_dict[cmpt.name] = cmpt
        else:
            print 'Point with name: ',cmpt.name,' already exists - use unique name'
            return
        try:
            self.points_data = np.vstack((self.points_data, cmpt.data))
            self.points_color = np.vstack((self.points_color, cmpt.color))
            self.points_names.append(cmpt.name)
        except AttributeError:
            self.points_data = np.array((cmpt.data))
            self.points_color = np.array((cmpt.color))
            self.points_names = [cmpt.name]

    def create_object_buffers(self):
        self.vbo_points_data = glvbo.VBO(self.points_data)
        self.vbo_points_color = glvbo.VBO(self.points_color) 
        self.points_count = self.points_data.shape[0]

    def read_file(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro'
            return f.parsed_list_dict

    def animate(self):
        self.points_color = np.random.rand(369, 4)
        self.vbo_points_color.set_array(self.points_color)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.vbo_points_data.bind()
	glEnableClientState(GL_VERTEX_ARRAY)
	glVertexPointer(3, GL_FLOAT, 0, self.vbo_points_data)
        self.vbo_points_color.bind()
	glEnableClientState(GL_COLOR_ARRAY)
	glColorPointer(4, GL_FLOAT, 0, self.vbo_points_color)
        glPointSize(2.0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glDrawArrays(GL_POINTS, 0, self.points_count)
        glDisable(GL_BLEND)
        self.vbo_points_data.unbind()
        self.vbo_points_color.unbind()
        #this is not even the best method out there, see http://pyopengl.sourceforge.net/context/tutorials/shader_2.xhtml
