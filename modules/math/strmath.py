import math

import modules.math.parser.lexer as lexer
import modules.math.parser.math_parser as parser
from modules.math.parser.ASTtools import Token

import modules.math.m_functions as m_functions


class Result:
    def __init__(self, tp, data):
        self.type = tp
        self.data = data


class ErrorData:
    def __init__(self, msg, tb):
        self.message = msg
        self.traceback = tb


class Cell:
    def __init__(self, func, params):
        self.name = func
        self.values = params


class Value:
    def __init__(self, val, data_type):
        self.val = val
        self.type = data_type


def unparse(ast):
    raw = []
    for item in ast.content:
        if isinstance(item, Token):
            raw.append(item)
        else:
            raw.append(unparse(item))
    return raw


def evaluate(expr):
    try:
        lx = lexer.Lexer()
        tokens = lx.lex(expr)
        p = parser.Parser(tokens)
        ast = p.parse()
        action_tree = build_action_tree(ast)
        try:
            result = execute_action_tree(action_tree)
        except ZeroDivisionError:
            raise Exception({'type': 'runtime', 'message': 'Unable to divide by zero.'})
        if not isinstance(result, complex):
            if result.is_integer():
                result = int(result)
            result = format(result, ',')
        else:
            result = format(result, ',')
            result = result.replace('j', 'i').replace('+0i', '')
            result = result.strip('(').strip(')')
        return Result('result', result)
    except Exception as e:
        content = e.args[0]
        if content['type'] == 'lex':
            return Result('error', ErrorData(content['message'], get_formatted_line(expr, content['info'])))
        elif content['type'] == 'syntax':
            info = content['info']
            if isinstance(info[1], list):
                info[1] = [x for x in info[1] if x != '$']
                er_message = get_formatted_line(expr, [info[0].value, info[0].ndx])
                er_message += '\n\nExpected or Missing: ' + ', '.join(info[1])
                return Result('error', ErrorData(content['message'], er_message))
            else:
                if info[1] == '$':
                    return Result('error', ErrorData('Expected End of Expression', ''))
                else:
                    er_message = get_formatted_line(expr, [info[0].value, info[0].ndx])
                    er_message += '\n\nExpected or Missing: ' + info[1]
                    return Result('error', ErrorData(content['message'], er_message))
        elif content['type'] == 'semantic':
            info = content['info']
            if isinstance(info, Token):
                return Result('error', ErrorData(content['message'], get_formatted_line(expr, [info.value, info.ndx])))
            else:
                raw = unparse(info)
                start = raw[0].ndx
                end = raw[-1].ndx + len(raw[-1].value)
                return Result('error', ErrorData(content['message'], get_formatted_line(expr, [' ' * (end - start), start])))
        elif content['type'] == 'runtime':
            return Result('error', ErrorData(content['message'], ''))


def execute_action_tree(action_tree):
    if isinstance(action_tree, Value):
        if action_tree.type == 'NUMBER':
            return float(action_tree.val)
        else:
            raw_val = float(str(action_tree.val)[:-1])
            return raw_val * 1j
    operations = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
        '-': lambda a, b: a - b,
        '/': lambda a, b: a / b,
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b,
        'sqrt': m_functions.sqrt,
        'sin': m_functions.sin,
        'cos': m_functions.cos,
        'tan': m_functions.tan,
        'asin': m_functions.asin,
        'acos': m_functions.acos,
        'atan': m_functions.atan,
        're': m_functions.real,
        'im': m_functions.imaginary,
        'abs': abs,
        'sinh': m_functions.sinh,
        'cosh': m_functions.cosh,
        'tanh': m_functions.tanh,
        'round': m_functions.roundf,
        'int': m_functions.intf,
        'asinh': m_functions.asinh,
        'acosh': m_functions.acosh,
        'atanh': m_functions.atanh,
        'deg': math.degrees,
        'rad': math.radians,
        'log': m_functions.log,
        'ln': m_functions.ln,
        'gamma': math.gamma,
        'gcf': m_functions.gcd,
        'lcm': m_functions.lcm,
        'neg': lambda x: -x
    }
    if len(action_tree.values) == 1:
        return operations[action_tree.name](execute_action_tree(action_tree.values[0]))
    elif len(action_tree.values) == 2:
        return operations[action_tree.name](execute_action_tree(action_tree.values[0]), execute_action_tree(action_tree.values[1]))


