from sys import argv
import copy

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


def is_unsolved(grid: list) -> bool:
    for e in grid:
        if not is_collapsed(e):
            return True

    return False


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


def is_broken(grid: list) -> bool:
    for e in grid:
        if len(e) == 0:
            return True
    return False


def cycle(in_grid: list, in_collapsed: list, in_not_collapsed: list) -> tuple:
    grid = copy.deepcopy(in_grid)
    collapsed = copy.deepcopy(in_collapsed)
    not_collapsed = copy.deepcopy(in_not_collapsed)

    grid = simplify_grid(grid, collapsed)

    # chain reaction
    while are_collapsed(grid, not_collapsed):
        for ie in not_collapsed:
            if is_collapsed(grid[ie]):
                not_collapsed.remove(ie)

        grid = simplify_grid(grid, collapsed)

        for ie in not_collapsed:
            if is_collapsed(grid[ie]) and not ie in collapsed:
                collapsed.append(ie)

    if is_broken(grid):
        return (False, grid)

    if not is_unsolved(grid):
        return (True, grid)

    # choose 'n collapse

    not_collapsed.sort(key=lambda ie : len(grid[ie]))
    lowest = not_collapsed[0]

    if lowest in collapsed:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    collapsed.append(lowest)
    for e in grid[lowest]:
        grid[lowest] = e
        solved, new_grid = cycle(grid, collapsed, not_collapsed)
        if solved:
            return (True, new_grid)

    if is_unsolved(grid) or is_broken(grid):
        return (False, grid)

    return (True, grid)


def solve(input_sudoku: str) -> tuple:
    grid = []
    collapsed = []
    not_collapsed = []
    i = 0
    for c in input_sudoku:
        if c != "-":
            grid.append(c)
            collapsed.append(i)
        else:
            grid.append("123456789")
            not_collapsed.append(i)
        i += 1

    solved, solved_grid = cycle(grid, collapsed, not_collapsed)
    return (solved, get_formatted_grid(solved_grid))


if __name__ == "__main__":
    filename = argv[1]
    #filename = input()

    input_file = ""
    with open(f"unsolved/{filename}.txt", "r") as f:
        s = "".join(f.readlines())
        input_file = s.replace("\n", "").replace(" ", "")

    is_solved, solved = solve(input_file)

    if is_solved:
        print("Solved!")
    else:
        print("Couldn't solve ya bastard!")

    with open(f"solved/{filename}.txt", "w") as f: f.write(solved)

# TODO: Fix it. Can't solve g.txt
