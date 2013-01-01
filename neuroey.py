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

    def drawCompartment(self,name,start_pos,end_pos,dia,draw_as='Line'):
        if (start_pos != end_pos): #not a soma
            if draw_as == 'Disk':
                compartment = Disk(self,name,start_pos+end_pos/2,dia) #average of start and end lists.
            elif draw_as == 'Point':
                compartment = Point(self,name,start_pos+end_pos/2,dia)#average of start and end lists.
            elif draw_as == 'Line':
                compartment = Line(self,name,start_pos,end_pos,dia)
            elif draw_as == 'Cylinder':
                compartment = Cylinder(self,name,start_pos,end_pos,dia)
            elif draw_as == 'Capsule':
                compartment = Capsule(self,name,start_pos,end_pos,dia)
        else: #soma case
            if draw_as == 'Disk' :
                compartment = Disk(self,name,start_pos,dia)
            elif draw_as == 'Point':
                compartment = Point(self,name,start_pos,dia)
            else :
                compartment = Sphere(self,name,start_pos,dia)

#        try:
#            self.cellComptDict[cellName].append(compartment)
#        except KeyError:
#            self.cellComptDict[cellName] = [compartment]

        return compartment
