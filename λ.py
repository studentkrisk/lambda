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
        # print(char)
        if char in "λ.()":
            return Token(char, None)
        else:
            return Token("SYMBOL", char)
    def prev(self):
        self.cur -= 1
        while self.d[self.cur] in whitespace:
            self.cur -= 1

#parser
vars = {}
cur_var_num = 0
def get_name(x):
    while x.isnumeric():
        x = vars[x]
    return x
class Function:
    def __init__(self, var, exp):
        global cur_var_num
        cur_var_num += 1
        vars[str(cur_var_num)] = var.name
        self.var = var.a_red(var, Var(str(cur_var_num)))
        self.exp = exp.a_red(var, Var(str(cur_var_num)))
    def a_red(self, v1, v2):
        return Function(self.var.a_red(v1, v2), self.exp.a_red(v1, v2))
    def b_red(self):
        # print(self)
        x = Function(self.var, self.exp.b_red())
        # print(f"created function: {x}")
        return x
    def __repr__(self):
        return f"λ{get_name(self.var.name)}.{self.exp.a_red(self.var, Var(get_name(self.var.name)))}"
class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def a_red(self, v1, v2):
        return Application(self.left.a_red(v1, v2), self.right.a_red(v1, v2))
    def b_red(self):
        # print(self)
        if type(self.left) == Var:
            x = Application(self.left, self.right.b_red())
            # print(f"created application {x}")
            return x
        l_func = self.left.b_red()
        if type(l_func) == Application:
            x = Application(l_func, self.right)
            # print(f"created applciation {x}")
            return x
        x = l_func.exp.a_red(l_func.var, self.right).b_red()
        # print(f"created function {x}")
        return x
    def __repr__(self):
        return f"({self.left if type(self.left) != Var else get_name(self.left.name)} {self.right if type(self.right) != Var else get_name(self.right.name)})"
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
    def parse(self):
        new = self.lexer.next()
        if new.type == "λ":
            # print(f"new function! {new}")
            return self.create_function()
        elif new.type == "(":
            # print("new application!")
            x = self.create_application()
            return x
        else:
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

dict = {}
for var in data:
    var = var.split(" = ")
    for other_var in dict.items():
        var[1] = var[1].replace(other_var[0], other_var[1])
    dict[var[0]] = var[1]
whole = Parser(Lexer(dict["OUT"])).parse()
whole = whole.b_red()
print(whole)
inv_dict = {str(Parser(Lexer(v)).parse().b_red()): k for k, v in dict.items() if k != "OUT"}
try:
    print(inv_dict[str(whole)])
except KeyError:
    print("Undefined")