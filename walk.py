import sys


class Treasure:

    def __init__(self, pos, value, weight):
        self.pos = pos
        self.value = value
        self.weight = weight


class Walk:

    def __init__(self, source_file, option, exit_file=None):

        self.source_file = open(source_file, 'r').read().split('\n')
        self.option = option
        self.initial_pos = None
        self.destination = None
        self.labyrinth = []
        self.treasures = []

        # Creates an output file if needed
        if exit_file:
            self.exit_file = open(exit_file, 'w+')

        lab_size = int(self.source_file[0][0]), int(self.source_file[0][2])

        for line in self.source_file[1:lab_size[0] + 1]:
            self.labyrinth.append([True if elem == '.' else False for elem in line])
        for line in self.source_file[lab_size[0] + 2:-2]:
            line = line.split(" ")
            self.treasures.append(Treasure((int(line[0]), int(line[1])), int(line[2]), int(line[3])))

        self.initial_pos = int(self.source_file[-2][0]), int(self.source_file[-2][2])
        self.destination = int(self.source_file[-1][0]), int(self.source_file[-1][2])

    def aux_print(self, to_print):
        if self.exit_file:
            self.exit_file.write(to_print)
        print(to_print)

    def walk(self):
        if self.option == 1:
            # Todo shortest path
            pass
        elif self.option == 2:
            # Todo longest path
            pass
        elif self.option == 3:
            # Todo most valuable path
            pass
        elif self.option == 4:
            # Todo most fastest path
            pass
        else:
            print("Invalid option")


try:
    temp = sys.argv[3]
except IndexError:
    temp = None

a = Walk(sys.argv[1], sys.argv[2], temp)
a.walk()
