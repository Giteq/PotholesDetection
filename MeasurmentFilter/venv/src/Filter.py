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
import scipy.signal as signal

#http://newline.nadav.org/

# '/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/matplotlibrc' -> plik do zmiany domyślnej ścieżki do zapisywania wykresów

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
        self.filterOrder = 4  # Order of Buttewroth filter.
        self.cutoff = 14  # desired cutoff frequency of the filter, Hz
        self.time_between_samples = 0.0032 #in seconds
        self.x_treshold = 0.1
        self.vel_tresh = 2.5
        self.y_tresh = 8
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
                    self.x_measures.append(float(lines[i][0]) * 0.061)
                    self.y_measures.append(float(lines[i][1]) * 0.061)
                    self.z_measures.append(float(lines[i][2]) * 0.061)

                else:
                    break
            except ValueError:
                print("")

    def filter_data(self):
        self.not_fil_z = copy.copy(self.z_measures)
        self.not_fil_velocity = self.calculate_velocity()
        self.z_measures = self.__butter_lowpass_filter(self.z_measures)
        self.x_measures = self.__butter_lowpass_filter(self.x_measures)
        self.y_measures = self.__butter_lowpass_filter(self.y_measures)
        self.cutoff = 0.0001
        self.x_measures = self.__noch_filter(self.x_measures, 0.00015)
        self.x_std_dev = statistics.stdev(self.x_measures)
        # self.x_measures = self.__kalman_filter(self.x_measures, process_variance=1e-2)
        self.velocity = self.calculate_velocity()
        # self.velocity = self.__kalman_2(self.x_measures)
        # self.velocity = [x * 10 for x in self.velocity]
        # self.cutoff = 0.0001
        # self.y_measures = self.__noch_filter(self.y_measures, 0.00015)
        # self.y_measures = self.__kalman_filter(self.y_measures, process_variance=1e-2)
        # self.y_measures, _ = self.__kalman_2(self.y_measures)

    def calculate_velocity(self):
        return  cumtrapz(self.x_measures, self.time_measures, initial=0)
        # self.velocity = [x * 5 for x in self.velocity]

    def gen_second_velocity(self, start, stop):
        ret_list = []
        tmp2 = start
        tmp = 0
        while tmp < 1:
            tmp += (1 / self.fs)
            tmp2 += (stop - start) * (1 / self.fs)
            ret_list.append(tmp2)

        return ret_list

    def gen_real_velocity(self):
        tmp = []

        # Pomiar nr 9
        # seconds = [0, 0, 0, 8, 21, 24, 28, 32, 39, 39, 40, 41, 44, 45, 45, 45, 45, 45, 45, 45, 46, 46, 46, 46, 47, 47, \
        #            47, 47, 47, 47, 47, 48, 47, 46, 45, 45, 45, 45, 43, 42, 40, 39, 34, 33, 32, 31, 33, 35, 34, 31, 28]


        #xses = np.arange(0, (15650 * (1 / self.fs)), (1 / self.fs))

        # Pomiar nr 14 2 minuty 3 sekundy xses = np.arange(0, (38499 * (1 / self.fs)), (1 / self.fs))
        seconds = [0, 13, 26, 32, 34, 36, 40, 43, 44, 46, 45, 45, 45, 45, 45, 45, 45, 46, 47, \
                   46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, \
                   46, 46, 46, 46, 44, 43, 43, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 38, 37, 37, 34, 30, 27, \
                   24,  11, 5, 0, 0, 0, 0, 0, 4, 13, 17, 23, 30, 38, 31, 41, 43, 46, 47, 49, 50, \
                   51, 51, 50, 46, 37, 33, 21, 23, 11, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, \
                   6,  10, 17,  18, 23, 26, 31, 33, 33, 33, 29, 26, 18, 11, 8,9,  14, 18, 23]

        # Pomiar nr 7 xses = np.arange(0, (38499 * (1 / self.fs)), (1 / self.fs))
        # seconds = [0, 0, 8, 11, 19, 26, 31, 33, 34, 34, 35, 35, 35, 35, 34, 29, 28, \
        #            26, 25, 25, 25, 26, 25, 24, 27, 29, 30, 32, 32, 33, 34, 34, 34, \
        #            33, 35, 36, 36, 36, 37, 37,37, 38, 38, 38, 37, 37, 37, 37, 38, 39, \
        #            40, 40, 39, 38, 38, 38, 38, 38, 39, 40, 41, 42, 42, 42, 42, 42, \
        #            42, 43, 44, 44, 44, 44, 45, 45, 45, 45, 45, 44, 43, 41, 38, 35, \
        #            31, 30, 27, 25, 26, 25, 24, 24, 25, 26, 27, 27, 27, 27, 26, 25, 23,
        #             21, 12]

        for i in range(len(seconds) - 1):
            tmp.append(self.gen_second_velocity(seconds[i], seconds[i + 1]))
        flatten = [item for sublist in tmp for item in sublist]
        print(flatten)
        xses = np.arange(0, (38499 * (1 / self.fs)), (1 / self.fs))

        return xses[:len(flatten)], flatten



    def plot_result(self, string):

        if 'x' in string:
            plt.figure(1)
            # plt.subplot(3, 1, 1)
            plt.plot(self.time_measures, self.x_measures)
            # plt.gcf().autofmt_xdate()
            plt.ylabel('Not filtered X')

        if 'y' in string:
            plt.figure(2)
            plt.plot(self.time_measures, self.y_measures)
            plt.ylabel('Filtered Y')
        if 'z' in string:
            fig = plt.figure(5)
            ax1 = plt.subplot(111)
            ax1.plot(self.time_measures, self.z_measures)
            ax1.title.set_text("Odczyty z osi Z")
            ax1.set_ylabel("Przyspieszenie [mg]")
            self.real_poles(self.z_measures, self.time_measures, ax1)
            # Porownanie
            # ax1 = plt.subplot(211)
            # ax1.plot(self.time_measures, self.not_fil_z)
            # ax1.title.set_text("Odczyty z osi Z przed filtracją")
            # ax1.set_ylabel("Przyspieszenie [mg]")
            # ax2 = plt.subplot(212, sharex=ax1)
            # ax2.plot(self.time_measures, self.z_measures)
            # ax2.title.set_text("Odczyty z osi Z po filtracji")
            # ax2.set_xlabel("Czas [s]")
            # ax2.set_ylabel("Przyspieszenie [mg]")

        if 'v' in string:
            plt.figure(6)

            x, y = self.gen_real_velocity()
            plt.plot(x, y)

            ax1 = plt.subplot(211)
            ax1.plot(self.time_measures[:len(self.velocity)], self.not_fil_velocity)
            ax1.plot(x, y)
            ax1.title.set_text("Uzyskana prędkość przed filtracją")
            ax1.set_ylabel("Prędkość [km/h]")
            ax2 = plt.subplot(212, sharex=ax1)
            ax2.plot(self.time_measures[:len(self.velocity)], self.velocity)
            ax2.plot(x, y)
            ax2.title.set_text("Uzyskana prędkość po filtracją")
            ax2.set_xlabel("Czas [s]")
            ax2.set_ylabel("Prędkość [km/h]")
            plt.xlabel("Czas [s]")

            plt.legend(["Prędkość wyliczona", "Prędkość rzeczywista"])
        if 'filter' in string:
            self.__print_noch_char()
        plt.show()

    def split_mesures(self, measures, time_measures, time_window):
        splied_measures = [[]]
        num_of_splited = 0
        for i in range(len(measures)):
            if time_measures[i] < time_window * (num_of_splited + 1):
                splied_measures[num_of_splited].append(measures[i])
            else:
                num_of_splited += 1
                splied_measures.append([])
                splied_measures[num_of_splited].append(measures[i])

        return splied_measures

    def find_poles(self):

        time_window = 5

        splited_z_measures = self.split_mesures(self.z_measures, self.time_measures, time_window)
        splited_y_measures = self.split_mesures(self.y_measures, self.time_measures, time_window)
        splited_velocity = self.split_mesures(self.velocity, self.time_measures, time_window)
        splited_time_measures = self.split_mesures(self.time_measures, self.time_measures, time_window)
        std_dev = statistics.stdev(self.z_measures)
        m = 2.0
        poles_loc = set()
        self.treshold = treshold = m * std_dev
        num_of_probes_to_phole = 10
        found = 0

        for window_no in range(len(splited_z_measures)):
            std_dev = statistics.stdev(splited_z_measures[window_no])
            treshold = m * std_dev
            for i in range(len(splited_z_measures[window_no]) - num_of_probes_to_phole):
                if abs(splited_z_measures[window_no][i]) > treshold and splited_velocity[window_no][i] > self.vel_tresh:
                    # and splited_y_measures[window_no][i] < self.y_tresh\
                    found += 1
                if found == num_of_probes_to_phole:
                    poles_loc.add(round(splited_time_measures[window_no][i]))
                    found = 0
        return poles_loc, treshold

    def __butter_lowpass_filter(self, data):
        nyq = 0.5 * self.fs
        normal_cutoff = (self.cutoff / nyq)
        print(normal_cutoff)
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        self.b = b
        self.a = a
        y = lfilter(b, a, data)
        return y

    def __butter_highpass_filter(self, data):
        nyq = 0.5 * self.fs
        normal_cutoff =  self.cutoff / nyq
        b, a = butter(self.filterOrder, normal_cutoff, btype='highpass', analog=False)
        y = lfilter(b, a, data)
        return y

    def __print_butter_char(self):
        self.cutoff = 16
        nyq = 0.5 * self.fs
        normal_cutoff = (self.cutoff / nyq)
        print(normal_cutoff)
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        # Plot the frequency response.
        w, h = freqz(b, a, worN=8000)
        plt.plot(0.5 * self.fs * w / np.pi, np.abs(h), 'b')
        plt.plot(self.cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(self.cutoff, color='k')
        plt.xlim(0, 0.5 * self.fs)
        plt.title("Charakterystyka amplitudowa dolnoprzepustowego filtru Butterwortha")
        plt.xlabel('Częstotliwość [Hz]')
        plt.ylabel('Wzmocnienie')
        plt.grid()

    def __print_noch_char(self):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        Q = normal_cutoff / self.bandwidth
        b, a = iirnotch(normal_cutoff, Q)
        w, h = freqz(b, a, worN=8000)
        h = [abs(x) if abs(x) > 0.9 else abs(x) - 0.5 for x in h]
        plt.plot(0.5 * self.fs * w / np.pi, np.abs(h), 'b')

        x = [0.00582,  0.051]
        y = [0.5 * np.sqrt(2), 0.5 * np.sqrt(2)]
        plt.text(np.average(x) - 0.015, y[0] + 0.01, "$\Delta f$")
        plt.plot(0.02, 0.14, 'ko')
        plt.text(0.03, 0.14, "$f_0$")
        plt.plot(x,y)
        plt.axvline(self.cutoff, color='k')
        plt.xlim(0, 0.3)
        plt.plot()
        plt.title("Charakterystyka amplitudowa filtru Noch")
        plt.xlabel('Częstotliwość [Hz]')
        plt.ylabel('Wzmocnienie')
        plt.grid()


    def __noch_filter(self, data, bandwidth):
        nyq = 0.5 * self.fs
        self.bandwidth = bandwidth
        normal_cutoff = self.cutoff / nyq
        Q = normal_cutoff / bandwidth
        b, a = iirnotch(normal_cutoff, Q)
        y = lfilter(b, a, data)
        return y

    def __kalman_filter(self, measures, process_variance):
        measurement_standard_deviation = statistics.stdev(measures)
        estimated_measurement_variance = measurement_standard_deviation ** 2
        kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)

        for i in range(len(measures)):
            kalman_filter.input_latest_noisy_measurement(measures[i])
            measures[i] = kalman_filter.get_latest_estimated_measurement()

        return measures

    def __kalman_2(self, measures):
        from pykalman import KalmanFilter
        import numpy as np
        import matplotlib.pyplot as plt

        # Data description
        #  Time
        #  AccX_HP - high precision acceleration signal
        #  AccX_LP - low precision acceleration signal
        #  RefPosX - real position (ground truth)
        #  RefVelX - real velocity (ground truth)

        # switch between two acceleration signals
        AccX_Variance = 0.0007

        # time step
        dt = 1 / self.fs

        # transition_matrix
        F = [1]

        # observation_matrix
        H = [1]

        # transition_covariance
        Q = [dt**2]

        # observation_covariance
        R = self.x_std_dev

        # transition offset
        B = [dt]

        # initial_state_mean
        X0 = [0]

        # initial_state_covariance
        P0 = [dt**2]

        n_timesteps = np.array(measures).shape[0]
        n_dim_state = 1
        filtered_state_means = np.zeros((n_timesteps, n_dim_state))
        filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))

        kf = KalmanFilter(transition_matrices=F,
                          observation_matrices=H,
                          transition_covariance=Q,
                          observation_covariance=R,
                          initial_state_mean=X0,
                          initial_state_covariance=P0,
                          transition_offsets=B)

        # iterative estimation for each new measurement
        for t in range(n_timesteps):
            if t == 0:
                filtered_state_means[t] = X0
                filtered_state_covariances[t] = P0
            else:
                filtered_state_means[t], filtered_state_covariances[t] = (
                    kf.filter_update(
                        filtered_state_means[t - 1],
                        filtered_state_covariances[t - 1],
                        measures[t]
                    )
                )

        # Acc, Vel, Pos
        return filtered_state_means[:, 0]

