from grammar import Grammar

if __name__ == '__main__':
    grammar2_filename = 'grammar2.txt'
    grammar2 = Grammar(grammar2_filename)
    # print(grammar2.get_grammar())
    for key in grammar2.grammar:
        print(key, ' : ', grammar2.grammar[key])
