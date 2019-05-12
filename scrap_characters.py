with open("lib\\edipo_re\\text.txt", 'r', encoding="utf-8") as file:
    text = file.read()
    short = filter(lambda x: len(x.strip().split(' ')) < 2, text.split('\n'))

short = list(filter(lambda x: len(x) > 3 and '-' not in x, short))

print(short)