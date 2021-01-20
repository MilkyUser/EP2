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
        :type labyrinth: Labyrinth
        :param path: list of steps taken by the adventurer
        """
        self.path = path
        self.inventory = []
        self.total_value = 0
        self.total_weight = 0
        self.duration = 0
        time_sqrt = 1
        available_treasures = labyrinth.treasures
        for x, pos in enumerate(path):
            if x > 0:
                self.duration += time_sqrt**2
            if pos in [available_treasures[x].pos for x, _ in enumerate(available_treasures)]:
                index = [available_treasures[x].pos for x, _ in enumerate(available_treasures)].index(pos)
                time_sqrt += (float(available_treasures[index].weight) / 10)
                self.inventory.append(available_treasures[index])
                self.total_value += available_treasures[index].value
                self.total_weight += available_treasures[index].weight


class Labyrinth:
    """
    Class builds a labyrinth model and a treasure list
    """

    def __init__(self, source_file):
        """
        :type source_file: str
        :param source_file: .txt file name to be read with the parameters of the run
        """
        self.source_file = open(source_file, 'r').read().split('\n')
        self.initial_pos = None
        self.destination = None
        self.labyrinth_matrix = []
        self.treasures = []
a
        lab_size = self.source_file[0].split()
        lab_size = [int(elem) for elem in lab_size]

        for line in self.source_file[1:lab_size[0] + 1]:
            self.labyrinth_matrix.append([True if elem == '.' else False for elem in line])
        for line in self.labyrinth_matrix:
            line.insert(0, False)
            line.append(False)
        self.labyrinth_matrix.insert(0, [False for _ in range(lab_size[1] + 2)])
        self.labyrinth_matrix.append([False for _ in range(lab_size[1] + 2)])

        # Builds treasures list
        for line in self.source_file[lab_size[0] + 2:-2]:
            line = line.split(" ")
            self.treasures.append(Treasure((int(line[0]) + 1, int(line[1]) + 1), int(line[2]), int(line[3])))

        self.initial_pos = self.source_file[-2].split()
        self.initial_pos = tuple([int(elem) + 1 for elem in self.initial_pos])
        self.destination = self.source_file[-1].split()
        self.destination = tuple([int(elem) + 1 for elem in self.destination])

    def possible_paths(self):
        possible_positions_paths = []
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

                    if current_position not in [(current_path[-1][0]-1, current_path[-1][1]),
                                                (current_path[-1][0]+1, current_path[-1][1]),
                                                (current_path[-1][0], current_path[-1][1]+1),
                                                (current_path[-1][0], current_path[-1][1]-1)]:
                        current_path.pop()

                    if current_position == destination:
                        current_path.append(destination)
                        possible_positions_paths.append(current_path)

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

                return do_step

            do_first_step = enclosing_step(pos, labyrinth_matrix, path)
            do_first_step()

        step(initial_position, temp_labyrinth)  # Builds the possible_positions_paths

        for path in possible_positions_paths:
            possible_paths.append(Path(path, self))

        return possible_paths


def path_option(option, labyrinth):
    """
    :type option: int
    :type labyrinth: Labyrinth
    """
    possible_paths = labyrinth.possible_paths()

    # Shortest path
    if option == 1:
        shortest_dist = min([len(elem.path) for elem in possible_paths])
        index = [len(elem.path) for elem in possible_paths].index(shortest_dist)
        return possible_paths[index]
    # Longest path
    elif option == 2:
        longest_dist = max([len(elem.path) for elem in possible_paths])
        index = [len(elem.path) for elem in possible_paths].index(longest_dist)
        return possible_paths[index]
    # Most valuable path
    elif option == 3:
        most_valuable = max([elem.total_value for elem in possible_paths])
        index = [elem.total_value for elem in possible_paths].index(most_valuable)
        return possible_paths[index]
    elif option == 4:
        fastest = min([elem.duration for elem in possible_paths])
        index = [elem.duration for elem in possible_paths].index(fastest)
        return possible_paths[index]
    else:
        print('Invalid option')


def aux_print(temp, to_print):
    """
    This function prints the parameters in the terminal and in a file if needed
    :type temp: TextIO
    :type to_print:  Any
    """
    if temp:
        temp.write(to_print)
    print(to_print, end='')


try:
    exit_file = open(sys.argv[3], 'w+')
except IndexError:
    exit_file = False

a = Labyrinth(sys.argv[1])
chosen_path = path_option(int(sys.argv[2]), a)
aux_print(exit_file, str(len(chosen_path.path)) + ' ' + str(chosen_path.duration) + '\n')
for p in chosen_path.path:
    aux_print(exit_file, str(p[0] - 1) + ' ' + str(p[1] - 1) + '\n')
aux_print(exit_file, str(len(chosen_path.inventory)) + ' ' + str(chosen_path.total_value) + ' ' +
          str(chosen_path.total_weight) + '\n')
for i in chosen_path.inventory:
    aux_print(exit_file, str(i.pos[0] - 1) + ' ' + str(i.pos[1] - 1) + '\n')
