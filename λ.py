data = ""
with open("programs/nums.λ", "r") as f:
    data = f.read().split("\n")

# lexer
toks = []
for d in data:
    tok = []
    cur = 0
    while cur < len(d):
        if d[cur] in "λ.=\n" or 97 <= ord(d[cur]) <= 122 or 40 <= ord(d[cur]) <= 41:
            tok.append(d[cur])
        if 65 <= ord(d[cur]) <= 90:
            var = ""
            while cur < len(d) and (65 <= ord(d[cur]) <= 90 or 48 <= ord(d[cur]) <= 57):
                var += d[cur]
                cur += 1
            tok.append(var)
        cur += 1
    toks.append(tok)
print(toks)

dct = {}
for i in toks:
    dct[i[0]] = list(map(lambda x : dct[x] if 65 <= ord(x[0]) <= 90 or 48 <= ord(x) <= 57 else x, i[2:]))
print(dct["OUT"])

def create_ast(x):
    if x[0] == "λ":
        return [x[1], create_ast(x[3:])]
    if x[0] == "(":
        print(x)
        return [create_ast(x[:x.index(")")]), x[x.index(")")+1:]]
print(create_ast(["(", ")"]))