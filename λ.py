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
        if self.cur >= len(self.d):
            return Token("*", None) # EOF
        while self.d[self.cur] in whitespace:
            self.cur += 1
        char = self.d[self.cur]
        self.cur += 1
        print(char)
        if char in "λ.()":
            return Token(char, None)
        else:
            return Token("SYMBOL", char)
    def prev(self):
        self.cur -= 1
        while self.d[self.cur] in whitespace:
            self.cur -= 1

#parser
class Function:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp
    def a_red(self, v1, v2):
        return Function(self.var.a_red(v1, v2), self.exp.a_red(v1, v2))
    def b_red(self):
        print(self)
        return Function(self.var, self.exp.b_red())
    def __repr__(self):
        return f"λ{self.var}.{self.exp}"
class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def a_red(self, v1, v2):
        return Application(self.left.a_red(v1, v2), self.right.a_red(v1, v2))
    def b_red(self):
        print(self)
        if type(self.left) == Var:
            return Application(self.left.b_red(), self.right.b_red())
        l_func = self.left
        if type(self.left) == Application:
            l_func = self.left.b_red()
            if type(l_func) == Application:
                return l_func
        return l_func.exp.a_red(l_func.var, self.right.b_red()).b_red()
    def __repr__(self):
        return f"({self.left} {self.right})"
class Var:
    def __init__(self, name):
        self.name = name
    def a_red(self, v1, v2):
        if self.name == v1.name:
            return v2
        return self
    def b_red(self):
        return self
    def __repr__(self):
        return self.name
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        x = self.parse()
        print(x)
        x = x.b_red()
        print(x)
    def parse(self):
        new = self.lexer.next()
        if new.type == "λ":
            print(f"new function! {new}")
            return self.create_function()
        elif new.type == "(":
            print("new parenthesis!")
            x = self.parse()
            self.lexer.next()
            return x
        else:
            print(self.parse())

        # elif new.type == "(":
        #     print(f"new application! {new}")
        #     return self.create_application()
        # else:
        #     print(f"new variable! {new}")
        #     return Var(new.value)
    def create_function(self):
        var = Var(self.lexer.next().value)
        self.lexer.next()
        return Function(var, self.parse())
    def create_application(self):
        left = self.parse()
        right = self.parse()
        return Application(left, right)


Parser(Lexer(data[0]))