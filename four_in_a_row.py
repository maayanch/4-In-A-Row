###############################################################################
# FILE : four_in_a_row.py
# WRITER :
# maayan chetrit , maayanchetrit , 315512715
# lea khodorkovski, lea.khodo, 312250392
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION :this file is the main file that responsible to run the game
# and connect between all the other classes
###############################################################################


###############################################################################
# import
###############################################################################
import tkinter as tk
from game import Game
from gui import GuiBoard
from ai import AI
import sys
import socket

###############################################################################
# constant
###############################################################################
HUMAN = 'human'
A_I = 'ai'
SERVER = "Server"
CLIENT = "Client"
MOUSE_CLICK = "<Button-1>"
MIN_PORT_NUM_ALOUD = 1000
MAX_PORT_NUM = 65535
LEN_OF_CLIENT_ARGUMENTS = 4
IP_ADDRESS = 3
LEN_OF_SERVER_ARGUMENTS = 3
PORT = 2
PLAYER_TYPE = 1


class RunGame:
    """about RunGame :
    RunGame is the class who combines the game rules implemented in "Game"
    and the graphics implemented in the GUI. also , this class also connect
    between the ai class , in case the user wants to play against ai.  """
    def __init__(self, gui, game):
        self.__game = game
        self.__gui = gui
        self.__run_game(gui, game)

    def __run_game(self, gui, game):
        """the function that responsible to run the game , create the board,
        and add the chice of the user by helper function  """
        gui.create_board()
        if type_of_player == HUMAN:
            gui.get_canvas_board().bind(MOUSE_CLICK, self.send_to_add_player)
        elif type_of_player == A_I:
            #do the first movement
            col = ai.get_random_free_col(game.get_board_game())
            #make sure that ai found col.
            if col != None:
                self.send_to_add_player(col)

    def send_to_add_player(self, col):
        """The method get self and col and check if the turn to play now is
        the turn of the the player that run this specific running. if it is
        make the move if not dos not do anything """
        if gui.get_player_type() == gui.get_current_player():
            self.add_player(col)

    def add_player(self, event):
        """function that get an event(clicked place on the board) and process
        the clicked. the function aim is to connect between the classes game
         and gui, and the player to both of the classes,
        """
        if game.get_game_is_not_over:   # means that the game is not over and
            # allow to
                                # click on the board
            current_player = gui.get_current_player()
            if type_of_player == HUMAN:
                clicked_location_x = event.x
                if gui.check_if_in_edge(clicked_location_x):
                    # if the clicked location is in the edge ,
                    # add nothing to the board.
                    return
                col_x = clicked_location_x
            else:  # event=col from ai
                col_x = event
                # if the player is ai , the event is the col
            self.add_the_player_to_game_and_gui(col_x, current_player)
            gui.check_for_winner()

    def add_the_player_to_game_and_gui(self, param_col,
                                       current_player):
        """function that get a col  and player, and adds the player to the
        col. the function send to Game.make_move the col number and gwt the
        wanted row or, None , if None means that the col was full , and the
        player make an illegal move , else means that make_move returns a
        row and we need to add it to the game by the given row and col. than ,
        change the current player """
        if type_of_player == 'human':
            col = gui.get_column(param_col)
            row = game.make_move(col)
            if row == None:  # means that clicked place is illegal
                gui.prompt_illegal_move()
        else:  # type_of_player == 'ai'
            row, col = ai.find_legal_move(game, game.make_move)
        if current_player == Game.PLAYER_ONE:
            gui.add_player_to_gui(col, row, Game.PLAYER_ONE)
        else: # player is  player 2
            gui.add_player_to_gui(col, row, Game.PLAYER_TWO)
        gui.change_current_player()


def arguments_are_valid(all_input_argv):
    """ The function gets the input arguments and checks their validity. if
    all valid return True, otherwise return False"""
    # if there to many or not enough arguments return False
    num_of_given_arguments = len(all_input_argv)
    if num_of_given_arguments < LEN_OF_SERVER_ARGUMENTS or \
            num_of_given_arguments > LEN_OF_CLIENT_ARGUMENTS:
        return False
    # if the argument that represent the player type is not a human or ai
    # return False
    player_type = all_input_argv[PLAYER_TYPE]
    if player_type != HUMAN and player_type != A_I:
        return False
    # if the port argument is not valid
    port_number = int(all_input_argv[2])
    if port_number > MAX_PORT_NUM or port_number < MIN_PORT_NUM_ALOUD:
        return False
    # means all the argument are valid and return True
    return True


if __name__ == '__main__':
    root = tk.Tk()
    game = Game()
    if arguments_are_valid(sys.argv):
        type_of_player = sys.argv[PLAYER_TYPE]
        if type_of_player == A_I:
            ai = AI()
        else:
            ai = None
        port = int(sys.argv[PORT])
        # if the arguments without ip argument means its the server
        server = len(sys.argv) == LEN_OF_SERVER_ARGUMENTS
        if server:
            gui = GuiBoard(root, game, port, type_of_player, ai)
            root.title(SERVER)
        else:
            # it is the client
            gui = GuiBoard(root, game, port, type_of_player, ai,
                           sys.argv[IP_ADDRESS])
            root.title(CLIENT)
        Run = RunGame(gui, game)
        root.mainloop()
