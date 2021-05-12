from importlib._common import _

from sly import Lexer
from sly import Parser

class BasicLexer(Lexer):
    tokens = { VAR, NUMBER, STRING }
    ignore = '\t '
    literals = {'T', 'J', 'Z', 'O', 'S', 'L', 'I', '.', '='}

    # Every variable must start with a T
    VAR = r'[T][T|J|Z|O|S|L|I]+'
    STRING = r'\".*?\"'

    # Every number must start with an I
    # An I with nothing following it could be a 0
    @_(r'[I][T|J|Z|O|S|L|I]*')
    def NUMBER(self, t):
        num_dict = {'T': 1, 'J': 5, 'Z': 10, 'O': 50, 'S': 100, 'L': 500, 'I': 1000}

        # The [1:] removes the first I
        num_list = t.value
        #print(type(num_list))
        #value = num_list

        # for x in range(0, len(num_list)-1):
        #     if num_dict[num_list[x]] >= num_dict[num_list[x+1]]:
        #         value += num_dict[num_list[x]]
        #     else:
        #         value -= num_dict[num_list[x]]

        return 3
    # Comment token
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newline token(used only for showing
    # errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class BasicParser(Parser):
    #tokens are passed from lexer to parser
    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('VAR "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.expr)

    @_('VAR "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.VAR, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('VAR')
    def expr(self, p):
        return ('var', p.VAR)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    print('GFG Language')
    env = {}

    while True:

        try:
            text = input('GFG Language > ')

        except EOFError:
            break

        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env)


