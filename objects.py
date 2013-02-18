#Author:Chaitanya CH
#FileName: objects.py

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

from OpenGL.GL import *
from OpenGL.raw.GLUT import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import sqrt,arccos,arctan,absolute,array,float32,random
import OpenGL.arrays.vbo as glvbo
import numpy as np

class BaseObject(object):
	def __init__(self):
		"""
		Constructor of the base class. Usually, it should be called in
		the constructor of the inherited classes.
		"""
		self.rgb = np.array((1.0, 0.0, 0.0), dtype=float32)
		self.a = np.array((1.0), dtype=float32)
		self.name = None
		self.drawn_as = None
		self.color = None
		self.data = None
		self.start_pos = None
		self.end_pos = None
		self.dia = None
		self.subdivisions = 10

	def get_name(self):
		return self.name

	def get_drawn_as(self):
		return self.drawn_as

	def update_rbga(self, rgba):
		self.rgb = rgba[:3]
		self.a = rgba[3]
		self.color = rgba

	def update_rgb(self, rgb):
		self.rgb = rgb
		self.update_color()
		
	def update_a(self, a):
		self.a = a
		self.update_color()

	def update_color(self):
		self.color = np.hstack((self.rgb, self.a))

	def render(self):
		pass

class Point(BaseObject):
	"""
	Class that defines a point
	"""
	def __init__(self, name, position):
		"""
		Point constructor
		"""
		super(Point, self).__init__()
		self.name = name
		self.drawn_as = 'Point'
		self.data = np.array(position, dtype=np.float32)
		self.color = np.hstack((self.rgb, self.a))

class Line(BaseObject):
	"""
	Class that defines a compartment as a simple line.
	"""

	def __init__(self, name, start_pos, end_pos):
		"""
		Constructor. usecase: Line(name='Axon1',start_pos=[0.0,0.0,0.0], end_pos=[1.0,0.0,0.0])
		"""
		super(Line, self).__init__()
		self.name = name
		self.draw_as = 'Line'
		self.data = np.array((start_pos, end_pos), dtype=np.float32)
		self.color = np.hstack((self.rgb, self.a))
		self.color = np.vstack((self.color, self.color))

class Cylinder(BaseObject):
	"""
	Class that defines a compartment as a cylindrical shape. 
	"""
	def __init__(self, name, start_pos, end_pos, dia):
		"""
		Constructor.
		"""
		super(Cylinder, self).__init__()
		self.name = name
		self.draw_as = 'Cylinder'
		self.start_pos = np.array((start_pos), dtype=np.float32)
		self.end_pos = np.array((end_pos), dtype=np.float32)
		self.dia = dia
		self.data, self.index = self.generate_cylinder()
		self.color = np.zeros([len(self.data),4])
		for ii in range(len(self.data)):
			self.color[ii:] = np.array(np.hstack((self.rgb, self.a)), dtype=float32)

	def vertex(self, r, angle):
		'''angle in degrees'''
		x = r*np.cos(np.radians(angle))
		y = r*np.sin(np.radians(angle))
		return np.hstack((x,y))

	def generate_cylinder(self):
		r = self.dia / 2.0
		height = np.linalg.norm(self.start_pos - self.end_pos) #dist bet. points
		z_angle = np.arccos((self.end_pos[2] - self.start_pos[2]) / height)
		xy_plane_proj = np.linalg.norm(self.start_pos[:2] - self.end_pos[:2])
		if xy_plane_proj == 0:
			x_angle = 0.0
		else:
			x_angle = np.arccos((self.end_pos[0] - self.start_pos[0]) / xy_plane_proj)
		#print height,np.rad2deg(z_angle),np.rad2deg(x_angle)
		subdiv = self.subdivisions
		angle = 360.0 / subdiv
		points = [np.hstack((0.0,0.0,0.0)), np.hstack((0.0,0.0,height))]
		for ang_down in np.arange(0.0, 360.0, angle):
			ang_top = ang_down #convenience 
			points.append(np.hstack((self.vertex(r, ang_down), 0.0)))
			points.append(np.hstack((self.vertex(r, ang_top), height)))
			nump = np.array(np.vstack(points), dtype=np.float32)
		indx = []
		for ii in range(2, 22, 2):
			point_1 = ii
			point_2 = ii+1
			point_3 = ii+2
			point_4 = ii+3
			if ii == 20:
				point_3 = 2
				point_4 = 3
			indx.extend([point_1, point_2, point_3])
			indx.extend([point_2, point_3, point_4])
			indx.extend([point_1, 0, point_3])
			indx.extend([point_2, 1, point_4])
		indx = np.array(np.hstack(indx), dtype=np.ubyte)
		return nump, indx

		
