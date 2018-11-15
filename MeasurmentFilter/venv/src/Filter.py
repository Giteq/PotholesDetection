import numbers
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, iirnotch
from datetime import datetime, timedelta
import statistics
import matplotlib.dates as dates
from datetime import datetime
import numpy as np
import math
from scipy.integrate import cumtrapz
import scipy.constants as constants
from KalmanFilter import KalmanFilter
import copy

#http://newline.nadav.org/

#Liczenie G
#http://ozzmaker.com/accelerometer-to-g/

class Filtr:
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
        self.cutoff = 15  # desired cutoff frequency of the filter, Hz
        self.time_between_samples = 0.0032 #in seconds
        self.x_treshold = 0.1
        self.vel_tresh = 0.05
        self.y_tresh = 3
        self.time_of_measure = measurment.time_of_measurment
        self.parse_file()
        self.filter_data()

    def parse_file(self):
        lines = self.file.read().split('\n')
        lines[:] = (x for x in lines if x != '')

        for i in range(len(lines)):
            lines[i] = lines[i].split("\t\t")
            #Filter empty strings in list
            try:
                if self.time_of_measure >= float(lines[i][3]):
                    self.time_measures.append((float(lines[i][3])))
                    self.x_measures.append(int(lines[i][0]) / 40)
                    self.y_measures.append(int(lines[i][1]) / 40)
                    self.z_measures.append(int(lines[i][2]) / 40)

                else:
                    break
            except ValueError:
                print("")

    def filter_data(self):
        self.not_fil_z = copy.copy(self.z_measures)
        self.z_measures = self.__butter_lowpass_filter(self.z_measures)
        self.x_measures = self.__butter_lowpass_filter(self.x_measures)
        self.cutoff = 0.001
        self.x_measures = self.__noch_filter(self.x_measures, 0.001)
        self.x_measures = self.__kalman_filter(self.x_measures, process_variance=1e-3)
        self.calculate_velocity()
        self.cutoff = 15
        self.y_measures = self.__butter_lowpass_filter(self.y_measures)
        self.cutoff = 0.001
        self.y_measures = self.__noch_filter(self.y_measures, 0.001)
        self.y_measures = self.__kalman_filter(self.y_measures, process_variance=1e-3)

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
            plt.plot(self.time_measures, self.not_fil_z)
            plt.ylabel('Not filtered Z')
            plt.plot(self.time_measures, self.z_measures)
            plt.axhline(y=treshold, color='r', linestyle='-')
            plt.axhline(y=-treshold, color='r', linestyle='-')
            plt.ylabel('Filtered Z')
            plt.legend(["Not filtered", "Filtered"])

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
        m = 1.8
        poles_loc = set()
        moments_of_poles = []   # 1-> there is pole, 0-> there is not
        treshold = m * std_dev
        time_window_size = 1
        found = 0

        for i in range(len(self.time_measures) - time_window_size):
            for j in range(time_window_size):
                if abs(self.z_measures[i+j]) > treshold:
                    found += 1
            if found == time_window_size and self.velocity[i] > self.vel_tresh and self.y_measures[i] < self.y_tresh:
                poles_loc.add(int(self.time_measures[i]))
                moments_of_poles.append(1)
            else:
                moments_of_poles.append(0)
            found = False
        return poles_loc, treshold, moments_of_poles

    def __butter_lowpass_filter(self, data):
        nyq = 0.5 * self.fs
        normal_cutoff =  self.cutoff / nyq
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        y = lfilter(b, a, data)
        return y

    def __noch_filter(self, data, bandwidth):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        Q = normal_cutoff / bandwidth
        b, a = iirnotch(normal_cutoff, Q)
        y = lfilter(b, a, data)
        return y

    def __kalman_filter(self, measures, process_variance):
        measurement_standard_deviation = statistics.stdev(measures)
        estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2
        kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)

        for i in range(len(measures)):
            kalman_filter.input_latest_noisy_measurement(measures[i])
            measures[i] = kalman_filter.get_latest_estimated_measurement()

        return measures
