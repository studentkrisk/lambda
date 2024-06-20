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
        print(char)
        if char in "λ.()":
            return Token(char, None)
        else:
            return Token("SYMBOL", char)

#parser
class Function:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp
    def __repr__(self):
        return f"λ{self.var}.{self.exp}"
class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.right})"
class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        print(self.parse())
    def parse(self):
        new = self.lexer.next()
        if new.type == "λ":
            return self.create_function()
        elif new.type == "(":
            return self.create_application()
        elif len(toks) > 1:
            return Application(self.parse(toks[:-2]), Var(toks[-1].value))
        else:
            return Var(toks[0].value)
    def create_function(self):
        var = Var(self.lexer.next().value)
        self.lexer.next()
        return Function(var, self.parse())
    def create_application(self):
        left = self.parse()
        right = self.parse()
        return Application(left, right)


# toks = {}
# for i in data:
#     toks[i.split(" ")[0]] = Lexer(" ".join(i.split(" ")[2:])).toks

Parser(Lexer(data[0]))


# toks = []
# for d in data:
#     tok = []
#     cur = 0
#     while cur < len(d):
#         if d[cur] in "λ.=\n" or 97 <= ord(d[cur]) <= 122 or 40 <= ord(d[cur]) <= 41:
#             tok.append(d[cur])
#         if 65 <= ord(d[cur]) <= 90:
#             var = ""
#             while cur < len(d) and (65 <= ord(d[cur]) <= 90 or 48 <= ord(d[cur]) <= 57):
#                 var += d[cur]
#                 cur += 1
#             tok.append(var)
#         cur += 1
#     toks.append(tok)
# print(toks)

# dct = {}
# for i in toks:
#     dct[i[0]] = list(map(lambda x : dct[x] if 65 <= ord(x[0]) <= 90 or 48 <= ord(x) <= 57 else x, i[2:]))
# print(dct["OUT"])

# def create_ast(x):
#     if x[0] == "λ":
#         return [x[1], create_ast(x[3:])]
#     if x[0] == "(":
#         print(x)
#         return [create_ast(x[1:x.index(")")] + x[x.index(")")+1:])]
#     return x
# print(create_ast(["(", "x", ")"]))