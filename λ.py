from string import ascii_lowercase, ascii_uppercase

data = ""
with open("test.λ", "r") as f:
    data = f.read().split("\n")

toks = []
for d in data:
    tok = []
    cur = 0
    while cur < len(d):
        if d[cur] in ascii_lowercase + "λ.=\n":
            tok.append(d[cur])
        if d[cur] in ascii_uppercase:
            var = ""
            while cur < len(d) and d[cur] in ascii_uppercase:
                var += d[cur]
                cur += 1
            tok.append(var)
        cur += 1
    toks.append(tok)
print(toks)