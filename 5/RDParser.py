from State import State, StateType
from grammar import Grammar


class RDParser:
    def __init__(self, grammar, w):
        self.grammar = grammar
        self.input = w

    def __get_next_prod(self, prod, productions):
        for i in range(len(productions)):
                if prod == productions[i] and i + 1 < len(productions):
                    return productions[i+1]
        return None

    def recursive_descent_run(self):
        state = State(self.grammar.start)
        while state.type != StateType.FINAL and state.type != StateType.ERROR:
            print(state)
            if state.type == StateType.NORMAL:
                if len(state.input_stack) == 0 and state.index == len(self.input):
                    state.type = StateType.FINAL
                elif len(state.input_stack) == 0:
                    state.type = StateType.BACK
                else:
                    if state.input_stack[0] in self.grammar.nonterminals:
                        nonterminal = state.input_stack[0]
                        first_production = self.grammar.productions[nonterminal][0].split(' ')
                        state.work_stack.append((nonterminal, first_production))
                        state.input_stack = first_production + state.input_stack[1:]
                    else:
                        if state.index == len(self.input):
                            state.type = StateType.BACK
                        elif state.input_stack[0] == StateType.ERROR:
                            state.work_stack.append((StateType.ERROR, []))
                            state.input_stack = state.input_stack[1:]
                        elif state.input_stack[0] == self.input[state.index]:
                            state.index += 1
                            state.work_stack.append((state.input_stack[0], []))
                            state.input_stack = state.input_stack[1:]
                        else:
                            state.type = StateType.BACK
            else:
                if state.type == StateType.BACK:
                    if state.work_stack[-1][0] in self.grammar.terminals:
                        if state.work_stack[-1][0] == StateType.ERROR:
                            state.work_stack.pop(-1)
                        else:
                            state.index -= 1
                            terminal = state.work_stack.pop(-1)[0]
                            state.input_stack = [terminal] + state.input_stack
                    else:
                        (nonterminal, last_production) = state.work_stack[-1]
                        productions = self.grammar.productions[nonterminal]
                        next_prod = self.__get_next_prod(last_production, productions)
                        if next_prod:
                            next_prod = next_prod.split(' ')
                            state.type = StateType.NORMAL
                            state.work_stack.pop(-1)
                            state.work_stack.append((nonterminal, next_prod))
                            state.input_stack = next_prod + state.input_stack[len(last_production):]
                        elif state.index == 0 and nonterminal == self.grammar.start:
                            state.type = StateType.ERROR
                        else:
                            state.work_stack.pop(-1)
                            if nonterminal == [StateType.ERROR]:
                                state.input_stack = [nonterminal] + state.input_stack
                            else:
                                state.input_stack = [nonterminal] + state.input_stack[len(last_production):]

        if state.type == StateType.ERROR:
            return False, []
        return True


if __name__ == '__main__':
    grammar = Grammar.readFromFile('g2.txt')
    rdp = RDParser(grammar, [
        '{',
        'int',
        'a',
        ';',
        'int',
        'b',
        ';',
        'int',
        'c',
        ';',
        'read',
        '(',
        'a',
        ')',
        ';',
        'read',
        '(',
        'b',
        ')',
        ';',
        'read',
        '(',
        'c',
        ')',
        ';',
        'if',
        '(',
        'a',
        '>',
        'b',
        ')',
        '{',
        'print',
        '(',
        'a',
        ')',
        '}',
        '}'
    ])
    isValid = rdp.recursive_descent_run()
    print("Sequence is", isValid)