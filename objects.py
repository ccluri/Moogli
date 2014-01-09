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
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import sqrt,arccos,arctan,absolute,array,float32,random
from numpy import radians,sin,cos,dot
from collections import deque
import OpenGL.arrays.vbo as glvbo
import numpy as np
#from itertools import izip,starmap
#from operator import mul

#sphere_30 = np.load('sphere30.npz')

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
	def __init__(self, name, position, rgb, alpha):
		"""
		Point constructor
		"""
		super(Point, self).__init__()
		self.name = name
		self.rgb = rgb
		self.a = alpha
		self.drawn_as = 'Point'
		self.data = np.array(position, dtype=np.float32)
		self.color = np.hstack((self.rgb, self.a))

class Line(BaseObject):
	"""
	Class that defines a compartment as a simple line.
	"""

	def __init__(self, name, start_pos, end_pos, rgb, alpha):
		"""
		Constructor. usecase: Line(name='Axon1',start_pos=[0.0,0.0,0.0], end_pos=[1.0,0.0,0.0])
		"""
		super(Line, self).__init__()
		self.name = name
		self.draw_as = 'Line'
		self.data = np.array((start_pos, end_pos), dtype=np.float32)
		self.rgb = rgb
		self.a = alpha
		self.color = np.zeros([2, 4], dtype=np.float32)
		self.color[:, :3] = self.rgb
		self.color[:, 3] = self.a

class Cylinder(BaseObject):
	"""
	Class that defines a compartment as a cylindrical shape.
	"""
	def __init__(self, name, start_pos, end_pos, dia, rgb, alpha):
		"""
		Constructor.
		"""
		super(Cylinder, self).__init__()
		self.name = name
		self.draw_as = 'Cylinder'
		self.rgb = rgb
		self.a = alpha
		self.start_pos = np.array((start_pos), dtype=np.float32)
		self.end_pos = np.array((end_pos), dtype=np.float32)
		self.dia = dia
		self.data = self.generate_cylinder()
		self.color = np.zeros([22, 4])
		self.color[:, :3] = self.rgb
		self.color[:, 3] = self.a

	def vertex(self, r, angle):
		'''angle in degrees'''
		x = r*cos(radians(angle))
		y = r*sin(radians(angle))
		return np.array((x,y))

	def dot(self,U,V):
		return dot(U,V) #ordered according to effeciency - this may depend on if or not numpy array used.
		#return (U[0]*V[0])+(U[1]*V[1])+(U[2]*V[2])		
		#return reduce(lambda sum, p: sum + p[0]*p[1], zip(U,V), 0)#takes too long!
		#return sum(starmap(mul,izip(U,V)))

	def generate_cylinder(self):
		r = self.dia / 2.0
		P1 = self.start_pos
		P2 = self.end_pos
		L = P2 - P1 #vector in dir of cylinder
		N = L / sqrt(self.dot(L, L.conj()))
		#N = L / np.sqrt(self.dot(L, L.conj()))
		#Eq of plane
		#L[0](x)+L[1](y)+L[2](z) = L[0]*P1[0]+L[1]*P1[1]+L[2]*P1[2]
		#A pt on plane above
		dum_num = [1.00001, 2.80] #np.random.rand(2,1)
		if L[0] != 0.0: #if the x intersect is non zero.
 			P = np.array(((self.dot(L,P1) -L[1]*dum_num[0] -L[2]*dum_num[1]) / L[0], dum_num[0], dum_num[1]), dtype=np.float32)
		elif L[1] != 0.0:
			P = np.array((dum_num[0], (self.dot(L,P1) -L[0]*dum_num[0] -L[2]*dum_num[1]) / L[1], dum_num[1]), dtype=np.float32)
		elif L[2] != 0.0:
			P = np.array((dum_num[0], dum_num[1], (self.dot(L,P1) -L[0]*dum_num[0] -L[1]*dum_num[1]) / L[2]), dtype=np.float32)
		else:
			print 'Cannot draw a zero length cylinder'
		P1P = P1 - P
		U = P1P / sqrt(self.dot(P1P, P1P.conj()))
		V = np.array(((U[1]*N[2])-(N[1]*U[2]),(U[2]*N[0])-(N[2]*U[0]),(U[0]*N[1])-(N[0]*U[1])),dtype=np.float32)
		V = V / sqrt(self.dot(V, V.conj()))
		subdiv = 10 # self.subdivisions
		angle = 36.0 #360.0 / subdiv
		#data_array = [] #
		data_array = deque() #more effecient that lists
		data_array.append(P1)
		data_array.append(P2)
		for angle_down in xrange(0, 360, 36):
		#for angle_down in np.arange(0.0, 360.0, angle):
			ang_down = radians(angle_down)
			bot_pt = P1 + r*sin(ang_down)*U + r*cos(ang_down)*V #numpy array!
			data_array.append(bot_pt)
			data_array.append(bot_pt + L)
		data_array_np = np.array((data_array), dtype=np.float32)
		return data_array_np

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
		self.data = np.array((self.radius*sphere_30['points'] + self.start_pos), dtype=np.float32)
		self.index = sphere_30['indx']
		self.color = np.zeros([len(self.data),4])
		for ii in range(len(self.data)):
			self.color[ii:] = np.array(np.hstack((self.rgb, self.a)), dtype=float32)


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
