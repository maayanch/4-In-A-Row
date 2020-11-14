###############################################################################
# FILE : game.py
# WRITER :
# maayan chetrit , maayanchetrit , 315512715
# lea khodorkovski, lea.khodo, 312250392
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION :this file contain the class "Game" that responsible to Manage
# the proper course of the game.
###############################################################################

###############################################################################
# Constant
###############################################################################
LAST_POSSIBLE_ROW = 2
TOP_ROW = 0
NUM_OF_SLOTS_TO_WIN = 4
NUM_OF_ALL_SLOTS = 42


class Game:
    """about game:
    Game is the class who Manage the proper course of the game. game check
    for winner and decide about any slot if the player can put his disk or
    not."""

    ###########################################################################
    # Class Constants
    ###########################################################################

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    LAST_ROW = 5
    LAST_COL = 6
    NUM_ROWS = 6
    NUM_COLS = 7

    def __init__(self):
        self.__board_game = [[None] * (self.NUM_COLS) for rows in range(
            self.NUM_ROWS)]
        self.__last_player = self.PLAYER_TWO
        self.__count_moves = 0
        self.__game_is_not_over = True
        # ABOUT WINNER PLACE : in order to mark the winner place every time
        # we check for winner, we save the (row,col) as a possible place for
        #  the winner if we found out that there are no 4 slots with the
        # same player, reset the list .
        self.__winner_place = []

    ###########################################################################
    # get_method
    ###########################################################################

    def get_winner_place(self):
        return self.__winner_place

    def get_game_is_not_over(self):
        return self.get_game_is_not_over()

    def get_board_game(self):
        """The method return the board of the game"""
        return self.__board_game

    ###########################################################################
    def __set_last_player(self):
        """ The method change the last player to play to the other player.
        player two is 1(True) and player one is 0(False) so """
        self.__last_player = not self.__last_player

    def make_move(self, column):
        """ The method get self and column (int) and make the move in the
        game - put a disk in the board at the column input.
        the method returns the row of the location of tha disk that put in
        the board (if there is not place to put a disk in the board returns
        None)"""
        # if the column in the board is full returns None
        if not self.__check_if_available(column):
            return None
        player = self.get_current_player()
        row = self.__set_disk_to_the_board(player, column)
        self.__set_last_player()
        self.__count_moves += 1
        return row

    def flag_that_game_over(self):
        """function that ends the game when the game is over."""
        self.__game_is_not_over = not self.__game_is_not_over

    def __check_if_available(self, column):
        """function that get a column and check if it is possible to add a
        "player" to that column . if the top row on the given column is
        already taken its mean that all the column is full and we need to
        raise an exception """
        try:
            if self.__board_game[TOP_ROW][column] != None:
                raise Exception
            return True
        except Exception:
            return False

    def __set_disk_to_the_board(self, player, column):
        first_empty_place = 0
        # the while loop check for the first empty place in the board game
        # (first from the bottom of None slots in the input column) assuming
        #  there is an empty place
        while first_empty_place != self.LAST_ROW and \
                self.__board_game[first_empty_place][column] == None \
                and self.__board_game[first_empty_place + 1][column] == None:
            first_empty_place += 1
        self.__board_game[first_empty_place][column] = player
        return first_empty_place

    def get_winner(self):
        """ The method check if there is a winner (if there is 4 disks in a
        row or col or diagonal) if there is return the winner if there is
        not return None"""
        row_winner = self.__check_4_in_rows()
        if row_winner is not None:
            return row_winner
        col_winner = self.__check_4_in_cols()
        if col_winner is not None:
            return col_winner
        diago_up_winner = self.__check_4_in_diagonals_up()
        if diago_up_winner is not None:
            return diago_up_winner
        diago_down_winner = self.__check_4_in_diagonals_down()
        if diago_down_winner is not None:
            return diago_down_winner
        # if all the slots in the board are full means the game is over and
        # there is a draw
        if self.__count_moves == NUM_OF_ALL_SLOTS:
            return self.DRAW
        return None

    def __check_4_in_cols(self):
        """ The method check if there are 4 slots in sequence in a col
        with the same player. the method run from the row on the floor and
        check all the possible location (until row 3 , including row 3) if
        there is return the winner if there is not return None"""
        # for any col
        for col in range(self.NUM_COLS):
            # for any row (from the last to the top)
            for row in range(self.LAST_ROW, LAST_POSSIBLE_ROW, -1):
                player_at_slot = self.get_player_at(row, col)
                # if there is no player in the slot continue to the next col
                if player_at_slot == None:
                    break
                # if from the current slot and the next 3 slots up in the
                # same col have the same player return the winner
                if self.__if_4_in_col(row, col):
                    return player_at_slot
        return None

    def __if_4_in_col(self, start_row, start_col):
        """ The method get 2 parameters of the location of the slot,
        and check from this slot if the current slot and the next 3 slots
        up in the same col have the same player, if it is return True. If not
        return False """
        optional_winner = self.get_player_at(start_row, start_col)
        self.__winner_place.append((start_row, start_col))
        for i in range(NUM_OF_SLOTS_TO_WIN):
            if self.get_player_at(start_row - i, start_col) != optional_winner:
                self.__winner_place = []
                return False
            self.__winner_place.append((start_row - i, start_col))
        return True

    def __check_4_in_rows(self):
        """ The method check if there are 4 slots in sequence in a row
        with the same player.the method check all and only the possible
        location. if there is return the winner if there is not
        return None"""
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS - 3):
                player_at_slot = self.get_player_at(row, col)
                # if there is no player in the slot continue to the next col
                if player_at_slot == None:
                    continue
                # if from the current slot and the next 3 slots right in the
                # same row have the same player return the winner
                if self.__if_4_in_row(row, col):
                    return player_at_slot
        return None

    def __if_4_in_row(self, start_row, start_col):
        """ The method get 2 parameters of the location of the slot,
        and check from this slot if the current slot and the next 3 slots
        right in the same row have the same player if it is return True. If
        not return False """
        optional_winner = self.get_player_at(start_row, start_col)
        self.__winner_place.append((start_row, start_col))
        for i in range(NUM_OF_SLOTS_TO_WIN):
            if self.get_player_at(start_row, start_col + i) != optional_winner:
                self.__winner_place = []
                return False
            self.__winner_place.append((start_row, start_col + i))
        return True

    def __check_4_in_diagonals_down(self):
        """ The method check if there are 4 slots in sequence in a diagonal
        down with the same player. if there is return the winner if there is not
        return None"""
        for row in range(3):
            for col in range(4):
                player_at_slot = self.get_player_at(row, col)
                if player_at_slot == None:
                    continue
                if self.__if_4_in_diagonal_down(row, col):
                    return player_at_slot
        return None

    def __if_4_in_diagonal_down(self, start_row, start_col):
        """ The method get 2 parameters of the location of the slot,
        and check from this slot if the current slot and the next 3 slots
        in the direction of the diagonal down have the same
        player, if it is return True. If
        not return False """
        # assume that the player is not None
        optional_winner = self.get_player_at(start_row, start_col)
        self.__winner_place.append((start_row, start_col))
        # assume that there is 4 slots from the start slot in diagonal down
        for i in range(NUM_OF_SLOTS_TO_WIN):
            if self.get_player_at(start_row + i, start_col + i) != \
                    optional_winner:
                self.__winner_place = []
                return False
            self.__winner_place.append((start_row + i, start_col + i))
        return True

    def __check_4_in_diagonals_up(self):
        """ The method check if there are 4 slots in sequence in a diagonal
        up with the same player. if there is return the winner if there is not
        return None"""
        for row in range(self.LAST_ROW, LAST_POSSIBLE_ROW, -1):
            for col in range(NUM_OF_SLOTS_TO_WIN):
                player_at_slot = self.get_player_at(row, col)
                if player_at_slot == None:
                    continue
                if self.__if_4_in_diagonal_up(row, col):
                    return player_at_slot
        return None

    def __if_4_in_diagonal_up(self, start_row, start_col):
        """ The method get 2 parameters of the location of the slot,
         and check from this slot if the current slot and the next 3 slots
         in the direction of the diagonal up have the same
         player, if it is return True. If
         not return False """
        optional_winner = self.get_player_at(start_row, start_col)
        self.__winner_place.append((start_row, start_col))
        for i in range(NUM_OF_SLOTS_TO_WIN):
            if self.get_player_at(start_row - i,
                                  start_col + i) != optional_winner:
                self.__winner_place = []
                return False
            self.__winner_place.append((start_row - i, start_col + i))
        return True

    def get_player_at(self, row, col):
        """ The method get row and col and return the player that in the
        given location (row, col) on the board of the game."""
        return self.__board_game[row][col]

    def get_current_player(self):
        """ The method get the player that it is his turn to play and return
        the player"""
        player = self.PLAYER_ONE
        # if the last player is PLAYER_TWO means it 1(True) so change to
        # PLAYER_TWO
        if not self.__last_player:
            player = Game.PLAYER_TWO
        return player
###############################################################################
