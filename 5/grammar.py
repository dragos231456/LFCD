class Grammar():
    def __init__(self, nonterminals, terminals, start, productions):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = start
        self.productions = productions

    @staticmethod
    def readFromFile(fileName):
        with open(fileName, "r") as file:
            nonTerminals = file.readline().strip().split()
            terminals = file.readline().strip().split()
            start = file.readline().strip()
            productions = {}

            for line in file:
                line = line.strip('\n')
                leftPart, rightPart = line.split('->')
                leftPart = leftPart.strip()
                rightPart = [part.strip() for part in rightPart.split('|')]

                if leftPart in productions.keys():
                    raise Exception('Corrupted file')

                productions[leftPart] = rightPart

        return Grammar(nonTerminals, terminals, start, productions)

    def printNonterminals(self):
        print('Nonterminals: ', self.nonterminals)

    def printTerminals(self):
        print('Terminals: ', self.terminals)

    def printProductions(self):
        print('Productions: ')
        for leftSide in self.productions:
            printProduction = ''
            for production in self.productions[leftSide]:
                printProduction += production + ' | '
            printProduction = printProduction[:-2]
            print(leftSide, '->', printProduction)

    def printProductionsForNonterminal(self, nonterminal):
        print('Production for ', nonterminal, ':', sep='')
        printProduction = ''
        for production in self.productions[nonterminal]:
            printProduction += production + ' | '
        printProduction = printProduction[:-2]
        print(nonterminal, '->', printProduction)

    def CFGcheck(self):
        for leftSide in self.productions.keys():
            if leftSide not in self.nonterminals:
                return False
        return True


if __name__ == '__main__':
    grammar = Grammar.readFromFile('g1.txt')
    print('Start:', grammar.start)
    grammar.printTerminals()
    grammar.printNonterminals()
    grammar.printProductions()
    grammar.printProductionsForNonterminal('A')
    print('CFG check: ' + str(grammar.CFGcheck()))
