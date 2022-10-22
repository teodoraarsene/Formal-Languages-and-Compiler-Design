import re
from HashTable import HashTable

PROGRAM_PATH = '../lab1a/ex1.txt'
TOKENS_PATH = '../lab1b/token.in'


class Parser:
    def __init__(self, exercise_path=PROGRAM_PATH, token_path=TOKENS_PATH):
        self.exercise_path = exercise_path
        self.token_path = token_path

        self.token_list = []
        self.reserved_tokens = []
        self.constants = HashTable()
        self.identifiers = HashTable()

    def parse(self):
        self._load_exercise()
        self._load_reserved_tokens()
        self._build_hash_table()

    def _load_exercise(self):
        with open(self.exercise_path, 'r') as f:
            text = f.read()

        tokens = re.split('(\s|\(|\)|{|}|[|]|"|and|or|<=|>=|==|=)', text)
        tokens = list(filter(''.__ne__, tokens))
        tokens = list(filter(' '.__ne__, tokens))
        tokens = list(filter('\n'.__ne__, tokens))
        self.token_list = list(filter('\t'.__ne__, tokens))

    def _load_reserved_tokens(self):
        with open(self.token_path, 'r') as f:
            self.reserved_tokens = f.read().split('\n')

    @staticmethod
    def is_identifier(name):
        identifier_regex = "^[a-zA-Z]([a-zA-Z][0-9])*$"
        if re.search(identifier_regex, name) is None:
            return False
        else:
            return True

    def _build_hash_table(self):
        for token in self.token_list:
            if token not in self.reserved_tokens:
                if self.is_identifier(token):
                    self.identifiers.add(token)
                else:
                    self.constants.add(token)


if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    print(parser.token_list)
    print('\n=======================\n')
    print(parser.reserved_tokens)
    print('\n=======================\n')
    print(parser.identifiers)
    print('\n=======================\n')
    print(parser.constants)
