class Grammar:
    def __init__(self, input_filename: str):
        self.__filename = input_filename
        self.__grammar = self.__read_grammar()
        self.__set_of_non_terminals = self.__grammar['non_terminals']
        self.__set_of_terminals = self.__grammar['terminals']
        self.__starting_symbol = self.__grammar['starting_symbol']
        self.__productions = self.__grammar['productions']

    @property
    def grammar(self) -> dict:
        return self.__grammar

    @property
    def non_terminals(self) -> list:
        return self.__set_of_non_terminals

    @property
    def terminals(self) -> list:
        return self.__set_of_terminals

    @property
    def starting_symbol(self) -> str:
        return self.__starting_symbol

    @property
    def productions(self) -> dict:
        return self.__productions

    def __read_grammar(self) -> dict:
        grammar = dict()
        with open(self.__filename) as file:
            # non terminals
            line = file.readline()
            grammar['non_terminals'] = line.strip().split()
            # terminals
            line = file.readline()
            grammar['terminals'] = line.strip().split()
            # starting symbol
            line = file.readline()
            grammar['starting_symbol'] = line.strip()
            # productions
            grammar['productions'] = dict()
            line = file.readline()
            while line:
                line = line.strip().split('->')
                left_hand_side = line[0].strip()
                right_hand_side = line[1].strip().split('|')
                grammar['productions'][left_hand_side] = list()
                for production in right_hand_side:
                    grammar['productions'][left_hand_side].append(production.strip())
                line = file.readline()

            return grammar

    def get_productions_for_non_terminal(self, symbol: str) -> list:
        return self.__productions[symbol]
