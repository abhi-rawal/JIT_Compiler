from lark import Lark, Transformer

# Define the path to the grammar file
grammar_path = "grammer.lark"  # Make sure grammar.lark is in the same folder

with open(grammar_path, "r") as f:
    grammar = f.read()

parser = Lark(grammar, parser='lalr')

def parse_code(code):
    tree = parser.parse(code)
    return ASTBuilder().transform(tree)

class ASTBuilder(Transformer):
    def assign(self, items):
        return ('assign', str(items[0]), items[1])

    def print_stmt(self, items):
        return ('print', items[0])

    def while_stmt(self, items):
        condition = items[0]
        body = items[1:]
        return ('while', condition, body)

    def gt(self, _): return '>'
    def lt(self, _): return '<'
    def eq(self, _): return '=='
    def neq(self, _): return '!='

    def condition(self, items):
        return ('condition', items[0], items[1], items[2])

    def var(self, items):
        return ('var', str(items[0]))

    def number(self, items):
        return float(items[0])

    def add(self, items): return ('add', items[0], items[1])
    def sub(self, items): return ('sub', items[0], items[1])
    def mul(self, items): return ('mul', items[0], items[1])
    def div(self, items): return ('div', items[0], items[1])
    def neg(self, items): return ('neg', items[0])