def get_formatted_line(text, token_info):
    lines = text.split('\n')
    pos = 0
    token_ndx = 0
    line = 0
    for item in lines:
        if token_info[1] > pos + len(lines[line]):
            pos += len(item)
            line += 1
        else:
            token_ndx = token_info[1] - pos
            break
    base = ' ' * token_ndx + '^' * len(token_info[0])
    return lines[line] + '\n' + base


def build_action_tree(ast):
    if ast.name == 'atom':
        return build_atom_tree(ast)
    current_layer = ast.content
    while current_layer[-1].name in ['n_term', 'n_factor', 'n_atom']:
        current_layer += current_layer.pop().content
    if ast.name == 'factor':
        if len(current_layer) > 1:
            operands = []
            for _ in range(0, 3):
                operands.append(current_layer.pop())
            action_tree = Cell(operands[1].type, [build_atom_tree(operands[2]), build_atom_tree(operands[0])])
            while len(current_layer) > 0:
                n_operands = []
                for _ in range(0, 2):
                    n_operands.append(current_layer.pop())
                action_tree = Cell(n_operands[0].type, [build_atom_tree(n_operands[1]), action_tree])
            return action_tree
        else:
            return build_atom_tree(current_layer[0])
    else:
        if len(current_layer) > 1:
            action_tree = Cell(current_layer[1].type, [build_action_tree(current_layer[0]), build_action_tree(current_layer[2])])
            current_layer = current_layer[3:]
            while len(current_layer) > 0:
                action_tree = Cell(current_layer[0].type, [action_tree, build_action_tree(current_layer[1])])
                current_layer = current_layer[2:]
            return action_tree
        else:
            return build_action_tree(current_layer[0])


def build_atom_tree(atom):
    if atom.content[0].name == 'neg':
        return Cell('neg', [build_base_tree(atom.content[1])])
    else:
        return build_base_tree(atom.content[0])


def build_base_tree(base):
    if len(base.content) > 1:
        if base.content[0].type == '(':
            return build_action_tree(base.content[1])
        elif base.content[0].type == '|':
            return Cell('abs', [build_action_tree(base.content[1])])
        else:
            if base.content[0].value not in functions:
                raise Exception({'type': 'semantic', 'message': 'Undefined Function', 'info': base.content[0]})
            params = get_param_list(base.content[1])
            p_count = functions[base.content[0].value]
            if isinstance(p_count, list):
                if len(params) not in p_count:
                    raise Exception({'type': 'semantic', 'message': 'Invalid Parameters', 'info': base.content[1]})
            elif len(params) != p_count:
                raise Exception({'type': 'semantic', 'message': 'Invalid Parameters', 'info': base.content[1]})
            return Cell(base.content[0].value, params)
    else:
        if base.content[0].type in ['COMPLEX', 'NUMBER']:
            return Value(base.content[0].value, base.content[0].type)
        else:
            if base.content[0].value not in constants:
                raise Exception({'type': 'semantic', 'message': 'Undefined Constant', 'info': base.content[0]})
            if base.content[0].value == 'i':
                return Value(1j, 'COMPLEX')
            else:
                return Value(constants[base.content[0].value], 'NUMBER')


def get_param_list(trailer):
    if len(trailer.content) < 4:
        return [build_action_tree(trailer.content[1])]
    else:
        n_param = trailer.content[2]
        params = [build_action_tree(trailer.content[1]), build_action_tree(n_param.content[1])]
        while n_param.content[-1].name == 'n_param':
            params.append(build_action_tree(n_param.content[1]))
            n_param = n_param.content[-1]
        return params


functions = {
    'sin': 1,
    'asin': 1,
    'cos': 1,
    'acos': 1,
    'tan': 1,
    'atan': 1,
    'sinh': 1,
    'asinh': 1,
    'cosh': 1,
    'acosh': 1,
    'tanh': 1,
    'atanh': 1,
    'deg': 1,
    'rad': 1,
    'sqrt': 1,
    'round': [1, 2],
    'int': 1,
    'ln': 1,
    'log': [1, 2],
    'gcf': 2,
    'lcm': 2,
    'gamma': 1,
    're': 1,
    'im': 1
}

constants = {
    'e': math.e,
    'pi': math.pi,
    'tau': math.tau,
    'true': 1,
    'false': 0,
    'i': 1j
}


