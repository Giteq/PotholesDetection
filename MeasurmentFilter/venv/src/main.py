from Filter import Filtr
from Measurment import Measurment
import numpy as np
import matplotlib.pyplot as plt
import json

best_mx = 2.2
best_mz = 1.8
best_time_window = 5

def check_result(real_poles, detected_poles, measure_time):
    false_negatives = set()
    false_positives = set()
    true_negative = set()
    true_positive = set()

    for i in range(measure_time + 1):
        for pole in detected_poles:
            if i in real_poles:
                if pole - 0.5 <= i <= pole + 0.5:
                    true_positive.add(i)
    visited_pole = 0
    for pole in real_poles:
        for det_pole in detected_poles:
            if not pole - 0.5 <= det_pole <= pole + 0.5:
                visited_pole +=1
        if visited_pole == len(detected_poles):
            false_negatives.add(pole)
        visited_pole = 0

    visited_pole = 0
    for pole in detected_poles:
        for true_pole in real_poles:
            if not true_pole  - 0.5 <= pole <= true_pole + 0.5:
                visited_pole += 1
        if visited_pole == len(real_poles):
            false_positives.add(int(pole))
        visited_pole = 0

    for i in range(measure_time + 1):
        if i not in list(false_positives) and i not in list(false_negatives) and i not in list(true_positive):
            true_negative.add(i)

    print(f'Real poles {sorted(list(real_poles))}')
    print(f'All detected poles {sorted(list(detected_poles))}')
    print(f'True positives {sorted(list(true_positive))}')
    print(f'False negatives {sorted(list(false_negatives))}')
    print(f'False positives {sorted(list(false_positives))}')
    print(f'True negatives {sorted(list(true_negative))}')

    return len(true_positive), len(true_negative), len(false_positives), len(false_negatives), len(real_poles)


def init_acc():
    with open('../real_potholes.json') as json_file:
        data = json.load(json_file)
        measurments = []

        for i in range(len(data)):
            path = f"../../../RaspberryPi_drivers/measurments/acc/{data[i]['number']}.txt"
            measurments.append(Measurment(path, data[i]["potholes"], data[i]["time"]))

    return measurments, sum([x["time"][1] - x["time"][0] for x in data])


def find_precesion(m, mx, width):
    acc_measurments, full_measures_time = init_acc()
    gl_false_pos = 0
    gl_false_neg = 0
    gl_true_neg = 0
    gl_true_pos = 0
    for measure in acc_measurments:
        print("\n")
        print(f'Measure number {measure.number}')
        print(f'm = {m}')
        print(f'width = {width}')
        filter = Filtr(measure, m, mx, width)
        poles_loc = filter.find_poles()
        true_pos, true_neg, false_pos, false_neg, real_poles = check_result(measure.poles, poles_loc,
                                                                (measure.stop - measure.start))
        gl_false_pos += false_pos
        gl_false_neg += false_neg
        gl_true_pos += true_pos
        gl_true_neg += true_neg

    accuracy = 100 * (gl_true_pos) / (gl_true_pos + gl_false_pos + gl_false_neg)

    print(f'True negatives: {gl_true_neg}')
    print(f'True positives: {gl_true_pos}')
    print(f'False negatives: {gl_false_neg}')
    print(f'False positives: {gl_false_pos}')
    print(f'Full time {full_measures_time }')
    print(f'Accuracy: {accuracy}')

    return gl_false_neg, gl_false_pos, gl_true_neg, gl_true_pos, accuracy


def best_accuracy():
    find_precesion(best_mx, best_mz, best_time_window)


def okno_czasowe_charakterystyka():
    accuracies = []
    all_false_positives = []
    all_false_negatices = []
    m = best_mz
    zakres = np.arange(1, 100, 1)
    mx =best_mx

    for width in zakres:
        gl_false_neg, gl_false_pos, gl_true_neg, gl_true_pos, accuracy = find_precesion(m, mx, width)
        all_false_negatices.append(gl_false_neg)
        all_false_positives.append(gl_false_pos)
        accuracies.append(accuracy)

    plt.figure(10)
    plt.ylabel("Skuteczność [%]")
    plt.title("Zależność skuteczności algorytmu od szerokości okna czasowego")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, accuracies)

    plt.figure(11)
    plt.ylabel("Ilość fałszywych nierówności")
    plt.title("Zależność ilości fałszywych nierówności od szerokości okna czasowego")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, all_false_positives)

    plt.figure(12)
    plt.ylabel("Ilość niewykrytych nierówności")
    plt.title("Zależność ilości niewykrytych nierówności od szerokości okna czasowego")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, all_false_negatices)



    plt.show()

def m_charakterystyka():
    accuracies = []
    all_false_positives = []
    all_false_negatices = []
    width = best_time_window
    zakres = np.arange(0, 4, 0.1)
    mx = best_mx

    for m in zakres:
        gl_false_neg, gl_false_pos, gl_true_neg, gl_true_pos, accuracy = find_precesion(m, mx, width)
        all_false_negatices.append(gl_false_neg)
        all_false_positives.append(gl_false_pos)
        accuracies.append(accuracy)

    plt.figure(10)
    plt.ylabel("Skuteczność [%]")
    plt.title("Zależność skuteczności od wartości parametru mz")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, accuracies)

    plt.figure(11)
    plt.ylabel("Ilość fałszywych nierówności")
    plt.title("Zależność ilości fałszywych nierówności od wartości parametru mz")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, all_false_positives)

    plt.figure(12)
    plt.ylabel("Ilość niewykrytych nierówności")
    plt.title("Zależność ilości niewykrytych nierówności od wartości parametru mz")
    plt.xlabel("Szerokość okna czasowego")
    plt.plot(zakres, all_false_negatices)
    plt.show()

if __name__ == "__main__":
    best_accuracy()
    # okno_czasowe_charakterystyka()
    # m_charakterystyka()
