class Measurment:
    poles = []
    time_of_measurment = 0
    path_of_file = 0

    def __init__(self, path_of_file, poles, time_tuple):
        self.path_of_file = path_of_file
        self.poles = poles
        self.start = time_tuple[0]
        self.stop = time_tuple[1]
        self.number = int(self.path_of_file[len(path_of_file) - 5])
