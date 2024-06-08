"""
    Sudoku Solver v3 (ssv3)
    
    made by: TekMike365
"""

import sys
import os.path
import copy
import time

def is_same_row(i1: int, i2: int) -> bool:
    return i1 // 9 == i2 // 9


def is_same_column(i1: int, i2: int) -> bool:
    return i1 % 9 == i2 % 9


def get_box_index(i: int) -> int:
    return ((i // 9) // 3) * 3 + (i % 9) // 3


def is_same_box(i1: int, i2: int) -> bool:
    return get_box_index(i1) == get_box_index(i2)


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read().replace(" ", "").replace("\n", "").replace("\r", "")


def save_file(sudoku: str, filepath: str) -> str:
    out = ""
    for i in range(81):
        out += sudoku[i]
        if i % 3 == 2:
            out += " "
        if i % 9 == 8:
            out += "\n"
            if (i // 9) % 3 == 2:
                out += "\n"
    with open(filepath, "w") as f: f.write(out)


def is_collapsed(val: str) -> bool:
    return len(val) == 1


def is_broken(val: str) -> None:
    return len(val) == 0


# TODO create a Game 'struct'
class Game:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.collapsed = []
        self.uncollapsed = []
        for i in range(len(grid)):
            self.uncollapsed.append(i)

        self.is_solved = False
        self.is_broken = False


def game_update_collapsed(game: Game) -> None:
    for i in range(len(game.grid)):
        if is_collapsed(game.grid[i]) and not i in game.collapsed:
            game.collapsed.append(i)


def game_collapsed_in_uncollapsed(game: Game) -> int:
    for e in game.collapsed:
        if e in game.uncollapsed:
            return e
    return None


def game_collapse(game: Game, id: int) -> None:
    if id in game.uncollapsed:
        game.uncollapsed.remove(id)
    if not id in game.collapsed:
        game.collapsed.append(id)

    for i in range(len(game.grid)):
        for e in game.grid[i]:
            if i == id:
                continue
            if e == game.grid[id] and (is_same_row(id, i) or is_same_column(id, i) or is_same_box(id, i)):
                game.grid[i] = game.grid[i].replace(e, "")
                continue
        if is_broken(game.grid[i]):
            game.is_broken = True


def game_update(game: Game) -> None:
    game_update_collapsed(game)
    to_collapse = game_collapsed_in_uncollapsed(game)
    while to_collapse != None:
        game_collapse(game, to_collapse)
        to_collapse = game_collapsed_in_uncollapsed(game)
    game_update_status(game)


def game_sort_uncollapsed(game: Game) -> None:
    game.uncollapsed.sort(key=lambda e : len(game.grid[e]))


def game_grid_str(game: Game) -> str:
    ret = ""
    for e in game.grid:
        if is_collapsed(e):
            ret += e
        else:
            ret += "-"
    return ret


def game_update_status(game: Game) -> None:
    game.is_solved = True
    for e in game.grid:
        if not is_collapsed(e):
            game.is_solved = False

        if is_broken(e):
            game.is_broken = True

    if game.is_solved and game.is_broken:
        game.is_solved = False


def recursive_solve(a_game: Game) -> Game:
    game = copy.deepcopy(a_game)

    game_update(game)

    if game.is_solved or game.is_broken:
        return game

    game_sort_uncollapsed(game)
    for e in game.grid[game.uncollapsed[0]]:
        game.grid[game.uncollapsed[0]] = e
        new_game = recursive_solve(game)
        if new_game.is_solved:
            return new_game

    return game


def solve(sudoku: str) -> str:
    grid = []
    for e in sudoku:
        if e != "-":
            grid.append(e)
            continue
        grid.append("123456789")

    game = Game(grid)
    game = recursive_solve(game)

    return game_grid_str(game)


def print_help() -> None:
    print("ssv3.py -h")
    print("ssv3.py <in_filepath> <out_filepath>")


def main(argv: list) -> int:
    if len(argv) == 1:
        print("requires arguments.")
        print_help()
        return -1

    if argv[1] == "-h":
        print_help()
        return 0

    if len(argv) < 3:
        print("requires 2 arguments.")
        print_help()
        return -1

    in_filepath = argv[1]
    out_filepath = argv[2]

    if not (os.path.exists(in_filepath) and os.path.isfile(in_filepath)):
        print(f"file '{in_filepath}' doesn't exist.")

    out_dir_filepath = ""
    if "/" in out_filepath:
        out_dir_filepath = "/".join(out_filepath.split("/")[:-1]) + "/"
    if "\\" in out_filepath:
        out_dir_filepath = "\\".join(out_filepath.split("\\")[:-1]) + "\\"

    if not (os.path.exists(out_dir_filepath) and os.path.isdir(out_dir_filepath)):
        print(f"dir '{out_dir_filepath}' doesn't exist.")

    solved = solve(read_file(in_filepath))

    save_file(solved, out_filepath)

    return 0


if __name__ == "__main__":
    t0 = time.time()
    exit_code = main(sys.argv)
    t1 = time.time()
    print(f"time: {(t1 - t0) * 10 ** 3}ms")
    print("Program ended with exit code:", exit_code)
