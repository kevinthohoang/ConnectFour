import connectfour

def draw_game_board(board: [[str]]) -> None:
    """ For the 7x6 game board, draw the board for players to visualize their gameplay
    """
    for col_num in range(connectfour.BOARD_COLUMNS):
        print(col_num + 1, end = " ")
    print()

    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            if board[col][row] == connectfour.NONE:
                print(".", end = " ")
            else:
                print(board[col][row], end = " ")
        print()

def get_move(game_state: connectfour.ConnectFourGameState) -> str:
    """ Get player's desired move
    """
    print("\n", game_state.turn, ", it's your turn.", sep = "")
    return input("What would you like to do? ")

def apply_move(game_state: connectfour.ConnectFourGameState, move: str) -> connectfour.ConnectFourGameState:
    """ Apply player's move to current board
    """
    col = int(move[move.find(" ") + 1:])
    
    if move.lower().startswith("drop"):
        print()
        return connectfour.drop_piece(game_state, col - 1)
    elif move.lower().startswith("pop"):
        print()
        return connectfour.pop_piece(game_state, col - 1)
    else:
        print("INVALID MOVE")

def display_winner(game_state: connectfour.ConnectFourGameState) -> str:
    """ Display winner at the end of game
    """
    draw_game_board(game_state.board)
    winning_message = "Congratulations! " + \
                      connectfour._opposite_turn(game_state.turn) + \
                      ", you're the winner"
    return winning_message
