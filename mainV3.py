"""
Same as V2 but more as a case study to see how multicore helps
with speed of the word-set initialization which is our most
time-consuming set.

Moved functions outside the class because they conflicted with
the multiprocessing library.

First we make workers. Then for each row we allocate a worker
that does the processing like before. We can do multiple rows at
the same time since it is multiprocessing so it should be faster.

Results:
For the original grid used for testing:
V2: 0.0003752919983526226 seconds
V3: 0.0737524169999233 seconds
There is a slowdown here. This is likely the multiprocessing overhead.
As input size increases the V3 overhead should become minimal and
performance should improve.

For the large grid made by make_grid:
V2: 47.72359229200083 seconds
V3: 4.3694680410008 seconds
This is about a 10x speedup. Larger inputs benefit from multiprocessing.

Conclusion:
Large grid: use multiprocessing.
Small grid: use the basic version.

References:
Multiprocessing: https://superfastpython.com/multiprocessing-pool-python/
"""

from multiprocessing import Pool, cpu_count
import time


def horizontal_word(grid: str, n: int, idx: int, length: int) -> str:
    """Adds word going right starting from index to index + length"""
    if (idx % n) + length > n:
        return ""

    return grid[idx : idx + length]


def vertical_word(grid: str, n: int, idx: int, length: int) -> str:
    """Adds word going down starting from index to index + length"""
    if (idx // n) + length > n:
        return ""

    gridPtr: int = idx
    word_chars: list[str] = []
    for _ in range(length):
        if gridPtr >= len(grid):
            return ""

        word_chars.append(grid[gridPtr])
        gridPtr += n

    return "".join(word_chars)


def _row_worker(row: int, grid: str, n: int) -> set[str]:
    """Adds a word incrementally from a index to length by going right and down"""
    base: int = row * n
    out: set[str] = set()
    for col in range(n):
        idx: int = base + col

        for length in range(4, 21):
            word = horizontal_word(grid, n, idx, length)
            if word:
                out.add(word)

            word = vertical_word(grid, n, idx, length)
            if word:
                out.add(word)

    return out


def make_grid(side: int) -> str:
    """To make a very large grid"""
    alphabet: str = "abcdefghijklmnopqrstuvwxyz"
    out: list[str] = []
    for i in range(side * side):
        out.append(alphabet[i % 26])

    return "".join(out)


class WordSearch:
    def __init__(self, grid: str):
        self.grid: str = grid
        n: int = int(len(self.grid) ** 0.5)
        if n**2 != len(grid):
            raise ValueError("Not a square grid")

        self.n: int = n

        self.valid_words: set[str] = set()
        self.all_words()

    def all_words(self) -> None:
        """Make word set using workers"""
        with Pool(cpu_count()) as p:  # make worker pool based on our cpu count
            results = p.starmap(  #  lets us pass multiple arguments into the _row_worker function
                _row_worker, [(r, self.grid, self.n) for r in range(self.n)]
            )

        for s in results:
            self.valid_words.update(s)

    def is_present(self, word: str) -> bool:
        "Checks whether that the word is in the grid"
        if not word or len(word) < 4 or len(word) > 20:
            return False

        return word in self.valid_words


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
    print(test_grid)

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

    start = time.perf_counter()
    wsTest = WordSearch(make_grid(2000))
    end = time.perf_counter()
    print("Word set build time ", end - start, "seconds")

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
