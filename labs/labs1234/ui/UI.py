from Domain.FiniteAutomata import FiniteAutomata


def menu():
    print("1.Display set of all states")
    print("2.Display display set of input symbols")
    print("3.Display transitions")
    print("4.Display final states")
    print("5.Check DFA int const")
    print("6.Check DFA identifiers")


class UI:
    def __init__(self):
        self.finite_automata_int_const = FiniteAutomata.process_file('../finite_automata_int_const.in')
        self.finite_automata_identifiers = FiniteAutomata.process_file('../finite_automata_identifiers.in')

    def display_set_of_all_states(self):
        print('int const:\n', self.finite_automata_int_const.q)
        print('---------')
        print('identifiers:\n', self.finite_automata_identifiers.q)

    def display_set_of_input_symbols(self):
        print('int const:\n', self.finite_automata_int_const.e)
        print('---------')
        print('identifiers:\n', self.finite_automata_identifiers.e)

    def display_transitions(self):
        print('int const:\n', self.finite_automata_int_const.s)
        print('---------')
        print('identifiers:\n', self.finite_automata_identifiers.s)

    def display_initial_state(self):
        print('int const:\n', self.finite_automata_int_const.q0)
        print('---------')
        print('identifiers:\n', self.finite_automata_identifiers.q0)

    def display_final_states(self):
        print('int const:\n', self.finite_automata_int_const.f)
        print('---------')
        print('identifiers:\n', self.finite_automata_identifiers.f)

    def check_if_dfa_int_const(self):
        print('---------')
        print('int const:\n', self.finite_automata_int_const.is_dfa())

    def check_if_dfa_identifiers(self):
        print('identifiers:\n', self.finite_automata_identifiers.is_dfa())

    def check_if_valid_int_const(self):
        print('---------')

        print("int const:\nIs valid") if self.finite_automata_int_const.validate() else print("Is not valid")

    def check_if_valid_identifiers(self):
        print("identifiers:\nIs valid") if self.finite_automata_identifiers.validate() else print("Is not valid")

    def run(self):
        print("Set of all states:")
        self.display_set_of_all_states()

        print("Set of input symbols:")
        self.display_set_of_input_symbols()

        print("Transitions:")
        self.display_transitions()

        print("Initial state:")
        self.display_initial_state()

        print("Final states:")
        self.display_final_states()

        print("Is DFA int const:")
        self.check_if_dfa_int_const()

        print("Is DFA identifiers:")
        self.check_if_dfa_identifiers()

        self.check_if_valid_int_const()
        self.check_if_valid_identifiers()

        print("Check if int const sequence is valid: ")
        input_sequence = input()
        print(self.finite_automata_int_const.is_accepted(input_sequence))

        print("Check if identifier sequence is valid: ")
        input_sequence = input()
        print(self.finite_automata_identifiers.is_accepted(input_sequence))


ui = UI()
ui.run()
