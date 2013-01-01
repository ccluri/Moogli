from moogli import Moogli
import pickle as pkl

def main(filename):
    f = open(filename, 'r')
    point_pos_dict = pkl.load(f)
    f.close()

    window = Moogli()
    for name in point_pos_dict:
        window.canvas.place_object(name, point_pos_dict[name])

    window.show()

main('pointPosDict.pkl')
