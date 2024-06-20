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
        return "{" + self.type + ": " + str(self.value) + "}"
class Lexer:
    def __init__(self, d):
        self.cur = 0
        self.d = d
        self.toks = []
        while self.cur < len(self.d):
            self.toks.append(self.tokenize())
            self.cur += 1
        self.toks.append(Token("EOF", None))

    def tokenize(self):
        while self.d[self.cur] in whitespace:
            self.cur += 1
        char = self.d[self.cur]
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
class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name.value
class Parser:
    def __init__(self, toks):
        self.toks = toks
        print(self.parse(self.toks))
    def parse(self, toks):
        if toks[0].type == "λ":
            return Function(Var(toks[1]), self.parse(toks[3:]))
        elif len(toks) > 1:
            return Application(self.parse(toks[:-2]), self.parse(toks[-1]))


# toks = {}
# for i in data:
#     toks[i.split(" ")[0]] = Lexer(" ".join(i.split(" ")[2:])).toks

Parser(Lexer(data[0]).toks)


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