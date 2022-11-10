from Domain.FiniteAutomata import FiniteAutomata


def menu():
    print("1.Display set of all states")
    print("2.Display display set of input symbols")
    print("3.Display transitions")
    print("4.Display final states")
    print("5.Check DFA")


class UI:
    def __init__(self):
        self.finite_automata = FiniteAutomata.process_file('../finite_automata.in')

    def display_set_of_all_states(self):
        print(self.finite_automata.q)

    def display_set_of_input_symbols(self):
        print(self.finite_automata.e)

    def display_transitions(self):
        print(self.finite_automata.s)

    def display_initial_state(self):
        print(self.finite_automata.q0)

    def display_final_states(self):
        print(self.finite_automata.f)

    def check_if_dfa(self):
        print(self.finite_automata.is_dfa())

    def check_if_valid(self):
        print("Is valid") if self.finite_automata.validate() else print("Is not valid")

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

        print("Is DFA:")
        self.check_if_dfa()

        self.check_if_valid()

        print("Check if sequence is valid: ")
        input_sequence = input()
        print(self.finite_automata.is_accepted(input_sequence))


ui = UI()
ui.run()
