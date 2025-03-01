from piece import Rook, Color, Knight, Bishop, Queen, King, Pawn, Piece

Position = str

BOARD_SIZE = 8


class Engine:
    def __init__(self, board: "Board") -> None:
        self.board = board

    def possible_moves(self, position: Position) -> list[Position]:
        piece = self.board[position]
        if piece is None:
            return []

        return piece.possible_moves(position, self.board)


EMPTY = " "

type BoardIndex = tuple[int, int]


class Board:
    def __init__(self) -> None:
        self._board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def print(self) -> None:
        for x in self._board:
            print(x, end="\n")

    def __getitem__(self, position: Position) -> Piece | None:
        x, y = self._idx_from_algebraic_notation(position)
        return self._board[x][y]

    def __setitem__(self, position: Position, piece: Piece | None) -> None:
        x, y = self._idx_from_algebraic_notation(position)
        self._board[x][y] = piece

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

    def _is_available_for_move(self, position: Position, piece: Piece) -> bool:
        return self._is_empty(position) or self._is_enemy(position, piece.color)

    def _is_empty(self, position: Position) -> bool:
        return self[position] == EMPTY

    def _is_enemy(self, position: Position, color: Color) -> bool:
        piece = self[position]
        return piece is not None and piece.color != color

    def _is_friendly(self, position: Position, color: Color) -> bool:
        piece = self[position]
        return piece is not None and piece.color == color

    def possible_moves(self, position: Position) -> set[Position]:
        if not self._is_empty(position):
            piece = self[position]
            return self._generate_moves_from_offsets(position, piece.offsets)
        return []

    def _generate_moves_from_offsets(
            self, position: Position, offsets: list[Position]
    ) -> set[Position]:
        moves = set()
        for offset in offsets:
            new_position = self._position_from_offset(position, offset)

            if new_position is None:
                continue

            if not self._is_position_within_bounds(new_position):
                continue

            if self._is_available_for_move(new_position, self[position]):
                moves.add(new_position)

        return moves

    # TODO - enkapsulacja pozycji i indeksów w jedną klassę
    def _is_position_within_bounds(self, position: Position) -> bool:
        x, y = self._idx_from_algebraic_notation(position)
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def _position_from_offset(self, position: Position, offset: Position) -> Position | None:
        x, y = self._idx_from_algebraic_notation(position)
        a, b = offset
        try:  # TODO - to jest brzydkie
            return self._algebraic_notation_from_idx((x + a, y + b))
        except KeyError:
            return None

    # TODO - skosne ruchy pionkiem tylko przy biciu, ruch o 2 pola tylko na początku
    def _idx_from_algebraic_notation(self, notation: str) -> Position:
        assert len(notation) == 2

        letter_row = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        letter, number = notation

        row = BOARD_SIZE - int(number)
        column = letter_row[letter]
        return row, column

    # TODO można to wygenerować (computed_property czy coś takiego)
    def _algebraic_notation_from_idx(self, idx: BoardIndex) -> str:
        row, column = idx
        letter_row = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return f"{letter_row[column]}{BOARD_SIZE - row}"

    def move(self, start: Position, end: Position) -> None:  # TODO przetestować
        piece = self[start]
        if piece is None:
            raise ValueError("No piece at start position")

        possible_moves = self.possible_moves(
            start
        )

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
