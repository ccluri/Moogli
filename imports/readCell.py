class readCell():
    def __init__(self):
        self.numCompartments = 0
        self.cell = 0
        self.currCell = 0
        self.lastCmpt = 0
        self.protoCmpt = 0
        self.graftFlag = 0
        self.polarFlag = 0
        self.relativeCoordsFlag = 0
        self.doubleEndPointFlag = 0

    def readCellFromFile(self,filename):
        f = open(filename,'r')
        
        lines = f.readlines()
        self.innerRead(lines)

    def innerRead(self,allLines):
        commentMode = 0
        for line in allLines:
            if line != '\n':
                line = line.strip().expandtabs()
                line = line.rsplit('//')[0]
                if commentMode:
                    if line.find('*/') != -1:
                        line = line.lstrip('*/')
                        commentMode = 0
                    else:
                        line = ''
                if line.find('/*') != -1:
                    if line.find('*/') != -1:
                        line = line.rsplit('/*')[0]+' '+line.split('*/')[1]
                        commentMode = 0
                    else:
                        line = ''
                        commentMode = 1
            if line.strip() != '':
                if line[0] == '*':
                    self.readScript(line)
                #else:
                #    self.readData(line)


    def readScript(self,line):
        if line == '*cartesian':
            self.polarFlag = 0
        if line == '*polar':
            self.polarFlag = 1
        if line == '*relative':
            self.relativeCoordsFlag = 1
        if line == '*absolute':
            self.relativeCoordsFlag = 0
        if line == '*double_endpoint':
            self.doubleEndPointFlag = 1
        if line == '*double_endpoint_off':
            self.doubleEndPointFlag = 0

        linePara = line.split(' ')

        if linePara[0] == '*start_cell':
            if len(linePara) == 1:
                self.graftFlag = 0
                self.currCell = self.cell
            elif len(linePara) == 2:
                self.graftFlag = 1
                self.currCell = self.startGraftCell(linePara[1])
            else:
                print 'Bad line'


        if linePara[0] == '*compt':
            if len(linePara) != 2:
                print 'Bad line'
            

def main():
    a = readCell()
    a.readCellFromFile('/home/chaitu/moose/GuiOG/Moogli/imports/ca1_v16.p')
main()
