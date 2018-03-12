from random import randint


emojis = [':apple:', ':tangerine:', ':watermelon:', ':cherries:', ':grapes:', ':strawberry:', ':pineapple:', ':lemon:']


def play():
    rows = []
    won = False
    for i in range(3):
        row = get_rand_row()
        if i == 1:
            if row[0] == row[1] == row[2]:
                won = True
        rows.append(row)
    for i in range(len(rows)):
        str_row = []
        for num in rows[i]:
            str_row.append(emojis[num])
        rows[i] = ' '.join(str_row)
    return won, rows


def get_rand_row():
    row = []
    for _ in range(3):
        row.append(randint(0, len(emojis) - 1))
    return row
