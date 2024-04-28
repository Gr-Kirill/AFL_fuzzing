import random
import json

CHRAS = [
    ',',
    '[',
    '}',
    ':',
    '"',
    "'",
]

WORDS = [
    "[]",
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
    ":",
    '{"level1": {"level2": {"level3": {"level4": {"key1": "value1", "key2": "value2"}}, "key3": "value3"}, "key4": "value4"}}',
]


def deinit():
    pass

def get_json_block():
    data = {
        "phone_numbers": [
            {
                "type": "home",
                "number": "555-555-1212"
            },
            {
                "type": "work",
                "number": "555-555-1213"
            }
        ]
    }

    test = json.dumps(data, indent=4)
    return test

#За 6 минут ищет 911 корпусов
def insert_json_block(buf):     #Вставка блока json в тест после рандомной запятой
    tmp_str = get_json_block()
    positions = [i for i, c in enumerate(buf) if c == ',']
    if positions:
        position= random.choice(positions)
    else:
        position = 0

    mutated_data = buf[:position] + tmp_str + buf[position:]

    return mutated_data

#За 6 минут ищет 935 корпусов
def merger(buf, add_buf):
    len_first = len(buf) // 2
    len_second = len(add_buf) // 2
    mutated_buf = ""
    choice = random.randint(1, 4)
    if(choice == 1) :
        mutated_buf += add_buf[:len_second]
        mutated_buf += buf[:len_first]
    elif(choice == 2) :
        mutated_buf += add_buf[:len_second]
        mutated_buf += buf[len_first:]
    elif(choice == 3) :
        mutated_buf += buf[:len_first]
        mutated_buf += add_buf[:len_second]
    else :
        mutated_buf += buf[:len_first]
        mutated_buf += add_buf[len_second:]
    
    return mutated_buf

#За 6 минут ищет 965 корпусов
def insert_words(buf):  # Вствка после запятой любого WORDS,  Результат - строка
    mutated_buf = ""
    for c in buf:
        mutated_buf += c
        if c == ',' and random.choice([0, 1]):
            mutated_buf += random.choice(WORDS)
            mutated_buf += ','

    return mutated_buf

#За 6 минут ищет 966 корпусов
def del_open_close(buf): #удаляет '[содержимое]' включительно []  Результат - строка
    count = 0
    open = 0
    for c in buf: 
        if (c == '['):
            open = count
        elif (c == ']'):
            return (buf[:open] + buf[count+1:])
        count+=1
    buf = insert_words(buf)

    return buf

#За 6 минут ищет 862 корпусов
def del_symbol(buf):
    mutated_buf = ""
    for c in buf:
        if c in CHRAS and random.choice([0, 1]):
            continue
        mutated_buf += c
    
    return mutated_buf

def fuzz(buf, add_buf, max_size):
    str_buf = buf.decode('utf-8', 'ignore')
    way = random.choice([0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5])
    mutated_buf = ""
    if way == 0:
        #За 6 минут ищет 969 корпусов
        for _ in range(random.randint(3, 5)):
            mutated_buf += random.choice(WORDS)
    elif way == 1:
        str_add_buf = add_buf.decode('utf-8', 'ignore')
        mutated_buf = merger(str_buf, str_add_buf)
    elif way == 2:
        mutated_buf = insert_words(str_buf)
    elif way == 3:
        mutated_buf = del_open_close(str_buf)
    elif way == 4:
        mutated_buf = insert_json_block(str_buf)
    else:
        mutated_buf = del_symbol(str_buf)

    return bytearray(mutated_buf, 'utf-8')
