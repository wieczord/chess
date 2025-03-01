from game.piece import Rook, Color, Knight, Bishop, Queen, King, Pawn, Piece

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

    def _ensure_bounds(self, x: int, y: int) -> bool:
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



BOARD_SIZE = 8


class Engine:
    def __init__(self, board: "Board") -> None:
        self.board = board

    def possible_moves(self, position: Position) -> list[Position]:
        piece = self.board[position]
        if piece is None:
            return []

        return piece.possible_moves(position, self.board)


EMPTY = " " # TODO null object pattern


class Board:
    def __init__(self) -> None:
        self._board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def print(self) -> None:
        for x in self._board:
            print(x, end="\n")

    def initialize_board(self):
        # pawns (white 0,1) black (-2, -1)
        self._board[-1] = [
            Rook(Color.WHITE),
            Knight(Color.WHITE),
            Bishop(Color.WHITE),
            Queen(Color.WHITE),
            King(Color.WHITE),
            Bishop(Color.WHITE),
            Knight(Color.WHITE),
            Rook(Color.WHITE),
        ]
        self._board[-2] = [Pawn(Color.WHITE) for _ in range(BOARD_SIZE)]

        self._board[0] = [
            Rook(Color.BLACK),
            Knight(Color.BLACK),
            Bishop(Color.BLACK),
            Queen(Color.BLACK),
            King(Color.BLACK),
            Bishop(Color.BLACK),
            Knight(Color.BLACK),
            Rook(Color.BLACK),
        ]
        self._board[1] = [Pawn(Color.BLACK) for _ in range(BOARD_SIZE)]

    def _at(self, position: Position) -> Piece | str:
        return self._board[position.rank_index][position.file_index]
    def _is_available_for_move(self, position: Position, piece: Piece) -> bool:
        return self._is_empty(position) or self._is_enemy(position, piece.color)

    def _is_empty(self, position: Position) -> bool:
        return self._at(position) == EMPTY

    def _is_enemy(self, position: Position, color: Color) -> bool:
        piece = self._at(position)
        return piece is not None and piece.color != color

    def _is_friendly(self, position: Position, color: Color) -> bool:
        piece = self._at(position)
        return piece is not None and piece.color == color

    def possible_moves(self, notation: AlgebraicNotation) -> set[Position]:
        position = Position.from_algebraic_notation(notation)
        if not self._is_empty(position): # TODO just get it
            piece = self._at(position)
            return self._generate_moves_from_offsets(position, piece.offsets)
        return []

    def _generate_moves_from_offsets(
            self, position: Position, offsets: list[Position]
    ) -> set[Position]:
        moves = set()
        for _, offset in offsets.items():
            for off in offset:
                try:
                    new_position = position.add_offset(off)
                except OutOfBoundsError:
                    continue

                if new_position is None:
                    continue

                if self._is_available_for_move(new_position, self._at(position)):
                    moves.add(new_position)

        return moves

    # TODO - enkapsulacja pozycji i indeksów w jedną klassę

    def _position_from_offset(
            self, position: Position, offset: Position
    ) -> Position | None:
        x, y = position
        a, b = offset
        new_position = Position(x + a, y + b)
        return new_position

    # TODO - skosne ruchy pionkiem tylko przy biciu, ruch o 2 pola tylko na początku

    def move(self, start: Position, end: Position) -> None:  # TODO przetestować
        piece = self[start]
        if piece is None:
            raise ValueError("No piece at start position")

        possible_moves = self.possible_moves(start)

        # TODO no w sumie kto ma wiedziec jak sie rusza jak nie bierka
        # TODO plus mozna trzymac w niej stan jak np pierwszy ruch czy prawo do roszady

        if end not in possible_moves:
            raise ValueError("Invalid move")
        self[end] = piece
        self[start] = EMPTY


def main() -> None:
    board = Board()
    board.initialize_board()
    board.print()
    e4 = board._idx_from_algebraic_notation("e4")
    board.move("e2", "e3")
    board.move("e2", "e5")
    print()
    board.print()


if __name__ == "__main__":
    main()
