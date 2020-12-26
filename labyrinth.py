import sys


class Treasure:

    def __init__(self, pos, value, weight):
        """
        :type pos: tuple
        :type value: float
        :type weight: float
        :param pos: coordinates of object in the labyrinth
        :param value: monetary value of object
        :param weight: weight of object
        """
        self.pos = pos
        self.value = value
        self.weight = weight


class Path:

    def __init__(self, path, labyrinth):
        """
        :type path: list
        :type labyrinth: labyrinth
        :param path: list of steps taken by the adventurer
        """
        self.path = path
        # self.duration = duration
        # self.inventory = inventory


class Labyrinth:
    """
    Class builds a labyrinth model and a treasure list
    """

    def __init__(self, source_file, exit_file=False):
        """
        :type source_file: str
        :type exit_file: str
        :param source_file: .txt file to be read with the parameters of the run
        :param exit_file: optional parameter, creates an .txt output file for the chosen path
        """
        self.source_file = open(source_file, 'r').read().split('\n')
        self.initial_pos = None
        self.destination = None
        self.labyrinth = []
        self.treasures = []

        # Creates an output file if needed
        if exit_file:
            self.exit_file = open(exit_file, 'w+')

        lab_size = self.source_file[0].split()
        lab_size = [int(elem) for elem in lab_size]

        for line in self.source_file[1:lab_size[0] + 1]:
            self.labyrinth.append([True if elem == '.' else False for elem in line])
        for line in self.labyrinth:
            line.insert(0, False)
            line.append(False)
        self.labyrinth.insert(0, [False for _ in range(lab_size[1] + 2)])
        self.labyrinth.append([False for _ in range(lab_size[1] + 2)])

        for line in self.source_file[lab_size[0] + 2:-2]:
            line = line.split(" ")
            self.treasures.append(Treasure((int(line[0]), int(line[1])), int(line[2]), int(line[3])))

        self.initial_pos = self.source_file[-2].split()
        self.initial_pos = tuple([int(elem) + 1 for elem in self.initial_pos])
        self.destination = self.source_file[-1].split()
        self.destination = tuple([int(elem) + 1 for elem in self.destination])

    def aux_print(self, to_print):
        """
        This function prints the parameters in the terminal and in a file if needed
        :param to_print:  object to be printed
        """
        if self.exit_file:
            self.exit_file.write(to_print)
        print(to_print)

    def possible_paths(self):
        possible_paths = []
        temp_labyrinth = self.labyrinth
        initial_position = self.initial_pos
        destination = self.destination
        print(initial_position)
        print(destination)
        for line in temp_labyrinth:
            print(line)

        def step(current_position, laby, path=[]):
            path.append(current_position)
            laby[current_position[0]][current_position[1]] = False
            print(path)
            print(current_position, laby[current_position[0]][current_position[1]])
            laby = temp_labyrinth
            for elem in path:
                laby[elem[0]][elem[1]] = False
            try:
                while path[-1] not in [tuple([path[-2][0] - 1, path[-2][1]]),
                                       tuple([path[-2][0], path[-2][1] + 1]),
                                       tuple([path[-2][0] + 1, path[-2][1]]),
                                       tuple([path[-2][0], path[-2][1] - 1])]:
                    path.pop(-2)
            except IndexError:
                pass
            if current_position == destination:
                possible_paths.append(path)
            else:
                # Goes up
                if laby[current_position[0] - 1][current_position[1]]:
                    step(tuple([current_position[0] - 1, current_position[1]]), laby, path)
                # Goes right
                if laby[current_position[0]][current_position[1] + 1]:
                    step(tuple([current_position[0], current_position[1] + 1]), laby, path)
                # Goes down
                if laby[current_position[0] + 1][current_position[1]]:
                    step(tuple([current_position[0] + 1, current_position[1]]), laby, path)
                # Goes left
                if laby[current_position[0]][current_position[1] - 1]:
                    step(tuple([current_position[0], current_position[1] - 1]), laby, path)

        step(initial_position, temp_labyrinth)
        print(len(possible_paths))
        return possible_paths


try:
    temp = sys.argv[3]
except IndexError:
    temp = False

a = Labyrinth(sys.argv[1], temp)
a.possible_paths()
