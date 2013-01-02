## Description: class NetworkML for loading NetworkML from file or xml element into MOOSE
## Version 1.0 by Aditya Gilra, NCBS, Bangalore, India, 2011 for serial MOOSE
## Version 1.5 by Niraj Dudani, NCBS, Bangalore, India, 2012, ported to parallel MOOSE
## Version 1.6 by Aditya Gilra, NCBS, Bangalore, India, 2012, further changes for parallel MOOSE

"""
NeuroML.py is the preferred interface. Use this only if NeuroML L1,L2,L3 files are misnamed/scattered.
Instantiate NetworlML class, and thence use method:
readNetworkMLFromFile(...) to load a standalone NetworkML file, OR
readNetworkML(...) to load from an xml.etree xml element (could be part of a larger NeuroML file).
"""

from xml.etree import cElementTree as ET
import string
import os
from math import cos, sin
from MorphML import MorphML
from neuroml_utils import meta_ns, nml_ns, find_first_file

class NetworkML():

    def __init__(self, nml_params,library={}):
        self.neuroml='http://morphml.org/neuroml/schema'
        self.bio='http://morphml.org/biophysics/schema'
        self.mml='http://morphml.org/morphml/schema'
        self.nml='http://morphml.org/networkml/schema'
        self.library = library
        self.cellDictBySegmentId={}
        self.cellDictByCableId={}
        self.nml_params = nml_params
        self.model_dir = nml_params['model_dir']

    def readNetworkMLFromFile(self,filename,cellSegmentDict={},params={}):
        """ 
        specify tweak params = {'excludePopulations':[popname1,...], 'excludeProjections':[projname1,...], \
            'onlyInclude':{'includePopulation':(popname,[id1,...]),'includeProjections':(projname1,...)} }
        If excludePopulations is present, then excludeProjections must also be present:
        Thus if you exclude some populations,
            ensure that you exclude projections that refer to those populations also!
        Though for onlyInclude, you may specify only included cells and this reader will
            also keep cells connected to those in onlyInclude.
        This reader first prunes the exclude-s,
            then keeps the onlyInclude-s and those that are connected.
        Use 'includeProjections' if you want to keep some projections not connected to
            the primary 'includePopulation' cells
        but connected to secondary cells that connected to the primary ones:
        e.g. baseline synapses on granule cells connected to 'includePopulation' mitrals;
            these synapses receive file based pre-synaptic events,
            not presynaptically connected to a cell.
        """
        print "reading file ... ", filename
        tree = ET.parse(filename)
        root_element = tree.getroot()
        try:
            return self.readNetworkML(root_element,cellSegmentDict,params,root_element.attrib['lengthUnits'])
        except:
            return self.readNetworkML(root_element,cellSegmentDict,params,root_element.attrib['length_units'])
    def readNetworkML(self,network,cellSegmentDict,params={},lengthUnits="micrometer"):
        """
        This returns populationDict = { 'populationname1':(cellname,{int(instanceid1):moosecell, ... }) , ... }
        and projectionDict = { 'projectionname1':(source,target,[(syn_name1,pre_seg_path,post_seg_path),...]) , ... }
        """
        if lengthUnits in ['micrometer','micron']:
            self.length_factor = 1e-6
        else:
            self.length_factor = 1.0
        self.network = network
        self.cellSegmentDict = cellSegmentDict
        self.params = params
        self.createPopulations() # create cells
        return self.populationDict

    def createPopulations(self):
        self.populationDict = {}
        for population in self.network.findall(".//{"+nml_ns+"}population"):
            cellname = population.attrib["cell_type"]
            populationname = population.attrib["name"]
            print "loading", populationname
            ## if cell does not exist in library load it from xml file
            if not self.library.has_key(cellname):
                mmlR = MorphML(self.nml_params)
                model_filenames = (cellname+'.xml', cellname+'.morph.xml')
                success = False
                for model_filename in model_filenames:
                    model_path = find_first_file(model_filename,self.model_dir)
                    if model_path is not None:
                        cellDict = mmlR.readMorphMLFromFile(model_path)
                        success = True
                        break
                if not success:
                    raise IOError(
                        'For cell {0}: files {1} not found under {2}.'.format(
                            cellname, model_filenames, self.model_dir
                        )
                    )
                self.cellSegmentDict.update(cellDict)
                self.library[cellname] = cellDict
            
            #self.populationDict[populationname] = (cellname,{})
            for instance in population.findall(".//{"+nml_ns+"}instance"):
                instanceid = instance.attrib['id']
                location = instance.find('./{'+nml_ns+'}location')
                rotationnote = instance.find('./{'+meta_ns+'}notes')
                if rotationnote is not None:
                    zrotation = float(string.split(rotationnote.text,'=')[1])
                else:
                    zrotation = 0
                
                x = float(location.attrib['x'])*self.length_factor
                y = float(location.attrib['y'])*self.length_factor
                z = float(location.attrib['z'])*self.length_factor
                self.populationDict.update(self.translate_rotate(populationname,instanceid,self.library[cellname],x,y,z,zrotation))
                
    def translate_rotate(self,populationname,instanceid,cellDict,x,y,z,ztheta): 
        newCellDict = {}
        for cmpt in cellDict:
            newCmptName = populationname+'/'+cmpt.split('/')[0]+'_'+str(instanceid)+'/'+cmpt.split('/')[1]
            x0 = cellDict[cmpt][0]
            y0 = cellDict[cmpt][1]
            x0new = x0*cos(ztheta)-y0*sin(ztheta)
            y0new = x0*sin(ztheta)+y0*cos(ztheta)
            newCellDict[newCmptName] = cellDict[cmpt]
            newCellDict[newCmptName][0] = x0new + x
            newCellDict[newCmptName][1] = y0new + y
            newCellDict[newCmptName][2] += z
            x1 = cellDict[cmpt][3]
            y1 = cellDict[cmpt][4]
            x1new = x1*cos(ztheta)-y1*sin(ztheta)
            y1new = x1*sin(ztheta)+y1*cos(ztheta)
            newCellDict[newCmptName][3] = x1new + x
            newCellDict[newCmptName][4] = y1new + y
            newCellDict[newCmptName][5] += z
        return newCellDict
