class WordSearch:
    def __init__(self, grid: str):
        self.grid: str = grid
        n: int = int(len(grid) ** 0.5)
        if n**2 != len(grid):
            raise ValueError("Not a square grid")

        self.n: int = n

        self.chToIdx: dict[str, list[int]] = {}
        for idx, ch in enumerate(grid):
            if ch not in self.chToIdx:
                self.chToIdx[ch] = []
            self.chToIdx[ch].append(idx)

    def is_vertical(self, idx: int, word: str) -> bool:
        """Checks whether at that index we have a vertical word"""
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
        """Checks whether at that index we have a horizontal word"""
        if (idx % self.n) + len(word) > self.n:
            return False

        gridPtr: int = idx
        if self.grid[gridPtr : gridPtr + len(word)] == word:
            return True
        return False

    def is_present(self, word: str) -> bool:
        """Checks whether word is in the grid"""
        if not word:
            return False

        first = word[0]
        if first not in self.chToIdx:
            return False

        for idx in self.chToIdx[first]:
            if self.is_vertical(idx, word) or self.is_horizontal(idx, word):
                return True
        return False


grid: str = "kdsaaajflaaaakdaaajflaaaasdaaajfaaaa"
"""
kdsaaa
jflaaa
akdaaa
jflaaa
asdaaa
jfaaaa
"""
"""
len(grid) = 36
COLS == 6
ROWS == 6

if we are going down case for kfs
13 to 19 to 25
check whether its in bounds 

if we are going across for fla
18 to 19 to 20 make sure we are in the same column

18 // 6

"""
words_to_find = ["add", "aaa", "lda", "jaj"]
ws = WordSearch(grid)
for word in words_to_find:
    if ws.is_present(word):
        print(f"found {word}")
