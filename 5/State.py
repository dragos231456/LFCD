class StateType:
    NORMAL = 'q'
    ERROR = 'e'
    BACK = 'b'
    FINAL = 'f'


class State:
    def __init__(self, start_sym):
        self.type = StateType.NORMAL
        self.index = 0
        self.work_stack = []
        self.input_stack = [start_sym]

    def __str__(self):
        return "STATE: {} {} {} {}".format(self.type, self.index, self.work_stack, self.input_stack)