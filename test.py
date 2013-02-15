from moogli import Moogli
from filehandler import FileHandler
import pickle as pkl

def main(filename):
    #f = open(filename, 'r')
    #point_pos_dict = pkl.load(f)
    #f.close()

    f = FileHandler()
    point_pos_dict = f.process_file('./samples/purk2.morph.xml')

    window = Moogli()
    for name,locations in point_pos_dict.iteritems():
        #window.canvas.place_point(name, locations)
        window.canvas.place_line(name, locations[:3],locations[3:6])
    #window.canvas.place_line('lest', start_pos=[0.0, 0.0, 0.0], end_pos=[100.0, 100.0, 100.0])
    window.show()

main('pointPosDict.pkl')
