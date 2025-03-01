from abc import ABC
from dataclasses import dataclass, field
from enum import Enum


class Offsets:
    move: list[tuple[int, int]]
    special_attack: list[tuple[int, int]]
    first_move: list[tuple[int, int]]

    def __init__(
        self,
        move_or_attack: list[tuple[int, int]],
        special_attack: list[tuple[int, int]],
        first_move: list[tuple[int, int]],
    ):
        self.move_or_attack = move_or_attack
        self.special_attack = special_attack
        self.first_move = first_move

    def __add__(self, other: "Offsets") -> "Offsets":
        return Offsets(
            move_or_attack=self.move_or_attack + other.move_or_attack,
            special_attack=self.special_attack + other.special_attack,
            first_move=self.first_move + other.first_move,
        )


DIAGONAL_OFFSETS = Offsets(
    move_or_attack=[(1, 1), (1, -1), (-1, 1), (-1, -1)],
    special_attack=[],
    first_move=[],
)
STRAIGHT_OFFSETS = Offsets(
    move_or_attack=[(1, 0), (0, 1), (-1, 0), (0, -1)],
    special_attack=[],
    first_move=[],
)
KNIGHT_OFFSETS = Offsets(
    move_or_attack=[
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ],
    special_attack=[],
    first_move=[],
)
WHITE_PAWN_OFFSETS = Offsets(
    move_or_attack=[(-1, 0)],
    special_attack=[(-1, 1), (-1, -1)],
    first_move=[(-2, 0)],
)
BLACK_PAWN_OFFSETS = Offsets(
    move_or_attack=[(1, 0)],
    special_attack=[(1, 1), (1, -1)],
    first_move=[(2, 0)],
)


class Color(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class PieceState:  # TODO defended?
    has_moved: bool = False
    pinned: bool = False


@dataclass
class Piece(ABC):
    color: Color
    white_unicode: str = field(init=False)
    black_unicode: str = field(init=False)
    offsets: Offsets = field(init=False)
    ranged: bool = False
    state: PieceState = field(default_factory=PieceState, init=False)

    def __repr__(self) -> str:
        return self.white_unicode if self.is_white else self.black_unicode

    @property
    def is_white(self) -> bool:
        return self.color == Color.WHITE


@dataclass
class Pawn(Piece):
    white_unicode: str = "♙"
    black_unicode: str = "♟"

    def __post_init__(self):
        self.offsets: Offsets = (
            WHITE_PAWN_OFFSETS if self.is_white else BLACK_PAWN_OFFSETS
        )


@dataclass
class Rook(Piece):
    white_unicode = "♖"
    black_unicode = "♜"
    offsets = STRAIGHT_OFFSETS


@dataclass
class Knight(Piece):
    white_unicode = "♘"
    black_unicode = "♖"

    def __post_init__(self):
        self.offsets: Offsets = KNIGHT_OFFSETS


@dataclass
class Bishop(Piece):
    white_unicode = "♗"
    black_unicode = "♝"

    def __post_init__(self):
        self.offsets: Offsets = DIAGONAL_OFFSETS
        self.ranged = True


@dataclass
class Queen(Piece):
    white_unicode = "♕"
    black_unicode = "♛"

    def __post_init__(self):
        self.offsets: Offsets = STRAIGHT_OFFSETS + DIAGONAL_OFFSETS
        self.ranged = True


@dataclass
class King(Piece):
    white_unicode = "♔"
    black_unicode = "♚"

    def __post_init__(self):
        self.offsets: Offsets = STRAIGHT_OFFSETS + DIAGONAL_OFFSETS
