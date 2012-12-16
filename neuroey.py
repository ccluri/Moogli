from objects import *
class Neuroey():
    def __init__():
        pass

    def drawCells(self,parsedCellList):
        for cell in parsedCellList:
            self.drawCell(cell)

    def drawCell(self,compartmentList):
        for compartment in compartmentList:
            self.drawCompartment(compartment)

    def drawCompartment(self,name,startPos,endPos,dia,drawAs='Line'):
        if (startPos != endPos): #not a soma
            if drawAs == 'Disk':
                compartment = Disk(self,name,startPos+endPos/2,dia) #average of start and end lists.
            elif drawAs == 'Point':
                compartment = Point(self,name,startPos+endPos/2,dia)#average of start and end lists.
            elif drawAs == 'Line':
                compartment = Line(self,name,startPos,endPos,dia)
            elif drawAs == 'Cylinder':
                compartment = Cylinder(self,name,startPos,endPos,dia)
            elif drawAs == 'Capsule':
                compartment = Capsule(self,name,startPos,endPos,dia)
        else: #soma case
            if drawAs == 'Disk' :
                compartment = Disk(self,name,startPos,dia)
            elif drawAs == 'Point':
                compartment = Point(self,name,startPos,dia)
            else :
                compartment = Sphere(self,name,startPos,dia)

#        try:
#            self.cellComptDict[cellName].append(compartment)
#        except KeyError:
#            self.cellComptDict[cellName] = [compartment]

        return compartment
