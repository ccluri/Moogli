from xml.etree import ElementTree as ET
from numpy import cos, sin
import string

from MorphML import *
import sys

class NetworkML():

    def __init__(self):
        self.neuroml='http://morphml.org/neuroml/schema'
        self.bio='http://morphml.org/biophysics/schema'
        self.mml='http://morphml.org/morphml/schema'
        self.nml='http://morphml.org/networkml/schema'
        
        self.cellDictBySegmentId={}
        self.cellDictByCableId={}
        #self.nml_params = nml_params

    def readNetworkMLFromFile(self,filename,params={}):
        print "reading file ... ", filename
        tree = ET.parse(filename)
        root_element = tree.getroot()
        return self.readNetworkML(root_element,params,root_element.attrib['lengthUnits'])

    def readNetworkML(self,network,cellDict,params={},lengthUnits="micrometer"):
        """
        This returns populationDict = { 'populationname1':(cellname,{instanceid1:moosecell, ... }) , ... }
        and projectionDict = { 'projectionname1':(source,target,[(syn_name1,pre_seg_path,post_seg_path),...]) , ... }
        """
        if lengthUnits in ['micrometer','micron']:
            self.length_factor = 1e-6
        else:
            self.length_factor = 1.0
        self.network = network

        self.params = params
        print "creating populations ... "
        self.createPopulations() # create cells
        return (self.populationDict)

    def createPopulations(self):
        self.populationDict = {}
        self.library = {}

        nml_ns='http://morphml.org/networkml/schema'
        meta_ns='http://morphml.org/metadata/schema'
        
        for population in self.network.findall(".//{"+nml_ns+"}population"):
            cellname = population.attrib["cell_type"]
            populationname = population.attrib["name"]
            print "loading", populationname
            ## if channel does not exist in library load it from xml file
            if not self.library.has_key(cellname):
                mmlR = MorphML()
                cellDict = mmlR.readMorphMLFromFile('/home/chaitu/buildQ/Demos/neuroml/CA1PyramidalCell/'+cellname+'.xml')
                #self.cellSegmentDict.update(cellDict)
                self.library[cellname] = cellDict
            #libcell = moose.Cell('/library/'+cellname)
            self.populationDict[populationname] = (cellname,{})

            for instance in population.findall(".//{"+nml_ns+"}instance"):
                instanceid = instance.attrib['id']
                location = instance.find('./{'+nml_ns+'}location')
                rotationnote = instance.find('./{'+meta_ns+'}notes')
                if rotationnote is not None:
                    ## the text in rotationnote is zrotation=xxxxxxx
                    zrotation = float(string.split(rotationnote.text,'=')[1])
                else:
                    zrotation = 0
                ## deep copies the library cell to an instance
                x = float(location.attrib['x'])*self.length_factor
                y = float(location.attrib['y'])*self.length_factor
                z = float(location.attrib['z'])*self.length_factor
                updatedCellDict = self.translate_rotate(cellDict,x,y,z,zrotation,populationname+'_'+str(instanceid))
                #self.populationDict[populationname+'_'+str(instanceid)] = updatedCellDict
                self.populationDict[populationname][1][int(instanceid)] = updatedCellDict
                
    def translate_rotate(self,cellDict,x,y,z,ztheta,newName): # recursively translate all compartments
        newCellDict = [] 
        for ii,cmpt in enumerate(cellDict):
            cmptNew = [] 
            cmptNew = [cmpt[0]+'_'+newName,cmpt[1],[]]

            x0 = cmpt[2][0]
            y0 = cmpt[2][1]
            x0new = x0*cos(ztheta)-y0*sin(ztheta)
            y0new = x0*sin(ztheta)+y0*cos(ztheta)

            cmptNew[2].append(x0new + x)
            cmptNew[2].append(y0new + y)
            cmptNew[2].append(cmpt[2][2] + z)

            x1 = cmpt[2][3]
            y1 = cmpt[2][4]
            x1new = x1*cos(ztheta)-y1*sin(ztheta)
            y1new = x1*sin(ztheta)+y1*cos(ztheta)
            cmptNew[2].append(x1new + x)
            cmptNew[2].append(y1new + y)
            cmptNew[2].append(cmpt[2][5] + z)

            cmptNew[2].append(cmpt[2][6])
            
            newCellDict.append(cmptNew)
        return newCellDict

