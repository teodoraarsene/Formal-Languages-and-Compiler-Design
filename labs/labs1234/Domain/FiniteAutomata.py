from __future__ import annotations


class FiniteAutomata:

    def __init__(self, set_of_all_states, set_of_input_symbols, initial_state, set_of_final_states, transitions):
        self.q = set_of_all_states
        self.e = set_of_input_symbols
        self.q0 = initial_state
        self.f = set_of_final_states
        self.s = transitions

    def is_accepted(self, input_sequence) -> bool:
        if self.is_dfa():
            current_state = self.q0

            for symbol in input_sequence:
                if (current_state, symbol) in self.s.keys():
                    current_state = self.s[(current_state, symbol)][0]
                else:
                    return False

            if current_state in self.f:
                return True

        return False

    def validate(self) -> bool:
        if self.q0 not in self.q:
            return False

        for final_state in self.f:
            if final_state not in self.q:
                return False

        for key in self.s.keys():
            state = key[0]
            symbol = key[1]

            if state not in self.q:
                return False

            if symbol not in self.e:
                return False

            for resulting_state in self.s[key]:
                if resulting_state not in self.q:
                    return False
        return True

    def is_dfa(self) -> bool:
        unique_keys = set(self.s.keys())
        for key in unique_keys:
            if len(self.s[key]) > 1:
                return False
        return True

    @staticmethod
    def get_line(line) -> str:
        return line.strip().split(' ')[2:]

    @staticmethod
    def process_file(file_name) -> FiniteAutomata:
        with open(file_name) as file:
            q = FiniteAutomata.get_line(file.readline())
            e = FiniteAutomata.get_line(file.readline())
            q0 = FiniteAutomata.get_line(file.readline())[0]
            f = FiniteAutomata.get_line(file.readline())

            s = {}
            file.readline()
            for line in file:
                source_state = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[0]
                value = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[1]
                destination_state = line.strip().split('->')[1].strip()

                if (source_state, value) in s.keys():
                    s[(source_state, value)].append(destination_state)
                else:
                    s[(source_state, value)] = [destination_state]

            return FiniteAutomata(q, e, q0, f, s)
