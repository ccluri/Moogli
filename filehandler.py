''' Handles everything that is to do with the input file.
    Called via canvas and returned to canvas for further action.
    Should return the kind of visualization "neuroey" or else.
    Should return the scale of the visualization um or what?
    Should return list of items comprehensible by canvas (via neuroey)
'''

class FileHandler():
    def __init__(self,filename):
        self.filename, self.fileType = filename.rsplit('.',1)
        self.categorize()
        
    def categorize(self):
        if (self.fileType == 'xml') or (self.fileType =='nml'):
            from imports.NeuroML import NeuroML #is this a good way?
            neuroml = NeuroML() 
            self.parsedList = neuroml.readNeuroMLFromFile(fileName)
    
        elif (self.fileType == 'csv'): #transpose the time representation!
            f = open(fileName,'r')
            testLine = f.readline()
            dialect = csv.Sniffer().sniff(testLine) #to get the format of the csv
            f.close()
            f = open(fileName, 'r')
            reader = csv.reader(f,dialect)
            for row in reader:
                self.parsedList.append([row[0],row[1],[float(i)*1e-6 for i in row[2:9]]])
                try:
                    dummy = row[9] #vm expect text
                    self.possibleData = True
                    self.generateDataFile(row)
                except IndexError:
                    pass
            f.close()
           
        elif (self.fileType == 'h5') or (self.fileType == 'hdf5'):
            self.fileType = 'h5'
            import h5py
            #raise exception if error
            self.dataFile = h5py.File(fileName)
            self.possibleData = True
            for name in self.dataFile.keys():
                if (name.find('.xml')!=-1) or (name.find('.nml')!=-1):
                    from imports.NeuroML import NeuroML
                    mml = NeuroML()
                    self.parsedList = mml.readNeuroMLFromString(str(self.dataFile[name].value[0]))
                elif (name.find('.csv') != -1):
                    f = open(fileName,'r')
                    testLine = f.readline()
                    dialect = csv.Sniffer().sniff(testLine) #to get the format of the csv
                    f.close()
                    f = open(fileName, 'r')
                    reader = csv.reader(f,dialect)
                    for row in reader:
                        self.parsedList.append([row[0],row[1],[float(i)*1e-6 for i in row[2:9]]])
                    f.close()
                
        else:
            print 'Not a supported Format yet*'


        return self.parsedList
