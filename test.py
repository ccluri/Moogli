from moogli import Moogli
import pickle as pkl

def main(filename):
    f = open(filename, 'r')
    point_pos_dict = pkl.load(f)
    f.close()

    window = Moogli()
    for name in point_pos_dict:
        window.canvas.place_point(name, point_pos_dict[name])
    window.canvas.place_line('lest', start_pos=[0.0, 0.0, 0.0], end_pos=[100.0, 100.0, 100.0])
    window.show()

main('pointPosDict.pkl')
