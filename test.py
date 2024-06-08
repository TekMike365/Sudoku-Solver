s = ""
for i in range(81):
    s += str(((i // 9) // 3) * 3 + (i % 9) // 3)

    if ((i+1) % 3) == 0:
        s += " "

        if ((i + 1) % 9) == 0:
            s += "\n"

            if ((i // 9) + 1) % 3 == 0:
                s += "\n"

print(s)
