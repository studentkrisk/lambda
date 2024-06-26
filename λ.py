from string import whitespace

data = ""
with open("programs/nums.λ", "r") as f:
    data = f.read().split("\n")

# lexer
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return self.type + ": " + str(self.value)
class Lexer:
    def __init__(self, d):
        self.cur = 0
        self.d = d
        self.toks = []
    def next(self):
        while self.d[self.cur] in whitespace:
            self.cur += 1
        char = self.d[self.cur]
        self.cur += 1
        if char in "λ.()":
            return Token(char, None)
        else:
            return Token("SYMBOL", char)

#parser
class Function:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp
    def a_red(self, v1, v2):
        self.var.a_red(v1, v2)
        self.exp.a_red(v1, v2)
    def __repr__(self):
        return f"λ{self.var}.{self.exp}"
class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def a_red(self, v1, v2):
        self.left.a_red(v1, v2)
        self.right.a_red(v1, v2)
    def b_red(self):
        if type(self.left) == Var:
            pass
    def __repr__(self):
        return f"({self.left} {self.right})"
class Var:
    def __init__(self, name):
        self.name = name
    def a_red(self, v1, v2):
        if self.name == v1:
            self.name = v2
    def __repr__(self):
        return self.name
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        x = self.parse()
        print(x)
        x.a_red("p", "placeholder")
    def parse(self):
        new = self.lexer.next()
        if new.type == "λ":
            print(f"new function! {new}")
            return self.create_function()
        elif new.type == "(":
            print(f"new application! {new}")
            return self.create_application()
        else:
            print(f"new variable! {new}")
            return Var(new.value)
    def create_function(self):
        var = Var(self.lexer.next().value)
        self.lexer.next()
        return Function(var, self.parse())
    def create_application(self):
        left = self.parse()
        right = self.parse()
        self.lexer.next()
        return Application(left, right)


Parser(Lexer(data[0]))