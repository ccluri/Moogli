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
        self.objt_dict = {}
        self.points_names = []
        self.lines_names = []
        self.cylinders_names = []

        self.points_count = 0
        self.lines_count = 0
        self.triangles_count = 0

        self.t_point = 0
        self.t_line = 0
        self.t_triangle = 0
        
    def init(self):
        self.restoreStateFromFile()
        #glDisable(GL_LIGHTING)
        self.setBackgroundColor(QtGui.QColor(255, 255, 255, 255))
        self.setSceneRadius(10.0)
        self.setAnimationPeriod(100)

    def place_cylinder(self, name, start_pos, end_pos, dia):
        objt = Cylinder(name, start_pos=np.array((start_pos), dtype=np.float32),
                    end_pos=np.array((end_pos), dtype=np.float32), dia=dia)
        if not self.objt_dict.has_key(objt.name):
            self.objt_dict[objt.name] = objt
        else:
            print 'Cylinder with name: ',objt.name,' already exists - use unique name'
            return
        try:
            self.triangles_data = np.vstack((self.triangles_data, objt.data))
            self.triangles_index = np.hstack((self.triangles_index, objt.index+len(self.triangles_index)))
            self.triangles_color = np.vstack((self.triangles_color, objt.color))
            self.cylinders_names.append(objt.name)
        except AttributeError:
            self.triangles_data = np.array(objt.data, dtype=np.float32)
            self.triangles_index = np.array(objt.index, dtype=np.ubyte)
            self.triangles_color = np.array(objt.color, dtype=np.float32)
            self.cylinders_names = [objt.name]

    def place_line(self, name, start_pos, end_pos):
        objt = Line(name, start_pos=np.array((start_pos), dtype=np.float32)*1e4,
                    end_pos=np.array((end_pos), dtype=np.float32)*1e4)
        if not self.objt_dict.has_key(objt.name):
            self.objt_dict[objt.name] = objt
        else:
            print 'Point with name: ',objt.name,' already exists - use unique name'
            return
        try:
            self.lines_data = np.vstack((self.lines_data, objt.data))
            self.lines_color = np.vstack((self.lines_color, objt.color))
            self.lines_names.append(objt.name)
        except AttributeError:
            self.lines_data = np.array((objt.data))
            self.lines_color = np.array((objt.color))
            self.lines_names = [objt.name]

    def place_point(self, name, start_pos):
        objt = Point(name, position=np.array((start_pos), dtype=np.float32)/1000.0)
        if not self.objt_dict.has_key(objt.name):
            self.objt_dict[objt.name] = objt
        else:
            print 'Point with name: ',objt.name,' already exists - use unique name'
            return
        try:
            self.points_data = np.vstack((self.points_data, objt.data))
            self.points_color = np.vstack((self.points_color, objt.color))
            self.points_names.append(objt.name)
        except AttributeError:
            self.points_data = np.array((objt.data))
            self.points_color = np.array((objt.color))
            self.points_names = [objt.name]

    def create_object_buffers(self):
        if self.points_names:
            self.vbo_points_data = glvbo.VBO(self.points_data)
            self.vbo_points_color = glvbo.VBO(self.points_color)
            self.points_count = self.points_data.shape[0]
        if self.lines_names:
            self.vbo_lines_data = glvbo.VBO(self.lines_data)
            self.vbo_lines_color = glvbo.VBO(self.lines_color)
            self.lines_count = self.lines_data.shape[0]
        if self.cylinders_names:
            self.vbo_triangles_data = glvbo.VBO(self.triangles_data)
            self.vbo_triangles_index = glvbo.VBO(self.triangles_index, target=GL_ELEMENT_ARRAY_BUFFER)
            self.vbo_triangles_color = glvbo.VBO(self.triangles_color)
            self.triangles_count = len(self.triangles_index)
        #print self.triangles_count, ' numer of triangles indices'
        #print len(self.triangles_data), 'number of vertices'
        #print self.triangles_color
    def read_file(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro'
            return f.parsed_list_dict

    def update_colors(self, objts, colors):
        for ii,objt in enumerate(objts):
            if objt in self.points_names:
                self.points_color[self.points_names.index(objt)] = colors[ii]
                self.t_point = 1
            elif objt in self.lines_names:
                line_index = self.lines_names.index(objt)
                self.lines_color[lines_index:lines_index+2] = colors[ii]
                self.t_line = 1
            elif objt in self.cylinders_names:
                cyl_index = self.cylinders_names.index(objt)
                self.triangles_color[cyl_index:cyl_index+23] = colors[ii]
                self.t_triangle = 1
            else:
                print objt, 'is not on canvas - cannot update its newcolor'

    def update_points_colors(self, objts, colors):
        try:
            for ii,objt in enumerate(objts):
                self.points_color[self.points_names.index(objt)] = colors[ii]
                self.t_point = 1
        except ValueError:
            print objt, 'is not a point on canvas'
            
    def update_lines_colors(self, objts, colors):
        try:
            for ii,objt in enumerate(objts):
                line_index = self.lines_names.index(objt)
                self.lines_color[lines_index:lines_index+2] = colors[ii]
                self.t_line = 1
        except ValueError:
            print objt, 'is not a line on canvas'
            
    def update_cylinders_colors(self, objts, colors):
        try:
            for ii,objt in enumerate(objts):
                cyl_index = self.cylinders_names.index(objt)
                self.triangles_color[cyl_index:cyl_index+23] = colors[ii]
                self.t_triangle = 1
        except:
            print objt, 'is not a cylinder on canvas'

    def animate(self):
        self.update_colors(['lest'],[np.float32(np.random.rand(4))])
        if self.t_point:
            self.vbo_points_color.set_array(self.points_color)
        if self.t_line:
            self.vbo_lines_color.set_array(self.lines_color)
        if self.t_triangle:
            self.vbo_triangles_color.set_array(self.triangles_color)
        self.t_point, self.t_line, self.t_triangle = 0, 0, 0

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
#        glEnable(GL_BLEND)
#        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self.points_count:
            self.vbo_points_data.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self.vbo_points_data)
            self.vbo_points_color.bind()
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4, GL_FLOAT, 0, self.vbo_points_color)
            glPointSize(2.0)
            glDrawArrays(GL_POINTS, 0, self.points_count)
            self.vbo_points_data.unbind()
            self.vbo_points_color.unbind()
        if self.lines_count:
            self.vbo_lines_data.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self.vbo_lines_data)
            self.vbo_lines_color.bind()
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4, GL_FLOAT, 0, self.vbo_lines_color)
            glDrawArrays(GL_LINES, 0, self.lines_count)
            self.vbo_lines_data.unbind()
            self.vbo_lines_color.unbind()
        if self.triangles_count:
            self.vbo_triangles_data.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self.vbo_triangles_data)
            self.vbo_triangles_color.bind()
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4, GL_FLOAT, 0, self.vbo_triangles_color)
            self.vbo_triangles_index.bind()
            glDrawElements(GL_TRIANGLES, self.triangles_count, GL_UNSIGNED_BYTE, self.vbo_triangles_index)
            self.vbo_triangles_data.unbind()
            self.vbo_triangles_index.unbind()
            self.vbo_triangles_color.unbind()
#        glDisable(GL_BLEND)
        #this is not even the best method out there, see http://pyopengl.sourceforge.net/context/tutorials/shader_2.xhtml
