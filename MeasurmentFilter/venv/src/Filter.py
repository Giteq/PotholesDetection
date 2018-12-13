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
import json

class Filtr:
    def __init__(self, measurment, m, mx, probes_to_pole):

        self.m = m
        self.mx = mx
        self.probes_to_pole = probes_to_pole
        self.start = measurment.start
        self.stop = measurment.stop
        self.fs = 1 / 0.0061
        self.filterOrder = 5
        self.cutoff = 14

        self.file = open(measurment.path_of_file, 'r')
        self.time_measures = []
        self.x_measures = []
        self.z_measures = []
        self.y_measures = []
        self.not_filtr_z = []
        self.velocity = []

        self.parse_file()
        self.time_measures = [x - self.start for x in self.time_measures]

        self.not_fil_x = copy.copy(self.x_measures)
        self.not_fil_z = copy.copy(self.z_measures)
        self.not_fil_velocity = self.calculate_velocity()
        self.filter_data()

    def parse_file(self):
        lines = self.file.read().split('\n')
        lines[:] = (x for x in lines if x != '')

        for i in range(len(lines)):
            lines[i] = lines[i].split("\t\t")
            try:
                if self.start <= float(lines[i][3]) <= self.stop:
                    self.time_measures.append((float(lines[i][3])))
                    self.x_measures.append(float(lines[i][0]) * 0.061 * constants.g / 1000)
                    self.y_measures.append(float(lines[i][1]) * 0.061)
                    self.z_measures.append(float(lines[i][2]) * 0.061)

                elif float(lines[i][3]) > self.stop:
                    break
            except ValueError:
                print("")
            except IndexError:
                pass

    def remove_g(self):
        mean = np.mean(self.z_measures)
        self.z_measures = [x - mean for x in self.z_measures]
        mean = np.mean(self.x_measures)
        self.x_measures = [x - mean for x in self.x_measures]

    def filter_data(self):
        self.z_measures = self.__butter_lowpass_filter(self.z_measures)
        self.x_measures = self.__butter_lowpass_filter(self.x_measures)
        self.cutoff = 0.0001
        self.x_measures = self.__noch_filter(self.x_measures, 0.00015)
        self.remove_g()
        self.velocity = self.calculate_velocity()

    def calculate_velocity(self):
        buff = cumtrapz(self.not_fil_x, self.time_measures, initial=0)
        buff = [x * 3.6 for x in buff]  # Convert to km/h
        self.not_fil_velocity = buff
        buff = cumtrapz(self.x_measures, self.time_measures, initial=0)
        buff = [x * 3.6 for x in buff]  # Convert to km/h
        return buff

    def gen_real_velocity(self):
        x = []
        y = []
        with open('../real_velocity.json') as json_file:
            data = json.load(json_file)

            for elem in data:
                for i in range(len(elem["velocity"])):
                    x.append(i)
                    y.append(elem["velocity"][i])

        return x, y

    def plot_axis(self, string):
        if 'x' in string:
            plt.figure(2)
            plt.plot(self.time_measures, self.x_measures)
            plt.title("X")
            plt.xlabel("Czas [s]")
            plt.ylabel("Przyspieszenie [mg]")
            plt.axhline(self.x_treshold)

        if 'y' in string:
            plt.figure(2)
            plt.plot(self.time_measures, self.y_measures)
            plt.title("Y")
            plt.xlabel("Czas [s]")
            plt.ylabel("Przyspieszenie [mg]")
        if 'z' in string:
            plt.figure(7)
            plt.plot(self.time_measures, self.z_measures)
            plt.title("Z")
            plt.xlabel("Czas [s]")
            plt.ylabel("Przyspieszenie [mg]")
        if 'v' in string:
            plt.figure(6)
            plt.title("V")
            x, y = self.gen_real_velocity()
            plt.plot(x, y)
            plt.figure(7)
            plt.plot(self.time_measures[:len(self.velocity)], self.velocity)
            plt.plot(x, y)
            plt.xlabel("Czas [s]")
            plt.ylabel("Prędkość [km/h]")
            plt.xlabel("Czas [s]")

            plt.legend(["Prędkość wyliczona", "Prędkość rzeczywista"])

        plt.show()

    def plot_result(self, trues, false_negatives, false_positives):
        plt.figure(6)
        plt.plot(self.time_measures, self.z_measures)
        plt.axhline(self.global_treshold,color='black', label='treshold')
        plt.axhline(-self.global_treshold, color='black', label='treshold')
        plt.ylabel("Przyspieszenie [mg]")
        plt.xlabel("Czas [s]")

        plt.figure(7)
        plt.plot(self.time_measures, self.x_measures)
        plt.axhline(self.x_treshold, color='black', label='treshold')
        plt.ylabel("Przyspieszenie [mg]")
        plt.xlabel("Czas [s]")

        plt.figure(8)
        for i in range(len(trues)):
            if i != len(trues) - 1:
                plt.plot([trues[i], trues[i]], [0, 1], color='green')
            else:
                plt.plot([trues[i], trues[i]], [0, 1], color='green', label="Wykryta nierówność")
        for i in range(len(false_negatives)):
            if i != len(false_negatives) - 1:
                plt.plot([false_negatives[i], false_negatives[i]], [0, 1], color='orange')
            else:
                plt.plot([false_negatives[i], false_negatives[i]], [0, 1], color='orange', label="Niewykryta nierówność")
        for i in range(len(false_positives)):
            if i != len(false_positives) - 1:
                plt.plot([false_positives[i], false_positives[i]], [0, 1], color='red')
            else:
                plt.plot([false_positives[i], false_positives[i]], [0, 1], color='red', label="Fałszywa nierówność")

        plt.ymax = 1
        plt.ylabel("Zdarzenia")
        plt.xlabel("Czas [s]")
        plt.legend(loc="best")
        plt.show()

    def find_poles(self):

        time_window = 5
        self.time_window = time_window
        poles_loc = set()
        self.all_tresholds = []
        num_of_probes_to_phole = self.probes_to_pole
        found = 0
        self.global_treshold = self.m * statistics.stdev(self.z_measures)
        self.x_treshold = - self.mx * statistics.stdev(self.x_measures)

        for i in range(len(self.z_measures)):
            if abs(self.z_measures[i]) > self.global_treshold:
                found += 1
            if found == num_of_probes_to_phole:
                if i - (self.fs) > 0 and  i + (self.fs) < len(self.x_measures):
                    for j in range(i - (int(self.fs)), i + (int(self.fs))):
                        if self.x_measures[j] < self.x_treshold:
                            poles_loc.add(round(self.time_measures[i]))
                found = 0
        return poles_loc

    def __butter_lowpass_filter(self, data):
        nyq = 0.5 * self.fs
        normal_cutoff = (self.cutoff / nyq)
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        self.b = b
        self.a = a
        y = lfilter(b, a, data)
        return y

    def __butter_highpass_filter(self, data):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.filterOrder, normal_cutoff, btype='highpass', analog=False)
        y = lfilter(b, a, data)
        return y

    def print_butter_char(self):
        nyq = 0.5 * self.fs
        normal_cutoff = (self.cutoff / nyq)
        b, a = butter(self.filterOrder, normal_cutoff, btype='lowpass', analog=False)
        # Plot the frequency response.
        w, h = freqz(b, a, worN=8000)
        plt.plot(0.5 * self.fs * w / np.pi, np.abs(h), 'b')
        plt.plot(self.cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(self.cutoff, color='k')
        plt.xlim(0, 0.5 * self.fs)
        plt.xlabel('Częstotliwość [Hz]')
        plt.ylabel('Wzmocnienie')
        plt.grid()

        plt.show()

    def __print_noch_char(self):
        self.cutoff = 0.0001
        self.bandwidth = 0.00015
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        Q = normal_cutoff / self.bandwidth
        b, a = iirnotch(normal_cutoff, Q)
        w, h = freqz(b, a, worN=19000)
        plt.plot(0.5 * self.fs * w / np.pi, np.abs(h), 'b')

        x = [0.0025,  0.0125]
        y = [0.5 * np.sqrt(2), 0.5 * np.sqrt(2)]
        plt.text(0.0015, y[0] + 0.03, "$\Delta \omega$")
        plt.plot(0.0040, 0.34, 'ko')
        plt.text(0.0060, 0.34, "$\omega_0$")
        plt.plot(x,y)
        plt.axvline(self.cutoff, color='k')
        plt.xlim(0, 0.3)
        plt.plot()
        plt.xlabel('Częstotliwość [Hz]')
        plt.ylabel('Wzmocnienie')
        plt.grid()

        plt.show()

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
        self.x_std_dev = statistics.stdev(self.x_measures)
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

