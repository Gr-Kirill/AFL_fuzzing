import random
import string

list_a = ["[]",
    "{}",
    '"A":"B"',
    '"C":{"D":"E","F":"G"}',
    '"Z":{},"Y":"X"',
    '"H":["I","J","K"]',
    '"L":{"M":"N","O":["P","Q"]}}',
    '"R":null,"S":true',
    '"T":false,"U":123',
    '"V":-456,"W":789.0',
    "0",
    ",0",
    ":0",
    "0:",
    "-1.2e+3",
    "true",
    "false",
    "null",
    "\"\"",
    ",\"\"",
    ":\"\"",
    "\"\":",
    ",{}",
    ":{}",
    "{\"\":0}",
    "{{}}",
    ",[]",
    ":[]",
    "[0]",
    "[[]]",
    "''",
    "\\",
    "\\b",
    "\\f",
    "\\n",
    "\\r",
    "\\t",
    "\\u0000",
    "\\x00",
    "\\0",
    "\\uD800\\uDC00",
    "\\uDBFF\\uDFFF",
    "\"\":0",
    "//",
    "/**/",
    "$ref",
    "type",
    "coordinates",
    "@context",
    "@id",
    ",",
    ":"]



with open("./model/result.json", "w") as f:
    list_c = list()
    while len(list_c) != 150:
        a = ""
        while len(a) < 30:
            i = list_a[random.randint(0, len(list_a) - 1)]
            if len(i) + len(a) <= 30:
                a += i
        if a not in list_c:
            list_c.append(a)
    for i in list_c:
        f.write(i+'\n')

all_characters = string.ascii_letters + string.digits + string.punctuation


with open("./model/input.json", "w") as file:
    list_b = list()
    for i in range (150):
        random_string = ''.join(random.choice(all_characters) for _ in range(30))
        list_b.append(random_string)
    for i in list_b:
        file.write(i+'\n')