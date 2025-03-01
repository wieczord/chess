from dataclasses import dataclass, field
from enum import Enum
# class Offset:

DIAGONAL_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
STRAIGHT_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
KNIGHT_OFFSETS = [
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
]
WHITE_PAWN_OFFSETS = {
    "first_move": [(-2, 0)],
    "move": [(-1, 0)],
    "attack": [(-1, 1), (-1, -1)],
}

BLACK_PAWN_OFFSETS = {
    "first_move": [(2, 0)],
    "move": [(1, 0)],
    "attack": [(1, 1), (1, -1)],
}


class Color(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class PieceState:
    has_moved: bool = False
    pinned: bool = False


@dataclass
class Piece:
    color: Color
    white_unicode: str
    black_unicode: str
    offsets: list[tuple[int, int]]
    ranged: bool = False
    state: PieceState = field(default_factory=PieceState)

    def __init__(self, color: Color):
        self.is_white = color == Color.WHITE
        self.color = color

    def __repr__(self) -> str:
        return self.white_unicode if self.is_white else self.black_unicode


class Pawn(Piece):
    white_unicode: str = "♙"
    black_unicode: str = "♟"
    offsets: list[tuple[int, int]] = WHITE_PAWN_OFFSETS


class Rook(Piece):
    white_unicode = "♖"
    black_unicode = "♜"
    offsets = STRAIGHT_OFFSETS


class Knight(Piece):
    white_unicode = "♘"
    black_unicode = "♖"

    def __post_init__(self):
        self.offsets: list[tuple[int, int]] = KNIGHT_OFFSETS


class Bishop(Piece):
    white_unicode = "♗"
    black_unicode = "♝"

    def __post_init__(self):
        self.offsets: list[tuple[int, int]] = DIAGONAL_OFFSETS
        self.ranged = True


class Queen(Piece):
    white_unicode = "♕"
    black_unicode = "♛"

    def __post_init__(self):
        self.offsets: list[tuple[int, int]] = STRAIGHT_OFFSETS + DIAGONAL_OFFSETS
        self.ranged = True


class King(Piece):
    white_unicode = "♔"
    black_unicode = "♚"

    def __post_init__(self):
        self.offsets: list[tuple[int, int]] = STRAIGHT_OFFSETS + DIAGONAL_OFFSETS
