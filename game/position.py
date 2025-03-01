from game.config import BOARD_SIZE

type AlgebraicNotation = str


class OutOfBoundsError(Exception):
    pass


class Position:
    def __init__(self, rank_index: int, file_index: int) -> None:
        self._ensure_bounds(rank_index, file_index)

        self.rank_index = rank_index
        self.file_index = file_index

    def __iter__(self):
        return iter((self.rank_index, self.file_index))

    def __repr__(self) -> str:
        return f"Position({self.rank_index}, {self.file_index}, {self.get_algebraic_notation()})"

    def __eq__(self, other: "Position") -> bool:
        return (
            self.rank_index == other.rank_index and self.file_index == other.file_index
        )

    def __hash__(self) -> int:
        return hash((self.rank_index, self.file_index))

    def _ensure_bounds(self, x: int, y: int) -> None:
        in_bounds = 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE
        if not in_bounds:
            raise OutOfBoundsError("Position out of bounds")

    @classmethod
    def from_algebraic_notation(cls, notation: AlgebraicNotation) -> "Position":
        assert len(notation) == 2

        letter_row = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        letter, number = notation

        row = BOARD_SIZE - int(number)
        column = letter_row[letter]

        return cls(row, column)

    @classmethod
    def from_idx(cls, idx: tuple[int, int]) -> "Position":
        row, column = idx
        return cls(row, column)

    def get_algebraic_notation(self) -> AlgebraicNotation:
        file_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return f"{file_map[self.file_index]}{BOARD_SIZE - self.rank_index}"

    def add_offset(self, offset: tuple[int, int]) -> "Position":
        return Position(self.rank_index + offset[0], self.file_index + offset[1])
