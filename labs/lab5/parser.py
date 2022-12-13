from grammar import Grammar
from node import Node


class Parser:
    def __init__(self, grammar_file: str, sequence_file: str, out_file: str):
        self.__grammar = Grammar(grammar_file)
        self.__sequence = self.__read_sequence(sequence_file)
        self.__output_file = out_file
        self.__init_output_file()
        print(self.__sequence)
        print(self.__grammar.grammar)

        # alpha - working stack, stores the way the parse is build
        self.__working_stack = []

        # beta - input stack
        self.__input_stack = [self.__grammar.starting_symbol]  # ['a', 'S', 'b', 'S', 'b', 'S']

        # s: q - normal state, b - back state, f - final state, e - error state
        self.__state = "q"

        # i - position of current symbol in input sequence
        self.__index = 0

        # representation - parsing tree
        self.__tree = list()

        self.__parser_out = ParserOutput(self)

    @property
    def state(self):
        return self.__state

    @property
    def working_stack(self):
        return self.__working_stack

    @property
    def tree(self):
        return self.__tree

    @staticmethod
    def __read_sequence(sequence_file: str) -> list:
        """
        reads the input sequence from a file
        :param sequence_file: the input file
        :return: the sequence
        """""
        sequence = list()
        with open(sequence_file, 'r') as f:
            if sequence_file == 'pif.out':
                pass
            else:
                line = f.readline()
                while line:
                    sequence.append(line[0:-1])
                    line = f.readline()

        return sequence

    def __init_output_file(self):
        """
        creates the output file
        :return: -
        """
        file = open(self.__output_file, 'a')
        file.write('')
        file.close()

    def write_in_output_file(self, text: str):
        """
        writes in the output file
        :param text: the message to be written
        :return: -
        """
        with open(self.__output_file, 'a') as f:
            f.write(text)

    def expand(self):
        """
        head of input stack os a non-terminal
        (q, i, alpha, A beta) ⊢ (q, i, alpha A1, gamma1 beta)
        :return: -
        """
        print('<-----> EXPAND <----->')
        self.write_in_output_file('<-----> EXPAND <----->')
        non_terminal = self.__input_stack.pop(0)  # pop A from beta
        self.__working_stack.append((non_terminal, 0))  # alpha -> alpha A1
        new_production = list(self.__grammar.get_productions_for_non_terminal(non_terminal)[0])
        self.__input_stack = new_production + self.__input_stack

    def advance(self):
        """
        head of input stack is a terminal which is the current symbol from the input sequence
        (q, i, alpha, a_i beta) ⊢ (q, i + 1, alpha a_i, beta)
        :return: -
        """
        print('<-----> ADVANCE <----->')
        self.write_in_output_file('<-----> ADVANCE <----->')
        self.__working_stack.append(self.__input_stack.pop(0))  # pop a_i from beta and add to alpha
        self.__index += 1

    def momentary_insuccess(self):
        """
        head of input stack is a terminal which is not the current symbol from the input sequence
        (q, i, alpha, beta) ⊢ (b, i, alpha, beta)
        :return: -
        """
        print('<-----> MOMENTARY INSUCCESS <----->')
        self.write_in_output_file('<-----> MOMENTARY INSUCCESS <----->')
        self.__state = 'b'

    def another_try(self):
        """
        head of input stack is a terminal which is not the current symbol from the input sequence
            and other productions are available
        (b, i, alpha A1, gamma1 beta) ⊢ (q, i, alpha A2, gamma2 beta)
        :return:
        """
        print('<-----> ANOTHER TRY <----->')
        self.write_in_output_file('<-----> ANOTHER TRY <----->')

        last_production = self.__working_stack.pop()  # tuple of non-terminal and production number
        if last_production[1] + 1 < len(self.__grammar.get_productions_for_non_terminal(last_production[0])):
            self.__state = 'q'
            # put the next production of the non-terminal in the working stack
            new_production = (last_production[0], last_production[1] + 1)
            self.__working_stack.append(new_production)

            # remove the old production from the input stack
            len_old_production = len(
                self.__grammar.get_productions_for_non_terminal(last_production[0])[last_production[1]])
            self.__input_stack = self.__input_stack[len_old_production:]

            # put the new production in the input stack
            new_production_out = list(self.__grammar.get_productions_for_non_terminal(new_production[0])[new_production[1]])
            self.__input_stack = new_production_out + self.__input_stack

        elif self.__index == 0 and last_production[0] == self.__grammar.starting_symbol:
            print(self.__index)
            self.__state = 'e'

        else:
            # change the production on the top of the input stack
            len_old_production = len(
                self.__grammar.get_productions_for_non_terminal(last_production[0])[last_production[1]])
            self.__input_stack = self.__input_stack[len_old_production:]
            self.__input_stack = [last_production[0]] + self.__input_stack

    def back(self):
        """
        head of input stack is a terminal which is not the current symbol from the input sequence
            and no other productions are available
        (b, i, alpha a, beta) ⊢ (b, i-1, alpha, a beta)
        :return: -
        """
        print('<-----> BACK <----->')
        self.write_in_output_file('<-----> BACK <----->')
        terminal = self.__working_stack.pop()
        self.__input_stack = [terminal] + self.__input_stack
        self.__index -= 1

    def success(self):
        """
        input stack is empty and the working stack contains the input sequence
        :return: -
        """
        print('<-----> SUCCESS <----->')
        self.write_in_output_file('<-----> SUCCESS <----->')
        self.__state = 'f'

    def print_working_stack(self):
        """
        prints to the screen and writes in the output file the contents of the working stack
        :return: -
        """
        print(self.__working_stack)
        self.write_in_output_file(str(self.__working_stack))

    def compute_parsing_tree(self):
        """
        computes the parsing tree based on the final working stack
        :return: -
        """
        for index in range(len(self.__working_stack)):
            # iterate the working stack
            if type(self.__working_stack[index]) == tuple:
                self.__tree.append(Node(self.__working_stack[index][0]))  # non-terminal
                self.__tree[index].production = self.__working_stack[index][1]  # production number
            else:
                self.__tree.append(Node(self.__working_stack[index]))  # terminal

        father = -1
        for index in range(len(self.__working_stack)):
            if type(self.__working_stack[index]) == tuple:
                self.__tree[index].father = father
                father = index
                # compute the length of the production of a non-terminal
                len_productions = len(
                    self.__grammar.productions[self.__working_stack[index][0]][self.__working_stack[index][1]])
                vector_index = list()
                for i in range(1, len_productions + 1):
                    vector_index.append(index + 1)
                for i in range(len_productions):
                    if self.__tree[vector_index[i]].production != -1:
                        offset = self.__get_length_depth(vector_index[i])
                        for j in range(i + 1, len_productions):
                            vector_index[j] += offset
                for i in range(0, len_productions - 1):
                    self.__tree[vector_index[i]].sibling = vector_index[i + 1]
            else:
                self.__tree[index].father = father
                father = -1

    def __get_length_depth(self, index: int) -> int:
        production = self.__grammar.productions[self.__working_stack[index][0]][self.__working_stack[index][1]]
        len_of_production = len(production)
        sum = len_of_production
        for i in range(1, len_of_production + 1):
            if type(self.__working_stack[index + 1]) == tuple:
                sum += self.__get_length_depth(index + 1)

        return sum

    def run(self):
        while self.__state not in ['f', 'e']:
            self.__write_all_data()
            if self.__state == 'q':
                if len(self.__input_stack) == 0 and self.__index == len(self.__sequence):
                    self.success()
                elif len(self.__input_stack) == 0:
                    self.momentary_insuccess()
                elif self.__input_stack[0] in self.__grammar.non_terminals:
                    self.expand()
                elif self.__index < len(self.__sequence) and self.__input_stack[0] == self.__sequence[self.__index]:
                    self.advance()
                else:
                    self.momentary_insuccess()

            elif self.__state == 'b':
                if self.__working_stack[-1] in self.__grammar.terminals:
                    self.back()
                else:
                    self.another_try()

        if self.__state == 'e':
            message = 'error occurred at index ' + str(self.__index)
        else:
            message = 'input sequence is accepted'
            self.print_working_stack()

        print(message)
        self.write_in_output_file(message + '\n----- END ------\n')
        self.compute_parsing_tree()
        self.__parser_out.write_parsing_tree()

    def __write_all_data(self):
        with open(self.__output_file, 'a') as f:
            f.write(str(self.__state) + ' ')
            f.write(str(self.__index) + '\n')
            f.write(str(self.__working_stack) + '\n')
            f.write(str(self.__input_stack) + '\n')


class ParserOutput:
    def __init__(self, parser: Parser):
        self.__parser = parser

    def write_parsing_tree(self):
        """
        writes the parsing tree in a readable format in the output file and command line
        :return: -
        """
        if self.__parser.state != 'e':
            self.__parser.write_in_output_file('\n<-----> PARSING TREE <----->\n')
            self.__parser.write_in_output_file('INDEX INFO PARENT LEFT_SIBLING\n')
            for index in range(len(self.__parser.working_stack)):
                msg = str(index) + ' ' + str(self.__parser.tree[index])
                self.__parser.write_in_output_file(msg + '\n')


if __name__ == '__main__':
    parser = Parser("grammar2.txt", "seq.in", "out.txt")
    parser.run()
