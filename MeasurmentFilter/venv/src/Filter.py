import numbers
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
from datetime import datetime, timedelta
import statistics
import matplotlib.dates as dates
from datetime import datetime
import numpy as np
import math
from scipy.integrate import cumtrapz
import scipy.constants as constants
from Labelator import Labelator

#http://newline.nadav.org/

#Liczenie G
#http://ozzmaker.com/accelerometer-to-g/

class Filtr(Labelator):
    def __init__(self, measurment):
        self.time_measures = []
        self.x_measures = []
        self.z_measures = []
        self.y_measures = []
        self.file = open(measurment.path_of_file, 'r')
        self.not_filtr_z = []
        self.velocity = []
        self.fs = 1 / 0.0032
        self.filterOrder = 5  # Order of Buttewroth filter.
        self.cutoff = 15 # desired cutoff frequency of the filter, Hz
        self.time_between_samples = 0.0032 #in seconds
        self.x_treshold = 0.1
        self.time_of_measure = measurment.time_of_measurment
        self.parse_file()
        self.filter_data()

    def filter_data(self):
        self.not_filtr_z = self.z_measures
        self.z_measures = self.__butter_lowpass_filter(self.z_measures)
        self.cutoff = 10
       # self.x_measures = self.__butter_lowpass_filter(self.x_measures)

        self.calculate_velocity()

    def get_x_measures(self, t, y):
        return self.x_measures

    def calculate_velocity(self):
        self.velocity = cumtrapz(self.x_measures, self.time_measures, initial=0)

    def plot_result(self, string):
        _, treshold, moments_of_poles = self.find_poles()

        if 'x' in string:
            plt.figure(1)
            # plt.subplot(3, 1, 1)
            plt.plot(self.time_measures, self.x_measures)
            # plt.gcf().autofmt_xdate()
            plt.ylabel('Not filtered X')

        if 'y' in string:
            plt.figure(2)
            # plt.subplot(3, 1, 2)
            plt.plot(self.time_measures, self.y_measures)
            # plt.gcf().autofmt_xdate()
            plt.ylabel('Filtered Y')
        if 'z' in string:
            plt.figure(5)
            plt.plot(self.time_measures, self.not_filtr_z)
            plt.ylabel('Not filtered Z')
            plt.figure(3)
            # plt.subplot(3, 1, 2)
            plt.plot(self.time_measures, self.z_measures)
            plt.axhline(y=treshold, color='r', linestyle='-')
            plt.axhline(y=-treshold, color='r', linestyle='-')
            # plt.gcf().autofmt_xdate()
            plt.ylabel('Filtered Z')

            plt.figure(4)
            # plt.subplot(3, 1, 3)
            plt.plot(self.time_measures[:len(moments_of_poles)], moments_of_poles)
            plt.ylabel('Poles')
            # plt.gcf().autofmt_xdate()

        if 'v' in string:
            plt.figure(5)
            # plt.subplot(3, 1, 2)
            plt.plot(self.time_measures[:len(self.velocity)], self.velocity)
            # plt.gcf().autofmt_xdate()
            plt.ylabel('Velocity')

            plt.ylabel('Poles')
        plt.show()

    def find_poles(self):
        std_dev = statistics.stdev(self.z_measures)
        m = 2.0
        poles_loc = set()
        moments_of_poles = []   # 1-> there is pole, 0-> there is not
        treshold = m * std_dev
        time_window_size = 10
        found = 0

        for i in range(len(self.time_measures) - time_window_size):
            for j in range(time_window_size):
                if self.z_measures[i+j] > treshold:
                    found += 1
            if found == time_window_size:
                # Round to the nearest 0.5.
                poles_loc.add(round(self.time_measures[i] * 2) / 2)
                moments_of_poles.append(1)
            else:
                moments_of_poles.append(0)
            found = False
        return poles_loc, treshold, moments_of_poles

    def __butter_lowpass(self):
        nyq = 0.5 * self.fs
        normal_cutoff =  self.cutoff / nyq
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        return b, a

    def __butter_lowpass_filter(self, data):
        b, a = self.__butter_lowpass()
        y = lfilter(b, a, data)
        return y


