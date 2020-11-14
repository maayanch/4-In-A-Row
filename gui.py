###############################################################################
# FILE : gui.py
# WRITER :
# maayan chetrit , maayanchetrit , 315512715
# lea khodorkovski, lea.khodo, 312250392
# EXERCISE :this file contains the class GuiBoard that responsible to  show
# the graphics of the game to the user. and send and process a massage from
# other users.
###############################################################################


###############################################################################
# IMPORT
###############################################################################
import tkinter as tk
from game import Game
import communicator

###############################################################################
# CONSTANT
###############################################################################
A_I = 'ai'
BUUTON_WIDTH = 10
PLACE_ON_COORD_Y = 20
PLACE_ON_COORD_X = 860
BUTTON_COLOR_WHEN_CLICKED = "pink"
BUTTON_COLOR = 'khaki'
BUTTON_EXIT_TEXT = "Quit Game"
COORD_Y_PLACE = 0
COORD_X_PLACE = 0
PLACE_OF_IMAGE = 'nw'
CIRCLE_WIDTH = 3
OUT_LINE_COLOR = 'white'
COL_PLACE = 0
ROW_PLACE = 1
TEXT_LOCATION_X = 450
TEXT_LOCATION_Y = 20
PREFIX_MASSAGE = 'The winner is: '
TEKO_NO_WINNER = 'no one'
PLAYER_ONE = 'player one'
PLAYER_TWO = 'player two'
START_PLACE_OF_COORD_Y_2 = 140
START_PLACE_OF_COORD_X_2 = 200
START_PLACE_OF_COORD_Y_1 = 40
START_PLACE_OF_COORD_X_1 = 100
MARGE_COLOR = 'olivedrab4'
HOMER_COLOR = 'firebrick3'
CORRECT_LOCATION_Y = -5
CORRECT_LOCATION_X = 10
NUM_OF_SECONDS = 2300
HEIGHT = 700
WIDTH = 900
END_RIGHT_EDGE = 900
START_RIGHT_EDGE = 800
END_LEFT_EDGE = 100
START_LEFT_EDGE = 0


