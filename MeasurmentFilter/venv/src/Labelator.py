import scipy.constants as constants
import matplotlib.pyplot as plt

class Labelator:
    dps = 0.061
    accuracy = 0.5 # in seconds
    def __init__(self, measure):
        self.time_measures = []
        self.x_measures = []
        self.z_measures = []
        self.y_measures = []
        self.file = open(measure.path_of_file, 'r')
        self.potholes = measure.poles
        self.time_of_measure = measure.time_of_measurment
        self.parse_file()


    def parse_file(self):
        lines = self.file.read().split('\n')
        lines[:] = (x for x in lines if x != '')

        for i in range(len(lines)):
            lines[i] = lines[i].split("\t\t")
            #Filter empty strings in list
            try:
                if self.time_of_measure >= float(lines[i][3]):
                    self.time_measures.append((float(lines[i][3])))
                    self.x_measures.append(int(lines[i][0]) * self.dps * constants.g * 3.6 / 1000)
                    self.y_measures.append(int(lines[i][1]) * self.dps / 1000)
                    self.z_measures.append(int(lines[i][2]) * self.dps / 1000)
                else:
                    break
            except ValueError:
                print("Blad w czasie")

            except IndexError:
                print("BLad")


    def add_potholes(self, num_od_measure, potholes):
         self.potholes[num_od_measure] = potholes


    def label(self):
        is_pothole = False
        labeled = []
        for time in self.time_measures:
            for pothole in self.potholes:
                if pothole - self.accuracy <= time <= pothole + self.accuracy:
                    is_pothole = True
                    break
                else:
                    is_pothole = False
            if is_pothole:
                 labeled.append(1)
            else:
                labeled.append(0)

        # plt.plot(self.time_measures, labeled)
        # plt.show()
        return labeled

