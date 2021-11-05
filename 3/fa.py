class Transition():
    def __init__(self, IS, tr, FS):
        self.IS = IS
        self.tr = tr
        self.FS = FS

    def __str__(self):
        return self.IS + '---' + self.tr + '-->' + self.FS

    def __repr__(self):
        return self.IS + '---' + self.tr + '-->' + self.FS


class FALoader():
    def __init__(self):
        self.initialState = ''
        self.states = []
        self.finalStates = []
        self.transitions = []
        self.alphabet = []

    def loadFromFile(self, filepath):
        file = open(filepath, 'r')
        lines = file.readlines()
        self.setAlphabet(lines[0])
        self.setStates(lines[1])
        self.setInitialState(lines[2])
        self.setFinalStates(lines[3])
        self.setTransitions(lines[4:])

    def setStates(self, line):
        self.states = line.strip('\n').split(' ')

    def setInitialState(self, line):
        self.initialState = line.strip('\n').strip()

    def setFinalStates(self, line):
        self.finalStates = line.strip('\n').split(' ')

    def setAlphabet(self, line):
        self.alphabet = line.strip('\n').split(' ')

    def setTransitions(self, lines):
        for line in lines:
            [IS, tr, FS] = line.strip('\n').split(' ')
            self.transitions.append(Transition(IS, tr, FS))

    def verifySequence(self, sequence):
        x = self.initialState
        for t in sequence:
            exist = False
            for transition in self.transitions:
                if transition.IS == x and transition.tr == t:
                    exist = True
                    y = transition.FS
            if not exist:
                return False
            x = y
        return True

    def showMenu(self):
        print('\033[93m' + "0: exit" + '\033[0m')
        print('\033[96m' + "1: display the alphabet" + '\033[0m')
        print('\033[96m' + "2: display the states" + '\033[0m')
        print('\033[96m' + "3: display the initial state" + '\033[0m')
        print('\033[96m' + "4: display the final states" + '\033[0m')
        print('\033[96m' + "5: display the transitions" + '\033[0m')
        print('\033[96m' + "6: for DFA verify sequence" + '\033[0m')

    def runMenu(self):
        self.showMenu()
        while True:
            command = input('\033[92m' + ">>>" + '\033[0m')
            if command == '0':
                return
            if command == '1':
                print(self.alphabet)
            if command == '2':
                print(self.states)
            if command == '3':
                print(self.initialState)
            if command == '4':
                print(self.finalStates)
            if command == '5':
                print(self.transitions)
            if command == '6':
                sequence = input('sequence: ')
                print(self.verifySequence(sequence))


if __name__ == '__main__':
    fa = FALoader()
    fa.loadFromFile('FA.in')
    fa.runMenu()