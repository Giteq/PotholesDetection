from Filter import Filtr
from Measurment import Measurment


def getPath(num_of_measure):
    return "../../../RaspberryPi_drivers/Measurments/" + str(num_of_measure) + ".txt"


def fill_labelator(labelator):
    for i in range(len(measures)):
        labelator.add_potholes(measures[i])


def check_result(labels, poles):
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
        [11, 13, 15, 17, 20, 23, 25, 27, 30],
        [7, 10, 15, 20, 26, 28, 31,  37, 41, 45, 46],
        [9, 15, 25, 27, 39, 41, 43, 55, 57],
        [2, 4, 5, 7, 8, 11, 13, 14, 15, 17, 19, 20, 23, 25, 28, 31, 34, 36, 38, 40, 44, 51, 53, 55, 65, 68, 73, 79],
        [3, 4, 6],
        [8, 9, 10, 11, 13, 15, 20, 21, 23, 25, 28, 31, 34, 37, 39, 41, 44, 48]
    ]
    times_of_measurment = [33, 51, 59, 80, 9, 50]

    measurments = []

    for i in range(len(poles)):
        measurments.append(Measurment(getPath(i + 1 + 3), poles[i], times_of_measurment[i]))

    return measurments

def test(measure_no, real_poles, time_of_measure):
    measure = Measurment(getPath(measure_no), real_poles, time_of_measure)
    filter = Filtr(measure)
    poles_loc, _, _ = filter.find_poles()
    filter.plot_result("z")
    print(f"Wykryte dziury {poles_loc}")
    print(f"Prawidziwe dziury {real_poles}")

if __name__ == "__main__":
    poles = [4, 8, 10, 11, 15, 18, 20]
    test(10, poles, 15)
    # measurments = init()
    # results = [0, 0, 0]
    # i = 4
    # for measure in measurments:
    #     print(f'Measure number {i}')
    #     i += 1
    #     filter = Filtr(measure)
    #     poles_loc, _, _ = filter.find_poles()
    #     results = [sum(x) for x in zip(results, check_result(measure.poles, poles_loc))]
    #     if "7" in measure.path_of_file:
    #         filter.plot_result("z")
    #
    # print(f'Probes: {results[0]}')
    # print(f'False negatives: {results[1]}')
    # print(f'False positives: {results[2]}')
    # print(f'Accuracy: {(results[0] - results[1]) / results[0]}')

# Założenia:
# Minimalna głębokość dziury jaką uznaje za dziurę to 20 cm
# Maksymalna prędkość jaką przyjmuję to 100 km/h
# Minimalny czas jaki mogę spędzić w dziurze to 0.1