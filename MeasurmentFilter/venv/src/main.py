from Labelator import Labelator
from Filter import Filtr
from Measurment import Measurment


def getPath(num_of_measure):
    return "../../../RaspberryPi_drivers/Measurments/" + str(num_of_measure) + ".txt"


def fill_labelator(labelator):
    for i in range(len(measures)):
        labelator.add_potholes(measures[i])


def check_result(labels, poles):
    detected = False
    false_negative = 0
    false_positive = 0
    print(poles)
    print(labels)
    for pole in poles:
        for label in labels:
            if label - 1 <= pole <= label + 1:
                detected = True
                break
        if not detected:
            false_positive += 1
        detected = False

    detected = False
    for label in labels:
        for pole in poles:
            if label - 1 <= pole <= label + 1:
                detected = True
                break
        if not detected:
            false_negative += 1
        detected = False

    print("False negative " + str(false_negative))
    print("False positive " + str(false_positive))


def init():
    poles = [[6, 11],
             [10, 14, 19, 20, 30, 52],
             [7, 13, 20, 26, 32, 42]]
    times_of_measurment = [50, 60, 10]

    measurments = []

    for i in range(len(poles)):
        measurments.append(Measurment(getPath(i + 1), poles[i], times_of_measurment[i]))

    return measurments

if __name__ == "__main__":
    measurments = init()

    for measure in measurments:
        num_of_measure = 1
        filter = Filtr(measure)
        poles_loc, _, _ = filter.find_poles()
        filter.plot_result("z")
        labelator = Labelator(measure)
        label = labelator.label()
        check_result(measure.poles, poles_loc)


# Założenia:
# Minimalna głębokość dziury jaką uznaje za dziurę to 20 cm
# Maksymalna prędkość jaką przyjmuję to 100 km/h
# Minimalny czas jaki mogę spędzić w dziurze to 0.1