# noinspection PyRedundantParentheses,PyAttributeOutsideInit
from symbolTable import SymbolTable
import re


class Scanner():
    def __init__(self, tokenFile):
        self.pifFile = open("PIF.out", 'w')
        self.errors = []
        self.tokens = []
        self.loadTokens(tokenFile)
        self.ST = SymbolTable()
        self.stFile = open("ST.out", 'w')

    def loadTokens(self, tokenFile):
        file = open(tokenFile, 'r')
        lines = file.readlines()
        for line in lines:
            self.tokens.append(line.strip())
        file.close()

    def isEmptyChar(self, char):
        return char == ' ' or char == '\n' or ord(char) == 9

    def expandLine(self, line):
        quotesOpen = False
        quoteOpen = False
        newLine = ''
        fbEqual = ['>', '<', '!', '=']
        repeated = ['|', '&', '^']
        for i in range(len(line)):
            addSpace = False
            newLine += line[i]
            if line[i] in fbEqual:
                if i + 1 < len(line) and line[i+1] != '=':
                    addSpace = True
            elif line[i] in repeated:
                if i + 1 < len(line) and line[i+1] != line[i]:
                    addSpace = True
            elif line[i] == "'":
                quoteOpen = not quoteOpen
                print(quoteOpen)
                addSpace = True
            elif line[i] == '"':
                quotesOpen = not quotesOpen
                addSpace = True
            elif not (line[i].isalpha() or line[i].isnumeric()):
                addSpace = True
            else:
                if i + 1 < len(line) and not (line[i+1].isalpha() or line[i+1].isnumeric()):
                    addSpace = True

            if addSpace and (not quotesOpen) and (not quoteOpen):
                newLine += ' '

        #print(newLine)
        return newLine

    def detectToken(self, line, index):
        token = ''
        isQuoteOpen = False
        isDoubleQuoteOpen = False
        while index < len(line) and self.isEmptyChar(line[index]):
            index += 1
        while index < len(line) and (not self.isEmptyChar(line[index]) or isQuoteOpen or isDoubleQuoteOpen):
            token += line[index]
            if line[index] == "'":
                isQuoteOpen = not isQuoteOpen
            if line[index] == '"':
                isDoubleQuoteOpen = not isDoubleQuoteOpen
            index += 1
        return [token, index]

    def writeToPIF(self, token, index):
        line = token + " " + str(index) + '\n'
        self.pifFile.write(line)

    def writeToST(self):
        i = 0
        for lst in self.ST.slla:
            j = 0
            for entry in lst:
                self.stFile.write(entry.identifier + " " + str([i, j]) + '\n')
                j += 1
            i += 1

    def identifierOrConstant(self, token):
        patterns = {"integer": r'[-+]?[0-9]+',
                    "float": r'[-+]?\d*\.\d+|\d+',
                    "string": r'".*?"',
                    "character": r"'.'",
                    "identifier": r'[a-z][a-zA-Z]*',
                    "bool": r'True|False'}

        for pattern in patterns.keys():
            x = re.findall(patterns[pattern], token)

            if len(x) != 0 and x[0] == token:
                if pattern == 'identifier':
                    return [True, pattern]
                else:
                    return [True, 'constant']
        return [False, '']

    def addError(self, token, lineIndex):
        self.errors.append("Line " + str(lineIndex) + ": Undefined token: " + token)

    def parse(self, line, lineIndex):
        index = 0
        while index < len(line):
            [token, index] = self.detectToken(line, index)

            if token == '':
                return

            if token in self.tokens:
                self.writeToPIF(token, 0)
            else:
                [isIDorC, type] = self.identifierOrConstant(token)
                if isIDorC:
                    stIndex = self.ST.add(token)
                    self.writeToPIF(type, stIndex)
                else:
                    self.addError(token, lineIndex)

    def scan(self, filename):
        file = open(filename, 'r')
        self.lines = file.readlines()
        file.close()

        lineIndex = 0
        for line in self.lines:
            lineIndex += 1
            expandedLine = self.expandLine(line)
            self.parse(expandedLine, lineIndex)

        self.writeToST()

        self.pifFile.close()
        self.stFile.close()

        if len(self.errors) == 0:
            print("Lexically correct")
        else:
            for error in self.errors:
                print(error)


if __name__ == '__main__':
    scanner = Scanner('token.txt')
    scanner.scan('p1err.txt')
