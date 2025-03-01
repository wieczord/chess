import inspect

from game.config import BOARD_SIZE
from game.piece import Rook, Color, Knight, Bishop, Queen, King, Pawn, Piece, Empty
from game.position import Position, OutOfBoundsError, AlgebraicNotation


class Engine:
    def __init__(self, board: "Board") -> None:
        self.board = board

    def possible_moves(self, position: Position) -> list[Position]:
        piece = self.board[position]
        if piece is None:
            return []

        return piece.possible_moves(position, self.board)


EMPTY = Empty()


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
        return self._is_empty(position) or self._is_enemy(
            position, piece.color
        )  # TODO _is_enemy? tutaj dla krola / pina trzeba uwazac

    def _is_empty(self, position: Position) -> bool:  # TODO potrzebne?
        return self._at(position) == EMPTY

    def _is_enemy(self, position: Position, color: Color) -> bool:
        piece = self._at(position)
        return piece != EMPTY and piece.color != color

    def _is_friendly(self, position: Position, color: Color) -> bool:
        piece = self._at(position)
        return piece is not None and piece.color == color

    def _get_possible_moves(self, position: Position) -> tuple[Piece | Empty, set[Position]]:
        piece = self._at(position)
        if piece != EMPTY:
            return piece, self._generate_moves_from_offsets(position, piece)
        return EMPTY, set()

    def possible_moves(self, notation: AlgebraicNotation) ->  set[Position]:
        position = Position.from_algebraic_notation(notation)
        _, possible_moves = self._get_possible_moves(position)
        return possible_moves

    def _generate_moves_from_offsets(
        self, position: Position, piece: Piece
    ) -> set[Position]:
        moves = set()
        offsets = piece.offsets
        move_offsets = offsets.move_or_attack + (
            offsets.first_move if not piece.state.has_moved else []
        )
        try:
            for offset in move_offsets:
                new_position = position.add_offset(offset)
                if self._is_available_for_move(new_position, self._at(position)):
                    moves.add(new_position)

            for offset in offsets.special_attack:
                new_position = position.add_offset(offset)
                if self._is_enemy(new_position, self._at(position)):
                    moves.add(new_position)
        except OutOfBoundsError:
            pass

        return moves

    # TODO - ruch o 2 pola tylko na początku

    def move(self, start: AlgebraicNotation, end: AlgebraicNotation) -> None:  # TODO przetestować
        start_pos = Position.from_algebraic_notation(start)
        piece_to_move, possible_moves = self._get_possible_moves(start_pos)
        if piece_to_move == EMPTY:
            raise ValueError("Empty start position")

        if not possible_moves:
            raise ValueError("No possible moves")

        end_pos = Position.from_algebraic_notation(end)
        if end_pos not in possible_moves:
            raise ValueError("Invalid move")

        self._place_on_board(end_pos, piece_to_move)
        self._place_on_board(start_pos, EMPTY)

        self._update_piece_state(piece_to_move)

    def _place_on_board(self, position: Position, piece: Piece | Empty) -> None:
        self._board[position.rank_index][position.file_index] = piece

    def _update_piece_state(self, piece: Piece) -> None:
        piece.state.has_moved = True

def main() -> None:
    board = Board()
    board.initialize_board()
    board.print()
    print()
    board.move("e2", "e4")
    print()
    board.print()
    board.move("e4", "e5")
    print()
    board.print()


if __name__ == "__main__":
    main()
