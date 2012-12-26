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

from filehandler import FileHandler
from neuroey import Neuroey

class GLCanvas(QGLViewer):

    def __init__(self, parent=None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.MoogliState.xml')
        self.viz_objects_dict = {}
        self.scale = 'micro'
        self.neuro = Neuroey()

    def init(self):
        self.restoreStateFromFile()
        self.setBackgroundColor(QtGui.QColor(255,255,255,255))
        self.setSceneRadius(10.0)

    def put_object(self,name,startPos,endPos,dia,drawAs):
        pass
    
    def drawObject1(self):
        self.viz_objects_dict['Soma'] = Point()

    def read_file(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro'
            print f.parsed_list_dict
            #self.neuro.drawCells(f.parsed_list_dict)
        
    def draw(self):
        for obj in self.viz_objects_dict.values():
            obj.render() 
