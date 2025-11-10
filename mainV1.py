"""
Initial solution:
Make a hashmap for every character to indec then iterate through those index's via a dfs down and right
thought that for a very large input maybe precomputing the words is better
"""


class WordSearch:
    def __init__(self, grid: str):
        self.grid: str = grid
        n: int = int(len(grid) ** 0.5)
        if n**2 != len(grid):
            raise ValueError("Not a square grid")

        self.n: int = n

    def is_vertical(self, idx: int, word: str) -> bool:
        """Checks the vertical"""
        if (idx // self.n) + len(word) > self.n:
            return False

        gridPtr: int = idx
        for ch in word:
            if gridPtr >= len(self.grid):
                return False

            if ch != self.grid[gridPtr]:
                return False

            gridPtr += self.n

        return True

    def is_horizontal(self, idx: int, word: str) -> bool:
        "Checks the horizontal"
        if (idx % self.n) + len(word) > self.n:
            return False

        gridPtr: int = idx
        if self.grid[gridPtr : gridPtr + len(word)] == word:
            return True

        return False

    def is_present(self, word: str) -> bool:
        "Checks whether that the word is in the grid"
        if not word or len(word) < 4 or len(word) > 20:
            return False

        for idx in range(len(self.grid)):
            if self.is_vertical(idx, word) or self.is_horizontal(idx, word):
                return True

        return False


if __name__ == "__main__":
    # Made via python script:
    test_grid = (
        "abcdefghij"
        "klmnopqrst"
        "uvwxyzabcd"
        "efghijklmn"
        "opqrstuvwx"
        "yzabcdefgh"
        "ijklmnopqr"
        "stuvwxyzab"
        "cdefghijkl"
        "mnopqrstuv"
    )

    # Grid layout:
    # a b c d e f g h i j
    # k l m n o p q r s t
    # u v w x y z a b c d
    # e f g h i j k l m n
    # o p q r s t u v w x
    # y z a b c d e f g h
    # i j k l m n o p q r
    # s t u v w x y z a b
    # c d e f g h i j k l
    # m n o p q r s t u v

    ws = WordSearch(test_grid)

    print("Testing horizontal words")
    assert ws.is_present("abcdefgh"), "'abcdefgh' should be present (first row)"
    assert ws.is_present("klmnopqr"), "'klmnopqr' should be present (second row)"
    assert ws.is_present("uvwxyzab"), "'uvwxyzab' should be present (third row)"

    print("Testing vertical words")
    assert ws.is_present("akueoyiscm"), "'akueoyiscm' should be present (first column)"
    assert ws.is_present("blvfpzjtdn"), "'blvfpzjtdn' should be present (second column)"

    print("Testing invalid cases")
    assert not ws.is_present("abc"), "'abc' should not be present (too short, min 4)"
    assert ws.is_present("ghijklmn"), "'ghijklmn' should be present (exists in row 3)"
    assert ws.is_present("wxyz"), "'wxyz' should be present (exists in multiple places)"

    print("All tests passed!")
