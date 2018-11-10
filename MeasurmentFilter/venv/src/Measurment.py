class Measurment:
    poles = []
    time_of_measurment = 0
    path_of_file = 0

    def __init__(self, path_of_file, poles, time_of_measurment):
        self.path_of_file = path_of_file
        self.poles = poles
        self.time_of_measurment = time_of_measurment
