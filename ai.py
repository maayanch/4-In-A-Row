###############################################################################
# FILE : ai.py
# WRITER :
# maayan chetrit , maayanchetrit , 315512715
# lea khodorkovski, lea.khodo, 312250392
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : this file containing class that responsible to play instead of
# human player .
###############################################################################


###############################################################################
# Imports
###############################################################################
import random

###############################################################################
# Constants
###############################################################################
NO_POSIBLLE_MOVES = "No possible AI moves"

TOP_ROW_OF_THE_BOARD = 0


class AI:
    """the class AI :
    responsible to act like a human and play against other user. the class
    chose random possible slots and send to the other player the move. """

    def find_legal_move(self, g, func, timeout=None):
        """The method get the following parameters:
        g: object Game() of the current running game
        func: a function that make a single move in the game
        return: the location in the board game of the move(row and col)
        The method find legal move and make it"""
        board_game = g.get_board_game()
        # getting the top row in the board (witch have the last slots to
        # fill in each column)
        top_row = board_game[TOP_ROW_OF_THE_BOARD]
        # getting one of the free slots - one of the columns that not full
        col_of_free_slot = self.__get_free_slot(top_row)
        # if there is not a free slot in the board raise Exception
        if col_of_free_slot == None:
            raise Exception(NO_POSIBLLE_MOVES)
        # there is a free slot on the board
        row, col = func(col_of_free_slot), col_of_free_slot
        return row, col

    def __get_free_slot(self, top_board_row):
        """ The method get top_row_board (list), check if there is
        slot with the value 'None'(means free slot), if there is return the
        number of the col of the slot(if there more than 1 choose randomly)
        if there is not return None """
        lst_free_slots = []
        for i in range(len(top_board_row)):
            if top_board_row[i] is None:
                lst_free_slots.append(i)
        # if there isn't a free slot
        if lst_free_slots == []:
            return None
        col = random.choice(lst_free_slots)
        return col

    def get_random_free_col(self, board):
        """this function looking for relevant column, by checking the top
        row.None tops row means that the column is possible """
        top_row = board[TOP_ROW_OF_THE_BOARD]
        return self.__get_free_slot(top_row)



