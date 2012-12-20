from PyQt4 import QtCore, QtGui
from PyQGLViewer import *
from objects import *

from filehandler import FileHandler
from neuroey import Neuroey

class GLCanvas(QGLViewer):
    compartmentSelected = QtCore.pyqtSignal(QtCore.QString)
    def __init__(self,parent=None):
        QGLViewer.__init__(self,parent)
        self.setStateFileName('.MoogliState.xml')
        self.vizObjects = {}

    def init(self):
        self.restoreStateFromFile()
        self.setBackgroundColor(QtGui.QColor(255,255,255,255))
        self.setSceneRadius(10.0)

    def scatterObjects(self,namesList,xPosList,yPosList,zPosList=None,dia=1.0,drawAs='Point'):
        pass

    def drawObject(self,name,startPos,endPos,dia,drawAs):
        pass
    
    def drawObject1(self):
        self.vizObjects['Soma'] = Point()

    def readFile(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro' #do something here to canvas! 
            neuro = Neuroey()  #this should be init at canvas init, will give handle to draw directly
            return neuro.drawCells(f.cellDict)
        
    def draw(self):
#        print len(self.vizObjects)
        for obj in self.vizObjects.values():
            obj.render() 

