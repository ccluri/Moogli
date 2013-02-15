import numpy as np

''' Handles everything that is to do with the input file.
    Called via canvas and returned to canvas for further action.
    Should return the kind of visualization "neuroey" or else.
    Should return the scale of the visualization um or what?
    Should return list of items comprehensible by canvas (via neuroey)
'''

class FileHandler():

    def __init__(self):
        self.filename = None
        self.filetype = None
        self.kind = None
        self.parsed_dict = {}

    def process_file(self, filename):
        self.filename, self.filetype = filename.rsplit('.',1) #what happens when path is passed?
        self.kind = 'neuroey' #all modules currently are neuroey
        return self.categorize(filename)
        
    def categorize(self, filename):
        if (self.filetype == 'xml') or (self.filetype =='nml'):
            from imports.NeuroML import NeuroML
            neuroml = NeuroML()#('model_dir':filename.rsplit('/',1)[0]}) 
            self.parsed_dict = neuroml.readNeuroMLFromFile(filename)

        elif (self.filetype == 'csv'):
            import csv
            f = open(filename, 'r')
            test_line = f.readline()
            dialect = csv.Sniffer().sniff(test_line) #to get the format of the csv
            f.close()
            f = open(filename, 'r')
            reader = csv.reader(f, dialect)
            for row in reader:
                self.parsed_dict[row[0]+'/'+row[1]] = [np.float32(i) for i in row[2:9]]
            f.close()
           
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
        else:
            print 'Not a supported Format yet*'
        return self.parsed_dict

if __name__ == '__main__':
    f = FileHandler()
    print f.process_file('./samples/purk2.morph.xml')
    
