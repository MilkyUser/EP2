import sys
import copy


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
        :param source_file: .txt file name to be read with the parameters of the run
        :param exit_file: optional parameter, creates an .txt output file for the chosen path
        """
        self.source_file = open(source_file, 'r').read().split('\n')
        self.initial_pos = None
        self.destination = None
        self.labyrinth_matrix = []
        self.treasures = []

        # Creates an output file if needed
        if exit_file:
            self.exit_file = open(exit_file, 'w+')

        lab_size = self.source_file[0].split()
        lab_size = [int(elem) for elem in lab_size]

        for line in self.source_file[1:lab_size[0] + 1]:
            self.labyrinth_matrix.append([True if elem == '.' else False for elem in line])
        for line in self.labyrinth_matrix:
            line.insert(0, False)
            line.append(False)
        self.labyrinth_matrix.insert(0, [False for _ in range(lab_size[1] + 2)])
        self.labyrinth_matrix.append([False for _ in range(lab_size[1] + 2)])

        for line in self.source_file[lab_size[0] + 2:-2]:
            line = line.split(" ")
            self.treasures.append(Treasure((int(line[0]), int(line[1])), int(line[2]), int(line[3])))

        self.initial_pos = self.source_file[-2].split()
        self.initial_pos = tuple([int(elem) + 1 for elem in self.initial_pos])
        self.destination = self.source_file[-1].split()
        self.destination = tuple([int(elem) + 1 for elem in self.destination])

    def __str__(self):
        s = ''
        for line in self.labyrinth_matrix:
            for elem in line:
                if elem:
                    s = s + '.'
                else:
                    s = s + 'X'
        return s

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
        temp_labyrinth = copy.deepcopy(self.labyrinth_matrix)
        initial_position = self.initial_pos
        destination = self.destination

        def step(pos, labyrinth_matrix, path=None):

            if path is None:
                path = []

            def enclosing_step(current_position, current_labyrinth, current_path):
                # this function is needed to create a Python closure instance

                def do_step():
                    current_labyrinth[current_position[0]][current_position[1]] = False
                    current_path.append(current_position)
                    temp_path = copy.deepcopy(current_path)
                    temp_labyrinth2 = copy.deepcopy(current_labyrinth)

                    if current_position == destination:
                        possible_paths.append(current_path)

                    else:
                        # Goes up if possible
                        if current_labyrinth[current_position[0] - 1][current_position[1]]:
                            next_position = current_position[0] - 1, current_position[1]
                            go_up = enclosing_step(next_position, temp_labyrinth2, temp_path)
                            go_up()
                        # Goes right if possible
                        if current_labyrinth[current_position[0]][current_position[1] + 1]:
                            next_position = current_position[0], current_position[1] + 1
                            go_right = enclosing_step(next_position, temp_labyrinth2, temp_path)
                            go_right()
                        # Goes down if possible
                        if current_labyrinth[current_position[0] + 1][current_position[1]]:
                            next_position = current_position[0] + 1, current_position[1]
                            go_down = enclosing_step(next_position, temp_labyrinth2, temp_path)
                            go_down()
                        # Goes left if possible
                        if current_labyrinth[current_position[0]][current_position[1] - 1]:
                            next_position = current_position[0], current_position[1] - 1
                            go_left = enclosing_step(next_position, temp_labyrinth2, temp_path)
                            go_left()

                return do_step  # returns the nested function

            do_first_step = enclosing_step(pos, labyrinth_matrix, path)
            do_first_step()

        step(initial_position, temp_labyrinth)
        return possible_paths


try:
    temp = sys.argv[3]
except IndexError:
    temp = False

a = Labyrinth(sys.argv[1], temp)
