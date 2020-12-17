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

    def __init__(self, source_file, option, exit_file=None):
        """
        :type source_file: str
        :type option: int
        :type exit_file: str
        :param source_file: .txt file to be read with the parameters of the run
        :param option: path options (should be between 1 - 4) -> int
        :param exit_file: optional parameter, creates an .txt output file for the chosen path
        """
        self.source_file = open(source_file, 'r').read().split('\n')
        self.option = option
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
        for line in temp_labyrinth:
            print(line)

        def step(current_position, direction, path=None):
            if path is None:
                path = []
            if temp_labyrinth[current_position[0]][current_position[1]]:
                path.append(current_position)
                if current_position == destination:
                    possible_paths.append(path)
                elif direction == 'up':
                    temp_labyrinth[current_position[0]][current_position[1]] = False
                    current_position = current_position[0] - 1, current_position[1]
                    step(current_position, 'up', path), step(current_position, 'right', path), \
                           step(current_position, 'left', path)
                elif direction == 'right':
                    temp_labyrinth[current_position[0]][current_position[1]] = False
                    current_position = current_position[0], current_position[1] + 1
                    return step(current_position, 'up', path), step(current_position, 'right', path), \
                           step(current_position, 'down', path)
                elif direction == 'down':
                    temp_labyrinth[current_position[0]][current_position[1]] = False
                    current_position = current_position[0] + 1, current_position[1]
                    return step(current_position, 'right', path), step(current_position, 'down', path), \
                           step(current_position, 'left', path)
                elif direction == 'left':
                    temp_labyrinth[current_position[0]][current_position[1]] = False
                    current_position = current_position[0], current_position[1] - 1
                    return step(current_position, 'up', path), step(current_position, 'down', path), \
                           step(current_position, 'left', path)
            else:
                temp_labyrinth[current_position[0]][current_position[1]] = False
                # reverts the previous step
                if direction == 'up':
                    # go down
                    current_position = current_position[0] + 1, current_position[1]
                    temp_labyrinth[current_position[0]][current_position[1]] = True
                    return step(current_position, 'right', path), step(current_position, 'down', path), \
                           step(current_position, 'left', path)
                elif direction == 'right':
                    # go left
                    current_position = current_position[0], current_position[1] - 1
                    return step(current_position, 'up', path), step(current_position, 'down', path), \
                           step(current_position, 'left', path)
                elif direction == 'down':
                    # go up
                    current_position = current_position[0] - 1, current_position[1]
                    return step(current_position, 'right', path), step(current_position, 'down', path), \
                           step(current_position, 'left', path)
                elif direction == 'left':
                    # go right
                    current_position = current_position[0], current_position[1] + 1
                    return step(current_position, 'up', path), step(current_position, 'right', path), \
                           step(current_position, 'down', path)
        step(initial_position, 'up')
        return possible_paths


try:
    temp = sys.argv[3]
except IndexError:
    temp = None

a = Labyrinth(sys.argv[1], int(sys.argv[2]), temp)
a.possible_paths()
