from canvas import

class Neuroey():
    def __init__():
        self.scale = 10e-6

    
    
    def read_file(self,filename):
        f = FileHandler(filename)
        if f.kind == 'neuroey':
            self.scale = 'micro'
            return f.parsed_list_dict



