from sys import argv

filepath = argv[1]

error = False

grid = ""
with open(filepath, "r") as f:
    s = "".join(f.readlines())
    grid = s.replace("\n", "").replace(" ", "")

for i in range(9):
    row = grid[i*9:9]
    simple_row = "".join(set(row))
    
    if len(row) != len(simple_row):
        print("incorrect row:", row)
        error = True

for i in range(9):
    column = ""
    for j in range(9):
        column += grid[j*9 + i]

    simple_column = "".join(set(column))
    
    if len(column) != len(simple_column):
        print("incorrect column:", column)
        error = True

for i in range(9):
    y = i // 3
    x = i % 3
    box = ""
    for m in range(3):
        for n in range(3):
            box += grid[y*3*9 + m*9 + x*3 + n]

    simple_box = "".join(set(box))

    if len(box) != len(simple_box):
        print("incorrect box:", box[:3])
        print("              ", box[3:6])
        print("              ", box[6:9])
        error = True

if not error:
    print("Everything is awesome.")
