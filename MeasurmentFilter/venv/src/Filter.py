import numbers
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

#http://newline.nadav.org/

#Liczenie G
#http://ozzmaker.com/accelerometer-to-g/

dps = 0.245

class Filtr:

    def __init__(self, path):
        self.file_path = path
        self.file = open(self.file_path, 'r')
        self.x_measures = []
        self.y_measures = []
        self.z_measures = []
        self.time_measures = []
        self.fs = 1 / 0.003103825
        self.filterOrder = 5  # Order of Buttewroth filter.
        self.cutoff = 3.667  # desired cutoff frequency of the filter, Hz

        self.__parse_file()
        self.filter_data()

    def filter_data(self):
        self.x_measures = self.__butter_lowpass_filter(self.x_measures)
        self.y_measures = self.__butter_lowpass_filter(self.y_measures)
        self.z_measures = self.__butter_lowpass_filter(self.z_measures)

    def plot_result(self, string):
        if 'x' in string:
            plt.subplot(3, 1, 1)
            plt.plot(self.time_measures, self.x_measures)
            plt.ylabel('Filtered X')
        if 'y' in string:
            plt.subplot(3, 1, 2)
            plt.plot(self.time_measures, self.y_measures)
            plt.ylabel('Filtered Y')
        if 'z' in string:
            plt.subplot(3, 1, 3)
            plt.plot(filter.time_measures, filter.z_measures)
            plt.ylabel('Filtered Z')
        plt.show()

    def __butter_lowpass(self):
        nyq = 0.5 * self.fs
        normal_cutoff =  self.cutoff / nyq
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        return b, a

    def __butter_lowpass_filter(self, data):
        b, a = self.__butter_lowpass()
        y = lfilter(b, a, data)
        return y

    def __parse_file(self):
        lines = self.file.read().split('\n')

        lines[:] = (x for x in lines if x != '')

        for i in range(len(lines)):
            lines[i] = lines[i].split("\t\t")

            #Filter empty strings in list
            if i % 2 == 1:
                try:
                    self.time_measures.append((int(lines[i][3])) / 1000000000)
                    self.x_measures.append(int(lines[i][0]) * dps / 1000)
                    self.y_measures.append(int(lines[i][1]) * dps / 1000)
                    self.z_measures.append(int(lines[i][2]) * dps / 1000)
                except ValueError:
                    print("Blad w czasie")

if __name__ == "__main__":
    filter = Filtr("C:/Projekty/PolesDetection/PolesDetection/RaspberryPi_drivers/bin/measurment.txt")
    filter.plot_result('z')
