from abc import ABC
from typing import Protocol, Literal

type Rank = Literal[1, 2, 3, 4, 5, 6, 7, 8]
type File = Literal["a", "b", "c", "d", "e", "f", "g", "h"]
type PieceChar = Literal[
    "P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"
]  # Upper case for white, lower case for black
type Color = Literal["white", "black"]


class Notation:
    def __init__(self, rank: Rank, file: File):
        self.rank = rank
        self.file = file

    def __repr__(self):
        return f"{self.file}{self.rank}"

    @classmethod
    def as_index(cls, rank: Rank, file: File) -> tuple[int, int]:
        return rank - 1, ord(file) - ord("a")


# class BoardState(Protocol):
#     def is_in_check(self) -> bool: ...
#     def is_in_checkmate(self) -> bool: ...
#     def is_in_stalemate(self) -> bool: ...


class PieceFactory:

    @classmethod
    def from_char(cls, piece_char: PieceChar):
        match piece_char:
            case "P" | "p":
                return Pawn(color=cls._color(piece_char))
            case "N" | "n":
                return Knight(color=cls._color(piece_char))
            case "B" | "b":
                return Bishop(color=cls._color(piece_char))
            case "R" | "r":
                return Rook(color=cls._color(piece_char))
            case "Q" | "q":
                return Queen(color=cls._color(piece_char))
            case "K" | "k":
                return King(color=cls._color(piece_char))
            case _:
                raise ValueError(f"Invalid piece character: {piece_char}")

    def _color(self, piece_char: PieceChar) -> Color:
        return "white" if piece_char else "black"


class Piece(ABC):
    has_moved: bool

    def __init__(self, color: Color):
        self.color = color

    def possible_moves(
        self, board: "BoardRepr", file: File, rank: Rank
    ) -> set[tuple[File, Rank]]: ...


class Pawn(Piece):
    def possible_moves(self, board: "BoardRepr", file: File, rank: Rank):
        pass


class Knight(Piece):
    def possible_moves(self, board: "BoardRepr", file: File, rank: Rank):
        pass


class Bishop(Piece):
    def possible_moves(self, board: "BoardRepr", file: File, rank: Rank):
        pass


class Rook(Piece):
    def possible_moves(self, board: "BoardRepr", file: File, rank: Rank):
        pass


class Queen(Piece):
    def possible_moves(self, board: "BoardRepr", file: File, rank: Rank):
        pass


class King(Piece):
    def possible_moves(
        self, board: "BoardRepr", file: File, rank: Rank
    ):  # TODO być może powinien przyjmować board state
        pass


class BoardState(
    Protocol
):  # TODO widzi mi się coś w stylu observer pattern w checkmate - zamiast sprawdzać co ruch , wysyłać eventy
    def check(self) -> bool: ...
    def checkmate(self) -> bool: ...
    def stalemate(self) -> bool: ...
    def is_castling_possible(
        self, color: Color, side: Literal["king", "queen"]
    ) -> bool: ...
    def is_en_passant_possible(self, file: File, rank: Rank) -> bool: ...


class BoardRepr(Protocol):
    state: BoardState

    def __getitem__(self, file: File, rank: Rank) -> str: ...

    def __setitem__(self, file: File, rank: Rank, value: str): ...


class ListBoard:
    BOARD_SIZE = 8, 8

    def __init__(self, board: list[list[PieceChar | None]]):
        self._board = board

    def __getitem__(self, file: File, rank: Rank) -> str:
        rank_index, file_index = Notation.as_index(rank, file)
        return self._board[rank_index][file_index]

    def __setitem__(self, file: File, rank: Rank, value: str):
        rank_index, file_index = Notation.as_index(rank, file)
        self._board[rank_index][file_index] = value

    def initialize_pieces(self):
        self._board[0] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        self._board[1] = ["P"] * 8
        self._board[6] = ["p"] * 8
        self._board[7] = ["r", "n", "b", "q", "k", "b", "n", "r"]

    def possible_moves(self, file: File, rank: Rank):
        piece = PieceFactory(self[file, rank])
        return piece.possible_moves(self, file, rank)


class ChessBoard:
    def __init__(self, board: BoardRepr):
        self._board = board


if __name__ == "__main__":
    pass
