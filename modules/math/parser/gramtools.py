import json


# template grammar class
class Grammar:
    def __init__(self):
        self.terminals = []
        self.nonterminals = []
        self.productions = {}
        self.start_symbol = ""


# reads data in from json and converts it to a grammar obj
def build_grammar():
    # opens json file
    json_obj = json.loads(open('modules/math/parser/config/grammars.json').read())
    # sets up new grammar
    grammar = Grammar()
    # adds all left hand side to non-terminals
    grammar.nonterminals = [x for x in json_obj]
    # sets first item in non_terminals as ss
    grammar.start_symbol = next(iter(grammar.nonterminals))
    # sorts terminals and vertices and records terminals
    for key in json_obj:
        # gets the production
        item = json_obj[key]
        # generates production
        grammar.productions[key] = [x.split(" ") for x in item]
        # gets terminals
        terminals = []
        # if is terminals adds it
        for production in item:
            terminals += [x for x in production.split(" ") if x not in grammar.nonterminals]
        # gets rid of repeats
        for terminal in terminals:
            if terminal not in grammar.terminals:
                grammar.terminals.append(terminal)
    return grammar
