## Description: class NeuroML for loading NeuroML from single file into MOOSE
## Version 1.0 by Aditya Gilra, NCBS, Bangalore, India, 2011 for serial MOOSE
## Version 1.5 by Niraj Dudani, NCBS, Bangalore, India, 2012, ported to parallel MOOSE
## Version 1.6 by Aditya Gilra, NCBS, Bangalore, India, 2012, further changes for parallel MOOSE


from xml.etree import cElementTree as ET
from MorphML import MorphML
from NetworkML import NetworkML
import string
import sys
from os import path

class NeuroML():

    def __init__(self):
        pass

    def readNeuroMLFromFile(self,filename):
        """
        For the format of params required to tweak what cells are loaded,
         refer to the doc string of NetworkML.readNetworkMLFromFile().
        Returns (populationDict,projectionDict),
         see doc string of NetworkML.readNetworkML() for details.
        """
        print "Loading neuroml file ... ", filename

        neuroml_ns='http://morphml.org/neuroml/schema'
        
        tree = ET.parse(filename)
        root_element = tree.getroot()
        self.model_dir = path.dirname( path.abspath( filename ) )
        self.lengthUnits = root_element.attrib['lengthUnits']
        
        self.nml_params = {
                'model_dir':self.model_dir,
        }
        mmlR = MorphML(self.nml_params)
        self.cellsDict = {}
        for cells in root_element.findall('.//{'+neuroml_ns+'}cells'):
            for cell in cells.findall('.//{'+neuroml_ns+'}cell'):
                cellDict = mmlR.readMorphML(cell,params={},lengthUnits=self.lengthUnits)
                self.cellsDict.update(cellDict)

        #print "Loading individual cells into MOOSE root ... "
        nmlR = NetworkML(self.nml_params)
        return nmlR.readNetworkML(root_element,self.cellsDict,params=params,lengthUnits=self.lengthUnits)

def loadNeuroML_L123(filename):
    neuromlR = NeuroML()
    return neuromlR.readNeuroMLFromFile(filename)

if __name__ == "__main__":
    if len(sys.argv)<2:
        print "You need to specify the neuroml filename."
        sys.exit(1)
    loadNeuroML_L123(sys.argv[1])
