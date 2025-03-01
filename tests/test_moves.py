from game.board import Board, Position
import pytest


def test_possible_moves_for_pawn__white_initial_position():
    board = Board()
    board.initialize_board()

    assert board.possible_moves("a2") == {
        Position.from_algebraic_notation("a3"),
        Position.from_algebraic_notation("a4"),
    }
    assert board.possible_moves("b2") == {
        Position.from_algebraic_notation("b3"),
        Position.from_algebraic_notation("b4"),
    }
    assert board.possible_moves("c2") == {
        Position.from_algebraic_notation("c3"),
        Position.from_algebraic_notation("c4"),
    }
    assert board.possible_moves("d2") == {
        Position.from_algebraic_notation("d3"),
        Position.from_algebraic_notation("d4"),
    }
    assert board.possible_moves("e2") == {
        Position.from_algebraic_notation("e3"),
        Position.from_algebraic_notation("e4"),
    }
    assert board.possible_moves("f2") == {
        Position.from_algebraic_notation("f3"),
        Position.from_algebraic_notation("f4"),
    }
    assert board.possible_moves("g2") == {
        Position.from_algebraic_notation("g3"),
        Position.from_algebraic_notation("g4"),
    }
    assert board.possible_moves("h2") == {
        Position.from_algebraic_notation("h3"),
        Position.from_algebraic_notation("h4"),
    }


def test_possible_moves_for_pawn__black_initial_position():
    board = Board()
    board.initialize_board()

    assert board.possible_moves("a7") == {
        Position.from_algebraic_notation("a6"),
        Position.from_algebraic_notation("a5"),
    }
    assert board.possible_moves("b7") == {
        Position.from_algebraic_notation("b6"),
        Position.from_algebraic_notation("b5"),
    }
    assert board.possible_moves("c7") == {
        Position.from_algebraic_notation("c6"),
        Position.from_algebraic_notation("c5"),
    }
    assert board.possible_moves("d7") == {
        Position.from_algebraic_notation("d6"),
        Position.from_algebraic_notation("d5"),
    }
    assert board.possible_moves("e7") == {
        Position.from_algebraic_notation("e6"),
        Position.from_algebraic_notation("e5"),
    }
    assert board.possible_moves("f7") == {
        Position.from_algebraic_notation("f6"),
        Position.from_algebraic_notation("f5"),
    }
    assert board.possible_moves("g7") == {
        Position.from_algebraic_notation("g6"),
        Position.from_algebraic_notation("g5"),
    }
    assert board.possible_moves("h7") == {
        Position.from_algebraic_notation("h6"),
        Position.from_algebraic_notation("h5"),
    }
