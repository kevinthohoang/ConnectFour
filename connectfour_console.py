import connectfour_shared_methods
import connectfour

def _run_user_interface() -> None:
    """ Main method for running player vs. player
    """
    current_game_state = connectfour.new_game_state()

    while connectfour.winning_player(current_game_state) == connectfour.NONE:
        current_game_state = player_turn(current_game_state)

    print(connectfour_shared_methods.display_winner(current_game_state))

def player_turn(game_state: connectfour.ConnectFourGameState) -> connectfour.ConnectFourGameState:
    """ Contains the logic for a player's turn
    """
    while True:
        try:
            connectfour_shared_methods.draw_game_board(game_state.board)
            return connectfour_shared_methods.apply_move(
                        game_state, connectfour_shared_methods.get_move(game_state))
        except:
            print("\nINVALID MOVE\n")
            
if __name__ == '__main__':
    _run_user_interface()
