import unittest

from RDParser import RDParser
from State import State, StateType
from grammar import Grammar


class MyTestCase(unittest.TestCase):
    def test_expand(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("acbc"))
        config = State(grammar.start)
        nonterminal = config.input_stack[0]
        self.assertIn(nonterminal, grammar.nonterminals)
        rdp.expand(config)
        self.assertTupleEqual((nonterminal, 0), config.work_stack[-1])
        first_production = grammar.productions[nonterminal][0].split()
        for i in range(len(first_production)):
            self.assertEqual(first_production[i], config.input_stack[i])

    def test_another_try_existing_next_production(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("aacbc"))
        config = State(grammar.start)
        rdp.expand(config)
        top = config.work_stack[-1]
        config.type = StateType.BACK
        rdp.another_try(config)
        self.assertEqual(config.work_stack[-1][1], top[1] + 1)
        actual_production = grammar.productions[top[0]][top[1]+1].split()
        self.assertEqual(config.type, StateType.NORMAL)
        for i in range(len(actual_production)):
            self.assertEqual(actual_production[i], config.input_stack[i])

    def test_another_try_error(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("aacbc"))
        config = State(grammar.start)
        rdp.expand(config)
        grammar.productions[grammar.start] = ['ba']
        self.assertEqual(config.index, 0)
        rdp.another_try(config)
        self.assertEqual(config.type, StateType.ERROR)

    def test_another_try_back(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("aacbc"))
        config = State(grammar.start)
        rdp.expand(config)
        grammar.productions[grammar.start] = ['ba']
        config.type = StateType.BACK
        config.index = 1
        rdp.another_try(config)
        self.assertEqual(grammar.start, config.input_stack[0])
        self.assertEqual(config.type, StateType.BACK)

    def test_advance(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("acbc"))
        config = State(grammar.start)
        rdp.expand(config)
        terminal = config.input_stack[0]
        previous_index = config.index
        previous_length = len(config.input_stack)
        self.assertIn(terminal, grammar.terminals)
        rdp.advance(config)
        self.assertEqual(previous_index+1, config.index)
        self.assertEqual(config.work_stack[-1], terminal)
        self.assertEqual(len(config.input_stack), previous_length-1)

    def test_momentary_insuccess(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("acbc"))
        config = State(grammar.start)
        rdp.momentary_insuccess(config)
        self.assertEqual(config.type, StateType.BACK)

    def test_back(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("acbc"))
        config = State(grammar.start)
        rdp.expand(config)
        rdp.advance(config)
        terminal = config.work_stack[-1]
        previous_index = config.index
        previous_length = len(config.work_stack)
        self.assertIn(terminal, grammar.terminals)
        rdp.back(config)
        self.assertEqual(previous_index-1, config.index)
        self.assertEqual(config.input_stack[0][0], terminal)
        self.assertEqual(len(config.work_stack), previous_length-1)

    def test_success(self):
        grammar = Grammar.readFromFile('g1.txt')
        rdp = RDParser(grammar, list("acbc"))
        config = State(grammar.start)
        rdp.success(config)
        self.assertEqual(config.type, StateType.FINAL)


if __name__ == '__main__':
    unittest.main()
