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
import OpenGL.arrays.vbo as glvbo
from PyQGLViewer import *
from objects import *
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
        self.spheres_names = []
        self.points_count = 0
        self.lines_count = 0
        self.triangles_count = 0

        self.t_point = 0
        self.t_line = 0
        self.t_triangle = 0

        self.light2 = ManipulatedFrame()
        self.show_lights = False#True

    def init(self):
        #glDisable(GL_LIGHTING)
        self.setBackgroundColor(QtGui.QColor(204, 204, 204, 255))
        #self.setBackgroundColor(QtGui.QColor(255, 255, 255, 255))
        self.setSceneRadius(10.0)
        self.setAnimationPeriod(100)
        self.light_defaults()
        self.restoreStateFromFile()

    def place_sphere(self, name, start_pos, dia):
        objt = Sphere(name, centre_pos=np.array((start_pos), dtype=np.float32),
                      dia=dia)
        if not self.objt_dict.has_key(objt.name):
            self.objt_dict[objt.name] = objt
        else:
            print 'Sphere with name: ',objt.name,' already exists - use unique name'
            return
        try:
            existing_count = np.uint32(len(self.triangles_data))
        except AttributeError:
            pass
        try:
            self.triangles_data = np.vstack((self.triangles_data, np.float32(objt.data)))
            self.triangles_index = np.hstack((self.triangles_index, objt.index + existing_count))
            self.triangles_color = np.vstack((self.triangles_color, np.float32(objt.color)))
            self.spheres_names.append(objt.name)
        except AttributeError:
            self.triangles_data = np.array(objt.data, dtype=np.float32)
            self.triangles_index = np.array(objt.index, dtype=np.uint32)
            self.triangles_color = np.array(objt.color, dtype=np.float32)
            self.spheres_names = [objt.name]

    def place_cylinder(self, name, start_pos, end_pos, dia, color):
        objt = Cylinder(name,
                        start_pos=np.array((start_pos),dtype=np.float32), 
                        end_pos=np.array((end_pos), dtype=np.float32), 
                        dia=dia,
                        rgb=np.array((color[0],color[1],color[2]), dtype=np.float32),
                        alpha=np.array((color[3]), dtype=np.float32))
        if not self.objt_dict.has_key(objt.name):
            self.objt_dict[objt.name] = objt
        else:
            print 'Cylinder with name: ',objt.name,' already exists - use unique name'
            return
        try:
            existing_count = np.uint32(len(self.triangles_data))
        except AttributeError:
            pass
        try:
            self.triangles_data = np.vstack((self.triangles_data, np.float32(objt.data)))
            self.triangles_index = np.hstack((self.triangles_index, objt.index + existing_count))
            self.triangles_color = np.vstack((self.triangles_color, np.float32(objt.color)))
            self.cylinders_names.append(objt.name)
        except AttributeError:
            self.triangles_data = np.array(objt.data, dtype=np.float32)
            self.triangles_index = np.array(objt.index, dtype=np.uint32)
            self.triangles_color = np.array(objt.color, dtype=np.float32)
            self.cylinders_names = [objt.name]
        
    def place_line(self, name, start_pos, end_pos, color):
        objt = Line(name,
                    start_pos=np.array((start_pos), dtype=np.float32),
                    end_pos=np.array((end_pos), dtype=np.float32),
                    rgb=np.array((color[0], color[1], color[2]), dtype=np.float32),
                    alpha=np.array((color[3]), dtype=np.float32))
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
        objt = Point(name, position=np.array((start_pos), dtype=np.float32))
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
        if self.spheres_names:
            self.vbo_triangles_data = glvbo.VBO(self.triangles_data)
            self.vbo_triangles_index = glvbo.VBO(self.triangles_index, target=GL_ELEMENT_ARRAY_BUFFER)
            self.vbo_triangles_color = glvbo.VBO(self.triangles_color)
            self.triangles_count = len(self.triangles_index)

    def clear_all(self):
        self.objt_dict = {}
        self.points_names = []
        self.lines_names = []
        self.cylinders_names = []
        self.spheres_names = []
        self.points_count = 0
        self.lines_count = 0
        self.triangles_count = 0
        self.t_point = 0
        self.t_line = 0
        self.t_triangle = 0
        try:
            del self.vbo_points_data, self.vbo_points_color
        except AttributeError, NameError:
            pass
        try:
            del self.vbo_lines_data, self.vbo_lines_color
        except AttributeError, NameError:
            pass
        try:
            del self.vbo_triangles_data, self.vbo_triangles_index, self.vbo_triangles_color
        except AttributeError, NameError:
            pass

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
                self.triangles_color[cyl_index:cyl_index+22] = colors[ii]
                self.t_triangle = 1
            elif objt in self.spheres_names:
                sph_index = self.spheres_names.index(objt)
                self.triangles_color[sph_index:sph_index+30] = colors[ii]
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
                self.triangles_color[cyl_index:cyl_index+22] = colors[ii]
                self.t_triangle = 1
        except:
            print objt, 'is not a cylinder on canvas'

    def update_spheres_colors(self, objts, colors):
        try:
            for ii,objt in enumerate(objts):
                sph_index = self.spheres_names.index(objt)
                self.triangles_color[sph_index:sph_index+30] = colors[ii]
                self.t_triangle = 1
        except:
            print objt, 'is not a sphere on canvas'

    def animate(self):
        self.update_colors(['Z_axis'],[np.float32(np.random.rand(4))])
        if self.t_point:
            self.vbo_points_color.set_array(self.points_color)
        if self.t_line:
            self.vbo_lines_color.set_array(self.lines_color)
        if self.t_triangle:
            self.vbo_triangles_color.set_array(self.triangles_color)
        self.t_point, self.t_line, self.t_triangle = 0, 0, 0

    def light_defaults(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Light0 is the default ambient light
        glEnable(GL_LIGHT0)
        # Light1 is a spot light
        # glEnable(GL_LIGHT1)
        # light_ambient  = [0.8, 0.2, 0.2, 1.0]
        # light_diffuse  = [1.0, 0.4, 0.4, 1.0]
        # light_specular = [1.0, 0.0, 0.0, 1.0]
        
        # glLightf(GL_LIGHT1, GL_SPOT_EXPONENT,  3.0)
        # glLightf( GL_LIGHT1, GL_SPOT_CUTOFF,    20.0)
        # glLightf( GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.5)
        # glLightf( GL_LIGHT1, GL_LINEAR_ATTENUATION, 1.0)
        # glLightf( GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 1.5)
        # glLightfv( GL_LIGHT1, GL_AMBIENT,  light_ambient)
        # glLightfv( GL_LIGHT1, GL_SPECULAR, light_specular)
        # glLightfv( GL_LIGHT1, GL_DIFFUSE,  light_diffuse)

        # Light2 is a classical directionnal light
        glEnable(GL_LIGHT2)
        light_ambient2  = [0.2, 0.2, 2.0, 1.0]
        light_diffuse2  = [0.8, 0.8, 1.0, 1.0]
        light_specular2 = [0.0, 0.0, 1.0, 1.0]
        glLightfv(GL_LIGHT2, GL_AMBIENT,  light_ambient2)
        glLightfv(GL_LIGHT2, GL_SPECULAR, light_specular2)
        glLightfv(GL_LIGHT2, GL_DIFFUSE,  light_diffuse2)
        self.setMouseTracking(True)
        
        #self.light1.setPosition(0.5, 0.5, 0)
        # Align z axis with -position direction : look at scene center
        #self.light1.setOrientation(Quaternion(Vec(0,0,1), -self.light1.position()))
        self.light2.setPosition(-0.5, 0.5, 0)

    def pre_draw_lights(self):
        pos = [1.0, 0.5, 0.0, 0.0]
        # Directionnal light
        glLightfv(GL_LIGHT0, GL_POSITION, pos)
        pos[3] = 1.0
        # # Spot light
        # pos2 = list(self.light1.getPosition()) + [1]
        # glLightfv(GL_LIGHT1, GL_POSITION, pos2)
        # v = self.light1.getInverseTransformOf((0,0,1))
        # glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, v)
        # Point light
        pos3 = list(self.light2.getPosition())
        pos3.append(1.0)
        glLightfv(GL_LIGHT2, GL_POSITION, pos3)


    def post_draw_lights(self):
        if self.show_lights:
            self.drawLight(GL_LIGHT0)
            #if self.light1.grabsMouse() :
            #    self.drawLight(GL_LIGHT1, 1.2)
            #else:
            #    self.drawLight(GL_LIGHT1)
            if self.light2.grabsMouse():
                self.drawLight(GL_LIGHT2, 1.2)
            else:
                self.drawLight(GL_LIGHT2)

    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        handled = False
        if ((e.key()==QtCore.Qt.Key_L) and (modifiers==QtCore.Qt.NoModifier)):
            self.show_lights = not self.show_lights
            self.updateGL()
        if not handled:
            QGLViewer.keyPressEvent(self,e)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.pre_draw_lights()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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
            glLineWidth(2.0)
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
            glDrawElements(GL_TRIANGLES, self.triangles_count, GL_UNSIGNED_INT, self.vbo_triangles_index)
            self.vbo_triangles_data.unbind()
            self.vbo_triangles_index.unbind()
            self.vbo_triangles_color.unbind()
        self.post_draw_lights()
        glDisable(GL_BLEND)
        #Ref. http://pyopengl.sourceforge.net/context/tutorials/shader_2.xhtml
