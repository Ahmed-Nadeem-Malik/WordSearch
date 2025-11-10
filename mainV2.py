class WordSearch:
    """
    Method adapted from v1, instead of checking that the word is at
    that index when we are checking the word we instead do it when
    we instatiate the class, its O(n^2) in time complexity but when
    we actually call is_present its O(n) which is very fast but the
    trade off is that our space complexity is O(n^2)
    """

    def __init__(self, grid: str):
        self.grid: str = grid
        n: int = int(len(self.grid) ** 0.5)
        if n**2 != len(grid):
            raise ValueError("Not a square grid")

        self.n: int = n

        self.valid_words: set[str] = set()
        self.all_words()

    def vertical_words(self, idx: int, length: int) -> str:
        """Adds word going down starting from index to index + length"""
        if (idx // self.n) + length > self.n:
            return ""

        gridPtr: int = idx
        word_chars: list[str] = []
        for _ in range(length):
            if gridPtr >= len(self.grid):
                return ""

            word_chars.append(self.grid[gridPtr])
            gridPtr += self.n

        return "".join(word_chars)

    def horizontal_words(self, idx: int, length: int) -> str:
        """Adds word going right starting from index to index + length"""
        if (idx % self.n) + length > self.n:
            return ""

        return self.grid[idx : idx + length]

    def all_words(self) -> None:
        """Adds a word incrementally from a index to length by going right and down"""
        for idx in range(len(self.grid)):
            for length in range(4, 21):
                word: str = self.horizontal_words(idx, length)
                if word:
                    self.valid_words.add(word)

                word = self.vertical_words(idx, length)
                if word:
                    self.valid_words.add(word)

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