class Sphere(BaseObject):
	"""
	Class that defines a compartment as a sphere.
	"""
	def __init__(self, name, centre_pos, dia=1.0):

		super(Sphere, self).__init__()
		self.name = name
		self.draw_as = 'Sphere'
		self.start_pos = centre_pos
		self.dia = dia
		self.radius = dia/2.0
#		self.data = self.generate_data()

	def generate_data(self):
		data = np.empty([np.square(self.subdivisions),3])
		angle = 360.0 / self.subdivisions
		ii = 0
	#	for ph in np.arange(-90.0, 90.0, angle):
#			for th in np.arange(0.0, 360.0, 2*angle):
#				data[ii] = self.get_vertex(
			
	def get_vertex(self, th2, ph2):
		x = np.sin(th2)*np.cos(ph2);
		y = np.cos(th2)*np.cos(ph2);
		z = np.sin(ph2);
		return x,y,z
		
class Disk(BaseObject):
	"""
	Class that defines a compartment as a Disk. 
	"""
	def __init__(self, name, centre_pos, dia=1.0):
		"""
		Disk constructor, usecase: Disk(name='Soma',centre_pos=[1.0,1.0,1.0], dia=1.0)
		"""
		super(Disk, self).__init__()
		self.name = name
		self.draw_as = 'Disk'
		self.start_pos = centre_pos
		self.dia = dia
		self.radius = dia/2.0

	def render(self):
		"""
		Renders the disk.
		"""
		glutInit(1,1)
		glPushMatrix()
		glColor(self.r, self.g, self.b, self.a)

		glTranslate(*self.start_pos[:3])		
		quadric = gluNewQuadric()
		gluDisk( quadric, 0.0, self.radius, self.subdivisions, 1)
		glTranslate(*[i*-1 for i in self.start_pos[:3]])
		glPopMatrix()




class Capsule(BaseObject):
	"""
	Class that defines a compartment as a cylindrical shape. 
	"""

	def __init__(self, name, start_pos, end_pos, dia):
		"""
		Constructor.
		"""
		super(Capsule, self).__init__()
		self.name = name
		self.draw_as = 'Capsule'
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.dia = dia

		x1,y1,z1 = self.start_pos[:3]
		x2,y2,z2 = self.end_pos[:3]
		self.radius = self.dia/2

		self.vx = x2-x1
		self.vy = y2-y1
		self.vz = z2-z1

			#float ax,rx,ry,rz;
		self.length = sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz)

	def render(self):
		"""
		Renders the compartment as a capsule.
		"""
		quadric = gluNewQuadric()
		glPushMatrix()

		glColor(self.r, self.g, self.b, self.a)

		glTranslatef(self.start_pos[0], self.start_pos[1], self.start_pos[2])
		if (absolute(self.vz) < 0.0001):
			glRotatef(90, 0,1,0)
			if self.vx == 0:
				if self.vy < 0:
					ax = 57.2957795
				else:
					ax = -57.2957795
			else:
				ax = 57.2957795*-arctan( self.vy / self.vx )
			if (self.vx < 0):
				ax = ax + 180
			rx = 1
			ry = 0
			rz = 0
		else:
			ax = 57.2957795*arccos( self.vz / self.length )
			if (self.vz < 0.0):
				ax = -ax
			rx = -self.vy*self.vz
			ry = self.vx*self.vz
			rz = 0
		#v = sqrt(self.vx*self.vx + self.vy*self.vy + self.vz*self.vz)

		glRotatef(ax, rx, ry, rz)
		gluQuadricOrientation(quadric,GLU_OUTSIDE)
		gluCylinder(quadric, self.radius, self.radius, self.length, self.subdivisions, 1)

		gluQuadricOrientation(quadric,GLU_OUTSIDE)
		gluSphere(quadric, self.radius, self.subdivisions, self.subdivisions)

		glTranslatef(0, 0, self.length)
		gluSphere(quadric, self.radius, self.subdivisions, self.subdivisions)

		glPopMatrix()
