from board import Board


def test_possible_moves_for_pawn__white_initial_position():
    board = Board()
    board.initialize_board()

    assert board.possible_moves("a", 2) == {"a3", "a4"}
    # assert board.possible_moves("b2") == {"b3", "b4"}
    # assert board.possible_moves("c2") == {"c3", "c4"}
    # assert board.possible_moves("d2") == {"d3", "d4"}
    # assert board.possible_moves("e2") == {"e3", "e4"}
    # assert board.possible_moves("f2") == {"f3", "f4"}
    # assert board.possible_moves("g2") == {"g3", "g4"}
    # assert board.possible_moves("h2") == {"h3", "h4"}


#
#
# def test_possible_moves_for_pawn__black_initial_position():
#     board = Board()
#     board.initialize_board()
#
#     assert board.possible_moves("a7") == {"a5", "a6"}
#     assert board.possible_moves("b7") == {"b5", "b6"}
#     assert board.possible_moves("c7") == {"c5", "c6"}
#     assert board.possible_moves("d7") == {"d5", "d6"}
#     assert board.possible_moves("e7") == {"e5", "e6"}
#     assert board.possible_moves("f7") == {"f5", "f6"}
#     assert board.possible_moves("g7") == {"g5", "g6"}
#     assert board.possible_moves("h7") == {"h5", "h6"}
