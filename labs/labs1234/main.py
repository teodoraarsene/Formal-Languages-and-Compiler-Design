import re

from Domain.ProgramInternalForm import ProgramInternalForm
from Domain.Scanner import Scanner
from Domain.SymbolTable import SymbolTable
from Domain.Symbols import read_file


class Main:

    def __init__(self, separators, operators, reserved_words):
        self.separators = separators
        self.operators = operators
        self.reserved_words = reserved_words
        self.symbol_table_id = SymbolTable(17)
        self.symbol_table_const = SymbolTable(17)
        self.program_internal_form = ProgramInternalForm()
        self.scanner = Scanner(separators, operators)

    def run(self):

        problem_file = "Problem1.txt"
        exception_message = ""

        with open(problem_file, 'r') as file:
            line_counter = 0
            for line in file:
                line_counter += 1
                tokens = self.scanner.tokenize(line.strip())
                extra = ''
                for i in range(len(tokens)):
                    if tokens[i] in reserved_words + separators + operators:
                        if tokens[i] == ' ':
                            continue
                        self.program_internal_form.add(tokens[i], ((reserved_words + separators + operators).index(tokens[i]), -1))
                    elif tokens[i] in self.scanner.cases and i < len(tokens) - 1:
                        if re.match("[1-9]", tokens[i + 1]):
                            self.program_internal_form.add(tokens[i][:-1], (-1, -1))
                            extra = tokens[i][-1]
                            continue
                        else:
                            exception_message += 'Lexical error at token ' + tokens[i] + ', at line ' + str(
                                line_counter) + "\n"
                    elif self.scanner.is_identifier(tokens[i]):
                        id = self.symbol_table_id.add(tokens[i])
                        self.program_internal_form.add("identifier", id)
                    elif self.scanner.is_constant(tokens[i]):
                        const = self.symbol_table_const.add(extra + tokens[i])
                        extra = ''
                        self.program_internal_form.add("const", const)
                    else:
                        exception_message += 'Program has an error at token ' + tokens[i] + ', at line ' + str(
                            line_counter) + "\n"

        with open('Symbol Table.out', 'w') as writer:
            writer.write('identifiers:\n' + str(self.symbol_table_id) + 'constants:\n' + str(self.symbol_table_const))

        with open('Program Internal Form.out', 'w') as writer:
            writer.write(str(self.program_internal_form))

        if exception_message == '':
            print("Program is lexically correct!")
        else:
            print(exception_message)


separators, operators, reserved_words = read_file()
# print(separators)
# print(operators)
# print(reserved_words)
main = Main(separators, operators, reserved_words)
main.run()
