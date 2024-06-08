from sys import argv
import random

def is_duplicate(i: int, val: int, grid: list, collapsed: list) -> bool:
    for ie in collapsed:
        if val == grid[ie] and (is_same_row(i, ie) or is_same_column(i, ie) or is_same_box(i, ie)):
            return True

    return False


def is_collapsed(vals: str) -> bool:
    return len(vals) == 1


def are_collapsed(grid: list, not_collapsed: list) -> bool:
    for i in not_collapsed:
        if is_collapsed(grid[i]):
            return True
    return False


def get_entropy(vals: str) -> int:
    return len(vals)


def is_same_row(i1: int, i2: int) -> bool:
    return i1 // 9 == i2 // 9


def is_same_column(i1: int, i2: int) -> bool:
    return i1 % 9 == i2 % 9


def get_box_index(i: int) -> int:
    return ((i // 9) // 3) * 3 + (i % 9) // 3


def is_same_box(i1: int, i2: int) -> bool:
    return get_box_index(i1) == get_box_index(i2)


def simplify_grid(grid: list, collapsed: list) -> list:
    for i in range(len(grid)):
        if i in collapsed:
            continue

        for ie in collapsed:
            if is_same_row(i, ie) or is_same_column(i, ie) or is_same_box(i, ie):
                grid[i] = grid[i].replace(grid[ie], "")

    return grid


def simplify_list(l: list) -> str:
    return list(dict.fromkeys(l))


def get_formatted_grid(grid: list) -> str:
    ret = ""
    for i in range(len(grid)):
        if is_collapsed(grid[i]):
            ret += grid[i]
        else:
            ret += "-"

        if ((i+1) % 3) == 0:
            ret += " "

        if ((i + 1) % 9) == 0:
            ret += "\n"

            if ((i // 9) + 1) % 3 == 0:
                ret += "\n"

    return ret


def solve(input_sudoku: str, filename: str) -> bool:
    grid = []
    collapsed = []
    not_collapsed = []
    i = 0
    for c in input_sudoku:
        if c != "-":
            grid.append(c)
            collapsed.append(i)
            collapsed = simplify_list(collapsed)
        else:
            grid.append("123456789")
            not_collapsed.append(i)
            not_collapsed = simplify_list(not_collapsed)
        i += 1

    while len(not_collapsed) != 0:
        # chain reaction
        while are_collapsed(grid, not_collapsed):
            for ei in not_collapsed:
                if is_collapsed(grid[ei]):
                    not_collapsed.remove(ei)

            grid = simplify_grid(grid, collapsed)

            for ei in not_collapsed:
                if is_collapsed(grid[ei]):
                    collapsed.append(ei)
                    collapsed = simplify_list(collapsed)

        # choose 'n collapse
        had_collapsed = False
        not_collapsed.sort(key=lambda ie : get_entropy(grid[ie]))

        for lowest in not_collapsed:
            if lowest == 1_000_000:
                print("an error has occured")
                break

            pick = []
            for val in grid[lowest]:
                if not is_duplicate(lowest, val, grid, collapsed):
                    pick.append(val)

            if len(pick) != 0:
                grid[lowest] = random.choice(pick)
                collapsed.append(lowest)
                collapsed = simplify_list(collapsed)
                had_collapsed = True

            if had_collapsed:
                break

        if not had_collapsed and len(collapsed) != len(grid):
            with open(f"solved/{filename}.txt", "w") as f: f.write(get_formatted_grid(grid))
            return False


    output = ""
    for i in range(len(grid)):
        output += grid[i]
        if ((i + 1) % 9) == 0:
            output += "\n"

    with open(f"solved/{filename}.txt", "w") as f: f.write(get_formatted_grid(grid))
    return True


if __name__ == "__main__":
    filename = argv[1]

    input_file = ""
    with open(f"unsolved/{filename}.txt", "r") as f:
        s = "".join(f.readlines())
        input_file = s.replace("\n", "").replace(" ", "")

    while not solve(input_file, filename):
        print("Didn't solve.")

    print("Solved!")
