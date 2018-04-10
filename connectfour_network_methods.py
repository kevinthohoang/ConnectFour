from collections import namedtuple
import socket

ConnectFourConnection = namedtuple(
    "ConnectFourConnection",
    ["socket", "socket_in", "socket_out"])

class ConnectFourError(Exception):
    pass


def connect(host: str, port: int) -> ConnectFourConnection:
    """ Given the correct host and port, connect to the Connect Four Server
    """
    connectfour_socket = socket.socket()
    connectfour_socket.connect((host, port))

    connectfour_socket_in  = connectfour_socket.makefile("r")
    connectfour_socket_out = connectfour_socket.makefile("w")

    return ConnectFourConnection(
        socket     = connectfour_socket,
        socket_in  = connectfour_socket_in,
        socket_out = connectfour_socket_out)

def disconnect(connection: ConnectFourConnection) -> None:
    """ Close the connection to the Connect Four Server
    """
    connection.socket_in.close()
    connection.socket_out.close()
    connection.socket.close()

def identify_user(connection: ConnectFourConnection, username: str) -> None:
    """ Identify ourselves by applying username with the correct protocol phrase
    """
    _write_line(connection, "I32CFSP_HELLO " + username)
    _expect_line(connection, "WELCOME " + username)

def start_ai_game(connection: ConnectFourConnection) -> None:
    """ Start a game with the server's artificial intelligence w/ "AI_GAME" phrase
    """
    _write_line(connection, "AI_GAME")
    _expect_line(connection, "READY")
    print("Starting AI game")

def send_move(connection: ConnectFourConnection, move: str) -> str:
    """ Send user's move to the server
    """
    _write_line(connection, move)
    
    if _valid_action(move) == True:
        expected = expect_line(connection, ["OKAY", "INVALID"])
        print(expected)

        if expected == "OKAY":
            ai_move = _expect_move(connection)
            print(ai_move)
            print(_expect_line(connection, ["READY", "WINNER_YELLOW", "WINNER_RED"]))
            return ai_move
        if expected == "INVALID":
            print(_expect_line(connection, ["READY"]))
    else:
        print(_expect_line(connection, ["INVALID"]))
        print(_expect_line(connection, ["READY"]))

def _valid_action(move: str) -> bool:
    """ Determine whether or not action is valid
    """
    if move.lower().startswith("drop") or move.lower().startswith("pop"):
        return True
    else:
        return False
    
def _expect_move(connection: ConnectFourConnection) -> str:
    """ Expect computer to reply with DROP or POP move. Make sure they
        respond appropriately.
    """
    line = _read_line(connection)

    if not line.startswith("DROP") or line.startswith("POP"):
        raise ConnectFourError

    return line
    
    
#------------------------------------------------------------------
def _read_line(connection: ConnectFourConnection) -> str:
    '''
    Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
    return connection.socket_in.readline()[:-1]

def _expect_line(connection: ConnectFourConnection, expected: [str]) -> str:
    '''
    Reads a line of text sent from the server, expecting it to contain
    a particular text.  If the line of text received is different, this
    function raises an exception; otherwise, the function has no effect.
    '''
    line = _read_line(connection)

    for expect in expected:
        if line == expect:
            return line
        if expect == len(expected):
            raise ConnectFourError()

def _write_line(connection: ConnectFourConnection, line: str) -> None:
    '''
    Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    connection.socket_out.write(line + '\r\n')
    connection.socket_out.flush()