class GuiBoard:
    """The class responsible for the graphic design of the game, the
    presentation of the vertical state of the board, the declaration of victory
    or an illegal move, and send and receive messages from the other user,
    and process the messages"""

    def __init__(self, root, game, port, player_type, ai, ip=None):
        self.__root = root
        self.__game = game
        self.__ai = ai
        self.__canvas_board = None
        self.__homer = tk.PhotoImage(file="homer.gif")
        self.__marge = tk.PhotoImage(file="marge.gif")
        self.__illegal_move = tk.PhotoImage(file="illegal_move.gif")
        self.__homer_wins = tk.PhotoImage(file="homer_winner.gif")
        self.__marge_wins = tk.PhotoImage(file="marge_winner.gif")
        self.__draw = tk.PhotoImage(file="teko.gif")
        self.__background = tk.PhotoImage(file="sofa.gif")
        self.__game_is_over = False
        self.__player_type = None
        self.__set_player(ip)
        self.__communicator = communicator.Communicator(self.__root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__response_to_message)
        self.__human_or_ai = player_type
        self.__current_player = Game.PLAYER_ONE
        self.__winner = False

    ###############################################################################
    # get method:
    # return the praivte object of the class to other classes
    ###############################################################################
    def get_player_type(self):
        return self.__player_type

    def get_canvas_board(self):
        return self.__canvas_board

    def get_type_of_player(self):
        return self.__human_or_ai

    def get_current_player(self):
        return self.__current_player

    ###############################################################################

    def create_board(self):
        """function that make a graphical board for the game "4 in row-The
        Simpson , the function make 7 columns and 6 rows by circle,
        and place a background to the 'game board' .
         the game board is a canvas ,and each place on the board described
         by coordination """
        self.__canvas_board = tk.Canvas(self.__root, width=WIDTH,
                                        height=HEIGHT)
        self.__canvas_board.create_image(COORD_X_PLACE, COORD_Y_PLACE,
                                         anchor=PLACE_OF_IMAGE,
                                         image=self.__background)
        self.__canvas_board.pack()
        # this for loops make the circle in the wanted way
        for col in range(Game.NUM_COLS):
            for row in range(Game.NUM_ROWS):
                x_1, x_2, y_1, y_2 = self.get_coords(col, row)
                self.__canvas_board.create_oval(x_1, y_1, x_2, y_2)

    def __set_player(self, ip):
        """ The method get self and the ip address(String). 
        And according to if there is a ip(that not None) set the self.player.
        returns: None"""
        # if the ip is None means its the server, witch means its player one
        if ip is None:
            self.__player_type = Game.PLAYER_ONE
        # if there is ip means its the client, witch means its player two
        else:
            self.__player_type = Game.PLAYER_TWO

    def get_column(self, coord_x):
        """function that get location in coordination x , and calculate the
        col of the given place. the function return the column number and
        not the coordination."""
        for col in range(Game.NUM_COLS):
            for row in range(Game.NUM_ROWS):
                x_1, x_2, y_1, y_2 = self.get_coords(col, row)
                if x_1 <= coord_x <= x_2:
                    return col
        # if the given coord_x is in the edge
        return None

    def get_coords(self, row, col):
        """function that get row and column and calculate the corners
        location on the canvas """
        x_1 = START_PLACE_OF_COORD_X_1 + START_PLACE_OF_COORD_X_1 * row
        y_1 = START_PLACE_OF_COORD_Y_1 + START_PLACE_OF_COORD_X_1 * col
        x_2 = START_PLACE_OF_COORD_X_2 + START_PLACE_OF_COORD_X_1 * row
        y_2 = START_PLACE_OF_COORD_Y_2 + START_PLACE_OF_COORD_X_1 * col
        return x_1, x_2, y_1, y_2

    def change_current_player(self):
        """function that change the current player , return None"""
        if self.__current_player == Game.PLAYER_TWO:
            self.__current_player = Game.PLAYER_ONE
        else:
            self.__current_player = Game.PLAYER_TWO

    def __response_to_message(self, message):
        """function that get a message from the other player and process his
        massage. the function update the other player moves in the board,
        and responsible to check if the other player won."""
        # the message is always from the another player
        column = int(message)
        row = self.__game.make_move(column)
        self.add_player_to_gui(column, row, self.__current_player)
        self.change_current_player()
        if self.__human_or_ai == A_I:
            row, col = self.__ai.find_legal_move(self.__game,
                                                 self.__game.make_move)
            self.add_player_to_gui(col, row, self.__current_player)
            self.change_current_player()
        self.check_for_winner()

    def __mark_winner_slots(self, list_of_places):
        """function that get a list of tuples that represent the place of
        the winner and mark thous place so the user can see who is the
        winner """
        for index in range(len(list_of_places)):
            x_1, x_2, y_1, y_2 = self.get_coords(
                list_of_places[index][ROW_PLACE],
                list_of_places[index][COL_PLACE])
            self.__canvas_board.create_oval(x_1, y_1, x_2, y_2,
                                            outline=OUT_LINE_COLOR,
                                            width=CIRCLE_WIDTH)

    def check_for_winner(self):
        """function that checks for winner. if the winner already founds,
        return None. else, the function  prompt for the winner and ends the
        game"""
        if self.__winner:
            # means that if the winner founds, do not check again and serch
            # for winner .
            return
        winner = self.__game.get_winner()
        if winner is not None:  # means winner is player 1/2 or draw.
            self.__game.flag_that_game_over()
            self.__prompt_winner(winner)
            self.__game_is_over = True

    def add_player_to_gui(self, col, row, player_to_put):
        """function that get  col, row and player , and add the player to
        rhe wanted place by the given col and row.
        the function mark each player with a different color and a different
        image"""
        if self.__game_is_over:
            return
        if player_to_put == Game.PLAYER_ONE:
            img = self.__homer
            color = HOMER_COLOR
        else:
            img = self.__marge
            color = MARGE_COLOR
        x_1, x_2, y_1, y_2 = self.get_coords(col, row)
        self.__canvas_board.create_oval(x_1, y_1, x_2, y_2, fill=color)
        # correct coords so the image will be in the midlle of the circle
        x_coord, y_coord = self.__correct_coord(x_1, x_2, y_1, y_2)
        self.__canvas_board.create_image(x_coord, y_coord, image=img)
        # send massage to the other player so he could add the current chice
        # to his board .
        if player_to_put == self.__player_type and not self.__game_is_over:
            self.__communicator.send_message(str(col))

    def __prompt_winner(self, winner):
        """function that get a winner , and prompt the appropriate image(the
        image that fit to the winner. the function also add an exit button
        and mark the winner slots"""
        if winner == Game.PLAYER_TWO:
            img = self.__marge_wins
            winner_name = PLAYER_TWO
        elif winner == Game.PLAYER_ONE:
            img = self.__homer_wins
            winner_name = PLAYER_ONE
        else:  # winner == Game.DRAW:
            img = self.__draw
            winner_name = TEKO_NO_WINNER
        massage = PREFIX_MASSAGE + winner_name
        # add the winner name to the canvas board:
        self.__canvas_board.create_text(TEXT_LOCATION_X, TEXT_LOCATION_Y,
                                        text=massage)
        self.__prompt_image_by_time(img)
        self.__add_exit_button()
        self.__mark_winner_slots(self.__game.get_winner_place())
        # update the object that the winner is founds
        self.__winner = True

    def __add_exit_button(self):
        """helper function that adds an exit button in thee end of the game"""
        exit_button = tk.Button(self.__root, text=BUTTON_EXIT_TEXT,
                                command=self.__game_over)
        exit_button.configure(width=BUUTON_WIDTH, background=BUTTON_COLOR,
                              activebackground=BUTTON_COLOR_WHEN_CLICKED)
        self.__canvas_board.create_window(PLACE_ON_COORD_X, PLACE_ON_COORD_Y,
                                          window=exit_button)

    def __game_over(self):
        """function that ends the game by destroy the root"""
        self.__root.destroy()

    def prompt_illegal_move(self):
        """function that get a massage , and use one of the class's function
        to prompt the image with the massage """
        self.__prompt_image_by_time(self.__illegal_move)

    def __prompt_image_by_time(self, img):
        """helper function use for prompt a photo for a few second.
        the function
        create a label with photo , and than delete it"""
        self.helper_lable = tk.Label(self.__canvas_board, image=img)
        self.helper_lable.pack()
        self.helper_lable.after(NUM_OF_SECONDS, self.__delete_the_label)

    def __delete_the_label(self):
        """helper function that destroy the label"""
        self.helper_lable.destroy()

    def __correct_coord(self, x_1, x_2, y_1, y_2):
        """function that get 2 coord on the board that represents the circle
        location, and calculate and return the center of the circle Including
        correction of standard deviation  """
        x_coord = ((x_1 + x_2) / 2) + CORRECT_LOCATION_X
        # calculate the average of the given coordination and add the
        # correction of standard deviation
        y_coord = ((y_1 + y_2) / 2) + CORRECT_LOCATION_Y
        return x_coord, y_coord

    def check_if_in_edge(self, coord_x):
        """function that get a coord_x and make sure that the clicked was not
        done in the edge of the canvas. mean that the clicked place connected to
        some column """
        if START_LEFT_EDGE < coord_x < END_LEFT_EDGE or \
                START_RIGHT_EDGE < coord_x < END_RIGHT_EDGE:
            return True
        else:
            return False
