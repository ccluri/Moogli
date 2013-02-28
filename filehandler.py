import numpy as np

''' Handles everything that is to do with the input file.
    get_values returns a dict of values
    Contains the scale of the visualization.
    Should return list of items comprehensible by canvas (via neuroey)
'''

class FileHandler():

    def __init__(self, filepath):
        self.filepath = filepath
        #self.filename = filepath.rsplit('.',1)[0]
        self.filetype = filepath.rsplit('.',1)[1]
        self.categorize()

    def categorize(self):
        '''categorize based on self.filetype'''
        self.kind = 'neuroey' #all are neuroey at present
        self.scale = 'micro' #for neuroey - default
        
    def get_values(self):
        if (self.filetype == 'xml') or (self.filetype =='nml'):
            from imports.NeuroML import NeuroML
            neuroml = NeuroML()
            parsed_dict = neuroml.readNeuroMLFromFile(self.filepath)
        elif (self.filetype == 'csv'):
            import csv
            print "In CSV format,all values are assumed to be in micro mts"
            f = open(self.filepath, 'r')
            test_line = f.readline()
            dialect = csv.Sniffer().sniff(test_line) #to get the format of the csv
            f.close()
            f = open(self.filepath, 'r')
            reader = csv.reader(f, dialect)
            for row in reader:
                parsed_dict[row[0]+'/'+row[1]] = [np.float32(i) for i in row[2:9]]
            f.close()
        else:
            print 'Not a supported Format yet*'
            parsed_dict = {}

        return parsed_dict
        # elif (self.filetype == 'h5') or (self.filetype == 'hdf5'):
        #     self.filetype = 'h5'
        #     try: 
        #         import h5py
        #     except ImportError:
        #         print 'No HDF5. Install python-h5py to correct'
        #         pass
        #     self.dataFile = h5py.File(fileName)
        #     self.possibleData = True
        #     for name in self.dataFile.keys():
        #         if (name.find('.xml')!=-1) or (name.find('.nml')!=-1):
        #             from imports.NeuroML import NeuroML
        #             mml = NeuroML()
        #             self.parsedList = mml.readNeuroMLFromString(str(self.dataFile[name].value[0]))
        #         elif (name.find('.csv') != -1):
        #             f = open(fileName,'r')
        #             testLine = f.readline()
        #             dialect = csv.Sniffer().sniff(testLine) #to get the format of the csv
        #             f.close()
        #             f = open(fileName, 'r')
        #             reader = csv.reader(f,dialect)
        #             for row in reader:
        #                 self.parsedList.append([row[0],row[1],[float(i)*1e-6 for i in row[2:9]]])
        #             f.close()

if __name__ == '__main__':
    f = FileHandler('./samples/purk2.morph.xml')
    print f.get_values()
    
