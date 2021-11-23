from State import State, StateType
from grammar import Grammar
from tree import TreeNode
from tabulate import tabulate

class RDParser:
    def __init__(self, grammar, w):
        self.grammar = grammar
        self.input = w

    def get_next_production(self, prod, productions):
        for i in range(len(productions)):
                if prod == productions[i] and i + 1 < len(productions):
                    return productions[i+1]
        return None

    def expand(self, config):
        #print(config)
        nonterminal = config.input_stack[0]
        first_production = self.grammar.productions[nonterminal][0].split()
        config.work_stack.append((nonterminal, 0))
        config.input_stack = first_production + config.input_stack[1:]
        #print(config)

    def advance(self, config):
        #print(config)
        terminal = config.input_stack[0]
        config.index += 1
        config.work_stack.append(terminal)
        config.input_stack = config.input_stack[1:]
        #print(config)

    def momentary_insuccess(self, config):
        config.type = StateType.BACK

    def back(self, config):
        #print(config)
        terminal = config.work_stack[-1]
        config.index -= 1
        config.work_stack.pop()
        config.input_stack = [terminal] + config.input_stack
        #print(config)

    def another_try(self, config):
        #print(config)
        (nonterminal, last_production_index) = config.work_stack.pop()
        last_production = self.grammar.productions[nonterminal][last_production_index]
        len_last_production = len(last_production.split())
        next_production = self.get_next_production(last_production, self.grammar.productions[nonterminal])
        if next_production:
            config.type = StateType.NORMAL
            config.work_stack.append((nonterminal, last_production_index + 1))
            next_production = next_production.split()
            config.input_stack = next_production + config.input_stack[len_last_production:]
        elif config.index == 0 and nonterminal == self.grammar.start:
            config.type = StateType.ERROR
        else:
            config.input_stack = [nonterminal] + config.input_stack[len_last_production:]
        #print(config)

    def success(self, config):
        config.type = StateType.FINAL

    def construct_parse_tree(self, workStack):
        currentIndex = 1
        firstNode = TreeNode(currentIndex, self.grammar.start, 0, 0)
        treeNodes = [firstNode]
        for elem in workStack:
            if elem[0] not in self.grammar.productions:
                currentIndex += 1
                continue
            elem = (elem[0], self.grammar.productions[elem[0]][elem[1]].split())
            if type(elem) is tuple and elem[0] in self.grammar.nonterminals:
                for symbol in range(len(elem[1])):
                    rightSibling = 0
                    if symbol > 0:
                        rightSibling = treeNodes[-1].index
                    treeNodes.append(TreeNode(len(treeNodes) + 1, elem[1][symbol], currentIndex, rightSibling))
            currentIndex += 1

        self.tree = [node.toList() for node in treeNodes]

    def recursive_descendent(self):
        config = State(self.grammar.start)
        while config.type != StateType.FINAL and config.type != StateType.ERROR:
            #print(config)
            if config.type == StateType.NORMAL:
                if config.index == len(self.input) and len(config.input_stack) == 0:
                    self.success(config)
                else:
                    if config.input_stack[0] in self.grammar.nonterminals:
                        self.expand(config)
                    else:
                        if config.index < len(self.input) and config.input_stack[0] == self.input[config.index]:
                            self.advance(config)
                        else:
                            self.momentary_insuccess(config)
            else:
                if config.type == StateType.BACK:
                    if config.work_stack[-1] in self.grammar.terminals:
                        self.back(config)
                    else:
                        self.another_try(config)

        if config.type == StateType.ERROR:
            return False, []
        else:
            return True, self.construct_parse_tree(config.work_stack)
                            

def read_input(filename):
    file_input = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        tokens = line.split()
        file_input += tokens
    #print(file_input)
    return file_input

if __name__ == '__main__':
    #grammar = Grammar.readFromFile('g1.txt')
    #rdp = RDParser(grammar, list("aacbc"))
    grammar = Grammar.readFromFile('g2.txt')
    rdp = RDParser(grammar, read_input('input.txt'))
    isValid, seq = rdp.recursive_descendent()

    if isValid:
        print("Sequence is valid")
        print(tabulate(rdp.tree, numalign='center', tablefmt="pretty", headers=['Index', 'Info', 'Parent', 'Left Sibling']))
    else:
        print("Sequence is not valid")
