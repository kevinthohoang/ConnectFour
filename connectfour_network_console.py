import connectfour_shared_methods
import connectfour_network_methods
import connectfour

CONNECTFOUR_HOST = "woodhouse.ics.uci.edu"
CONNECTFOUR_PORT = 4444

def _run_user_interface() -> None:
    """ Main method for running player vs. computer player
    """
    username = _get_valid_username()

    connection = connectfour_network_methods.connect(CONNECTFOUR_HOST, CONNECTFOUR_PORT)

    try:
        connectfour_network_methods.identify_user(connection, username)
        connectfour_network_methods.start_ai_game(connection)
        
        current_game_state = connectfour.new_game_state()

        while connectfour.winning_player(current_game_state) == connectfour.NONE:
            connectfour_shared_methods.draw_game_board(current_game_state)
            move = connectfour_shared_methods.get_move(current_game_state)
            
            try:
                current_game_state = connectfour_shared_methods.apply_move(
                                        current_game_state, get_move(current_game_state))
            except:
                print("INVALID MOVE!")

            try:
                ai_move = None
                ai_move = connectfour_network_methods.send_move(connect, move)

                if ai_move == None:
                    pass
                else:
                    current_game_state = connectfour_shared_methods.apply_move(current_game_state, ai_move)
            except:
                print("Server made an invalid move. Disconnecting...")
                connectfour_network_methods.disconnect(connect)
                break


                
        print(connectfour_shared_methods.winning_message(current_game_state)
            
    finally:
        connectfour_network_methods.disconnect(connection)
    
def _get_valid_username() -> str:
    """ ASk user for a valid username
        *Username cannot contain white spaces
    """
    while True:
        username = input("What is your name? ")
        if " " in username:
            print("Invalid username! Please enter one without spaces.\n")
        else:
            return username

if __name__ == '__main__':
    _run_user_interface()
