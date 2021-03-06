class Entry():
    def __init__(self, identifier):
        self.identifier = identifier

class SymbolTable():
    def __init__(self):
        self.m = 1000
        self.slla = []
        for i in range(self.m):
            self.slla.append([])

    def toAscii(self, str):
        res = 0
        for i in str:
            res += ord(i)
        return res

    def hash(self, entry):
        return self.toAscii(entry.identifier) % self.m
            
    def add(self, identifier):
        entry = Entry(identifier)
        pos = self.hash(entry)
        for i in range(len(self.slla[pos])):
            if self.slla[pos][i].identifier == entry.identifier:
                return pos, i
        i = len(self.slla[pos])
        self.slla[pos].append(entry)
        return pos, i


