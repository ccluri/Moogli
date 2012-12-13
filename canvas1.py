from PyQt4 import QtCore, QtGui
from PyQGLViewer import *
from objects import *

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

    def scatter(self,xPosList,yPosList,zPosList,namesList,drawAs='points'):
        pass

    def drawObject(self,name,startPos,endPos,dia,drawAs):
        pass
    
    def drawObject1(self):
        self.vizObjects['Soma'] = Cylinder('Soma',[0.0,0.0,0.0],[1.0,1.0,1.0],1.0)

    def drawNewCompartment(self,cellName,name,coords,style=3,cellCentre=[0.0,0.0,0.0],cellAngle=[0.0,0.0,0.0,0.0]):
        ''' name = 'segmentName',cellName= 'mitral', coords = [x0,y0,z0,x,y,z,d] , style = 1/2/3/4'''
        if (coords[0]!=coords[3] or coords[1]!=coords[4] or coords[2]!=coords[5]): #not a soma
            if style == 1 : #disk
                compartment = somaDisk(self,name,cellName,coords,cellCentre,cellAngle)
            elif style == 2: #line
                compartment = cLine(self,name,cellName,coords,cellCentre,cellAngle)
            elif style == 3: #cylinder
                compartment = cCylinder(self,name,cellName,coords,cellCentre,cellAngle)
            elif style == 4: #capsule
                compartment = cCapsule(self,name,cellName,coords,cellCentre,cellAngle)
        else: #soma case
            if style == 1 : #disk
                compartment = somaDisk(self,name,cellName,coords,cellCentre,cellAngle)
            else: #sphere
                compartment = somaSphere(self,name,cellName,coords,cellCentre,cellAngle)

#        self.vizObjects[cellName+'/'+name] = compartment #add cmpt to sceneobjects
        try:
            self.cellComptDict[cellName].append(compartment)
        except KeyError:
            self.cellComptDict[cellName] = [compartment]

        return compartment

    def draw(self):
#        print len(self.vizObjects)
        for obj in self.vizObjects.values():
            obj.render() 

