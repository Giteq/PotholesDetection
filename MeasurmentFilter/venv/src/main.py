from Filter import Filtr
from Measurment import Measurment
import numpy as np
import matplotlib.pyplot as plt

dt = 0.0032

def getPath(num_of_measure):
    return "../../../RaspberryPi_drivers/Measurments/" + str(num_of_measure) + ".txt"


def fill_labelator(labelator):
    for i in range(len(measures)):
        labelator.add_potholes(measures[i])


def check_result(labels, poles):
    # labels - prawdziwe
    # poles - wykryte
    detected = False
    false_negative_len = 0
    false_positive_len = 0

    false_negatives = []
    false_positives = []
    for pole in poles:
        for label in labels:
            if label - 1 <= pole <= label + 1:
                detected = True
                break
        if not detected:
            false_positive_len += 1
            false_positives.append(pole)
        detected = False

    detected = False
    for label in labels:
        for pole in poles:
            if label - 1 <= pole <= label + 1:
                detected = True
                break
        if not detected:
            false_negative_len += 1
            false_negatives.append(label)
        detected = False

    print(f'Real poles {labels}')
    print(f'Detected poles {poles}')
    print(f'False negatives {false_negatives}')
    print(f'False positives {false_positives}')

    return [len(labels), false_negative_len, false_positive_len]


def init():
    poles = \
    [
        [4, 7, 11, 13, 15, 17, 20, 23, 25, 27, 30, 32],
        [7, 10, 15, 18, 20, 23, 26, 28, 31, 35, 37, 41, 43, 45, 46, 50],
        [6, 9, 15, 20, 25, 27, 39, 41, 43, 47, 50, 55, 57],
        [2, 4, 5, 7, 8, 11, 13, 14, 15, 17, 19, 20, 23, 25, 28, 31, 34, 36, 38, 40, 44, 46, 51, 53, 55, 65, 68, 73, 79],
        [3, 4, 6],
        [8, 9, 10, 11, 13, 15, 18, 20, 21, 23, 25, 28, 31, 34, 37, 39, 41, 44, 46, 48]
    ]
    # zmienic 100 na 80, jeśli ważna accuracy
    times_of_measurment = [33, 51, 59, 100, 9, 50]

    measurments = []

    for i in range(len(poles)):
        measurments.append(Measurment(getPath(i + 1 + 3), poles[i], times_of_measurment[i]))

    return measurments

def test(measure_no, real_poles, time_of_measure):

    if measure_no == 10:
        measure = Measurment(getPath(measure_no), real_poles, time_of_measure)
        filter = Filtr(measure)
        poles_loc, _ = filter.find_poles()

        detected = False
        false_negative_len = 0
        false_positive_len = 0

        false_negatives = []
        false_positives = []
        for pole in poles_loc:
            for label in real_poles:
                if label - 1 <= pole <= label + 1:
                    detected = True
                    break
            if not detected:
                false_positive_len += 1
                false_positives.append(pole)
            detected = False

        detected = False
        for label in real_poles:
            for pole in poles_loc:
                if label - 1 <= pole <= label + 1:
                    detected = True
                    break
            if not detected:
                false_negative_len += 1
                false_negatives.append(label)
            detected = False

        print(f'Real poles {real_poles}')
        print(f'Detected poles {poles_loc}')
        print(f'False negatives {false_negatives}')
        print(f'False positives {false_positives}')
        filter.plot_result("z")
        return [len(real_poles), false_negative_len, false_positive_len]

    else:
        return 0, 0, 0

if __name__ == "__main__":
    # 158 nierówności

    print("\n\n-------Test-------\n\n")
    test_poles = [[4, 8, 10, 11, 15, 18],
                  [9, 11, 15,18, 25, 28, 30, 32, 34, 38, 40, 42, 44, 47, 50, 54, 56, 62, 66],
                  [4, 8, 11, 12, 21, 24, 27, 30, 34, 36, 39, 41, 43, 46, 48, 53, 58, 63, 70],
                  [6, 7, 12, 15, 17, 20, 23, 56, 58, 61, 66, 71, 73, 75, 78, 81, 83, 85, 88, 92, 96, 99, 103, 106, 112, 115, 119, 122, 129, 131], # 13 pomiar zakręt pod góre, super widać efekt okna czasowego
                  [4, 6, 8, 11, 14, 17, 20, 23, 25, 27, 30, 34, 37, 39, 42, 45, 48, 50, 53, 56, 68, 72, 83, 85, 106, 110, 115, 122, 124, 127, 130, 131, 132, 136] # 14 poiar fajny do pokazania prędkości
                  ]
    time_test = [18, 73, 62, 132, 123] # 140
    i = 0
    results = [0, 0, 0]
    for test_pole in test_poles:
        results = [sum(x) for x in zip(results, test(10 + i, test_pole, time_test[i]))]
        i += 1

    print(f'Probes: {results[0]}')
    print(f'False negatives: {results[1]}')
    print(f'False positives: {results[2]}')
    print(f'Accuracy: {(results[0] - results[1]) / results[0]}')

    print("\n\n-------Strojenie-------\n\n")
    measurments = init()
    results = [0, 0, 0]
    i = 4
    for measure in measurments:
        if "7" in measure.path_of_file:
            print(f'Measure number {i}')
            i += 1
            filter = Filtr(measure)
            poles_loc, _ = filter.find_poles()
            results = [sum(x) for x in zip(results, check_result(measure.poles, poles_loc))]
            print(f'Probes: {results[0]}')
            print(f'False negatives: {results[1]}')
            print(f'False positives: {results[2]}')
            print(f'Accuracy: {(results[0] - results[1]) / results[0]}')
            filter.plot_result("z")

# Założenia:
# Minimalna głębokość dziury jaką uznaje za dziurę to 20 cm
# Maksymalna prędkość jaką przyjmuję to 100 km/h
# Minimalny czas jaki mogę spędzić w dziurze to 0.1