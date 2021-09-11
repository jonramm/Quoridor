# Name: Jonathan Ramm- Gramenz
# Date: 8/12/21
# Description: Defines a QuoridorGame class for playing the Quoridor game. Also defines Player, Board, and GameState
# classes to work with QuoridorGame to implement game elements.


class QuoridorGame:
    """Creates a game object for Quoridor. Handles all pertinent game functionality by communicating with the Board,
    Player, and GameState classes by instantiating them and calling heir own class methods. Includes get methods for
    all private data members plus methods for moving a pawn, changing whose turn it is, placing a fence,
    and determining if a player has won. There are also helper methods for moving pawns and placing fences. """

    def __init__(self):
        """Initializes the elements of the game, the two players as Player class objects with their name (P1 or P2)
        and position, a fair player Player object for use in the fair play method,  the game board as a Board class
        object which holds a representation of the board and a dictionary of space locations, and the game state as a
        GameState class object which holds whose turn it is and if there's a winner. """
        self._board = Board()
        self._p1 = Player((4, 0), "P1")
        self._p2 = Player((4, 8), "P2")
        self.fair_player = Player((0, 0), "")
        self._game_state = GameState()

    def get_board(self):
        """Get method for game board object."""
        return self._board

    def get_p1(self):
        """Get method for P1 object."""
        return self._p1

    def get_p2(self):
        """Get method for P2 object."""
        return self._p2

    def get_game_state(self):
        """Get method for game state object."""
        return self._game_state

    def change_turn(self):
        """Sets turn to next player."""
        self._game_state.change_turn()

    def move_pawn(self, player_num, coord_tuple):
        """player_num parameter is an integer that indicates who is moving, and coord_tuple is where they will move.
        If the move is forbidden or blocked by a fence, returns False. If the move is successful or the player wins,
        returns True. If the game has already been won, return False. Uses helper method to get the appropriate
        player object. Uses the GameState class object to determine if the game has been won or not, and the Board
        class object to validate and move the pawn. """
        if player_num == 1:
            return self.help_move_pawn(self._p1, coord_tuple)
        if player_num == 2:
            return self.help_move_pawn(self._p2, coord_tuple)

    def help_move_pawn(self, player, coord_tuple):
        """Helper method for move_pawn that takes a new coordinates tuple plus the player object in order to use
        Player class methods on the correct player to retrieve data. Checks if the game has already been won, if it's
        the correct player's turn, then calls the validate_pawn method to make sure the move is legal. If so, it
        calls move_pawn to change the board representation, change_turn to update whose tuen it is, and
        determine_game_state to see if there's been a winner."""
        if self._game_state.get_game_state() is None:                           # if the game hasn't been won
            if player.get_player_name() == self.get_game_state().get_turn():    # if it's the correct player's turn
                if self._board.validate_pawn(player, coord_tuple) is True:      # if the move is valid
                    self._board.move_pawn(player, coord_tuple)
                    self._game_state.change_turn()
                    self._game_state.determine_game_state(self._board, player)
                    return True
        return False

    def place_fence(self, player_num, direction, coord_tuple):
        """Takes an integer that represents the player number (1 or 2), whether the fence is to be placed vertically
        or horizontally (v or h), and a tuple containing the coordinates where the fence will be placed. If player
        has no fence left, or if the fence is out of the boundaries of the board, or if there is already a fence
        there and the new fence will overlap or intersect with the existing fence, returns False. If the fence can be
        placed, returns True. If the game has already won returns False. Uses helper method to get the appropriate
        Player object and ascertain how many fences they have remaining and decrement their total if fence is placed.
        Helper method also Uses GameState object to determine if there's been a winner and Board class object to
        validate and place fence. """
        if player_num == 1:
            return self.help_place_fence(self._p1, self._p2, direction, coord_tuple)
        if player_num == 2:
            return self.help_place_fence(self._p2, self._p1, direction, coord_tuple)

    def help_place_fence(self, player, other_player, direction, coord_tuple):
        """Helper method for place_fence which takes direction and new coordinates tuple, plus the correct player
        object to more easily access Player class data and methods. Checks to see if the game has been won already,
        if it's the correct player's turn, if the player has any remaining fences, then calls the validate_fence
        method to make sure the fence placement is legal. If so, it calls place_fence to change the board
        representation and then fair_play to make sure the other player has a valid path to their goal line. If
        the fair play rule has been violated it returns "breaks the fair play rule" then calls remove_fence to update
        the game board. If fair play has not been violated it changes whose turn it is and decrements the player's
        remaining fences."""
        if self._game_state.get_game_state() is None:                           # if the game hasn't been won
            if player.get_player_name() == self.get_game_state().get_turn():    # if it's the correct player's turn
                if player.get_fences_remaining() > 0:                           # if the player still has fences
                    if self._board.validate_fence(direction, coord_tuple) is True:      # if fence placement is valid
                        self._board.place_fence(direction, coord_tuple)
                        if self._board.fair_play(other_player, self.fair_player) is True:    # fair play validation
                            self._game_state.change_turn()
                            player.dec_fences_remaining()
                            return True
                        else:
                            self._board.remove_fence(direction, coord_tuple)
                            return "breaks the fair play rule"
        return False

    def is_winner(self, player_num):
        """Takes an integer that represents the player number (1 or 2) to access the appropriate Player class object
        then calls the Player class method get_winning() to see if they've won. Returns True if they have,
        False if they haven't. """
        if player_num == 1:
            return self._p1.get_winning()
        elif player_num == 2:
            return self._p2.get_winning()
        else:
            return False


class Board:
    """Creates, stores, and displays board data. The board holds all fence and pawn positions. Since the board data
    contains more rows than the actual game board in order to represent horizontal fences, I've included a dictionary
    with coordinates for the game board as keys that correspond to the coordinates in my board representation. I've
    also included find_space and set_space methods that translates between the two to handle placement of objects on
    the board. """

    def __init__(self):
        """Initializes game board. There are extra rows between the rows where you can place the pawns for placement
        of horizontal fences. The whole board is surrounded by fences and each space in the rows where horizontal
        fences can be placed contains a '+' to visually represent the top left corner of a valid space. """
        self._board = [["+==", "+==", "+==", "+==", "+==", "+==", "+==", "+==", "+==+"],
                       ["|  ", "   ", "   ", "   ", " P1", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", "   ", "   ", "   ", "   ", "   |"],
                       ["+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  ", "+  +"],
                       ["|  ", "   ", "   ", "   ", " P2", "   ", "   ", "   ", "   |"],
                       ["+==", "+==", "+==", "+==", "+==", "+==", "+==", "+==", "+==+"]]

        self._spaces = {"(0, 0)": (1, 0),           # keys are the game board set of coordinates, corresponding data
                        "(1, 0)": (1, 1),           # are the coordinates in my board data array
                        "(2, 0)": (1, 2),
                        "(3, 0)": (1, 3),
                        "(4, 0)": (1, 4),
                        "(5, 0)": (1, 5),
                        "(6, 0)": (1, 6),
                        "(7, 0)": (1, 7),
                        "(8, 0)": (1, 8),
                        "(0, 1)": (3, 0),
                        "(1, 1)": (3, 1),
                        "(2, 1)": (3, 2),
                        "(3, 1)": (3, 3),
                        "(4, 1)": (3, 4),
                        "(5, 1)": (3, 5),
                        "(6, 1)": (3, 6),
                        "(7, 1)": (3, 7),
                        "(8, 1)": (3, 8),
                        "(0, 2)": (5, 0),
                        "(1, 2)": (5, 1),
                        "(2, 2)": (5, 2),
                        "(3, 2)": (5, 3),
                        "(4, 2)": (5, 4),
                        "(5, 2)": (5, 5),
                        "(6, 2)": (5, 6),
                        "(7, 2)": (5, 7),
                        "(8, 2)": (5, 8),
                        "(0, 3)": (7, 0),
                        "(1, 3)": (7, 1),
                        "(2, 3)": (7, 2),
                        "(3, 3)": (7, 3),
                        "(4, 3)": (7, 4),
                        "(5, 3)": (7, 5),
                        "(6, 3)": (7, 6),
                        "(7, 3)": (7, 7),
                        "(8, 3)": (7, 8),
                        "(0, 4)": (9, 0),
                        "(1, 4)": (9, 1),
                        "(2, 4)": (9, 2),
                        "(3, 4)": (9, 3),
                        "(4, 4)": (9, 4),
                        "(5, 4)": (9, 5),
                        "(6, 4)": (9, 6),
                        "(7, 4)": (9, 7),
                        "(8, 4)": (9, 8),
                        "(0, 5)": (11, 0),
                        "(1, 5)": (11, 1),
                        "(2, 5)": (11, 2),
                        "(3, 5)": (11, 3),
                        "(4, 5)": (11, 4),
                        "(5, 5)": (11, 5),
                        "(6, 5)": (11, 6),
                        "(7, 5)": (11, 7),
                        "(8, 5)": (11, 8),
                        "(0, 6)": (13, 0),
                        "(1, 6)": (13, 1),
                        "(2, 6)": (13, 2),
                        "(3, 6)": (13, 3),
                        "(4, 6)": (13, 4),
                        "(5, 6)": (13, 5),
                        "(6, 6)": (13, 6),
                        "(7, 6)": (13, 7),
                        "(8, 6)": (13, 8),
                        "(0, 7)": (15, 0),
                        "(1, 7)": (15, 1),
                        "(2, 7)": (15, 2),
                        "(3, 7)": (15, 3),
                        "(4, 7)": (15, 4),
                        "(5, 7)": (15, 5),
                        "(6, 7)": (15, 6),
                        "(7, 7)": (15, 7),
                        "(8, 7)": (15, 8),
                        "(0, 8)": (17, 0),
                        "(1, 8)": (17, 1),
                        "(2, 8)": (17, 2),
                        "(3, 8)": (17, 3),
                        "(4, 8)": (17, 4),
                        "(5, 8)": (17, 5),
                        "(6, 8)": (17, 6),
                        "(7, 8)": (17, 7),
                        "(8, 8)": (17, 8)
                        }

    def get_board(self):
        """Get method for game board."""
        return self._board

    def display_board(self):
        """Displays game board in it's current state to the console."""
        for row in self._board:
            line = ""
            for space in row:
                line += space
            print(line)

    def find_space(self, coord_tuple, horizontal=False):
        """Takes a new coordinates tuple and returns that space as it is represented in my board data. Extracts x and
        y coordinates from my _spaces dictionary and sets them to variables for cleaner code. Default horizontal
        value is False for all operations except horizontal fence placement. """
        x_coord = self._spaces[str(coord_tuple)][0]
        y_coord = self._spaces[str(coord_tuple)][1]
        if horizontal is False:
            return self._board[x_coord][y_coord]
        else:
            return self._board[x_coord-1][y_coord]      # accessing fence row above pawn placement row

    def set_space(self, coord_tuple, space_object):
        """Takes a new coordinates tuple and the string to be added to that space. Uses my_spaces dictionary to
        translate the coord_tuple to the proper representation. If the string is a representation of a horizontal
        fence it analyzes that condition and acts accordingly. """
        x_coord = self._spaces[str(coord_tuple)][0]
        y_coord = self._spaces[str(coord_tuple)][1]
        if "+" in space_object:
            self._board[x_coord-1][y_coord] = space_object      # If horizontal fence, accesses row above
        else:
            self._board[x_coord][y_coord] = space_object

    def validate_pawn(self, player, coord_tuple):
        """Validates pawn movement by first checking if the new coordinates are off the board. If not, it proceeds to
        check to see if the move is only attempting to move the allotted single space. If so, checks to see if
        there's a fence or pawn blocking it's path. It then checks to see if a pawn is attempting to move two spaces.
        If so it will check to see if the other pawn is adjacent and there is no fence on the other side for a jump.
        It then checks to see if a diagonal move is attempted. If so, it will check to see if the other pawn is
        adjacent, a fence is behind it, and if the diagonal move is not blocked by a fence. All directional
        validation will be handled by sub methods. """
        x_coord = coord_tuple[0]
        y_coord = coord_tuple[1]
        x_change = x_coord - player.get_position()[0]
        y_change = y_coord - player.get_position()[1]
        if 0 <= x_coord <= 8 and 0 <= y_coord <= 8:                        # are new coordinates within boundaries
            if (x_change == -1 or x_change == -2) and y_change == 0:       # attempting to move left one or two spaces
                return self.check_move_left(player, coord_tuple, x_change)
            if (x_change == 1 or x_change == 2) and y_change == 0:         # attempting to move right one or two spaces
                return self.check_move_right(coord_tuple, x_change)
            if (y_change == -1 or y_change == -2) and x_change == 0:       # attempting to move up one or two spaces
                return self.check_move_up(player, coord_tuple, y_change)
            if (y_change == 1 or y_change == 2) and x_change == 0:         # attempting to move down one or two spaces
                return self.check_move_down(player, coord_tuple, y_change)
            if abs(x_change) == 1 and abs(y_change) == 1:                  # attempting to move diagonally one space
                return self.check_diagonal(player, coord_tuple, x_change, y_change)
        return False

    def check_move_left(self, player, coord_tuple, x_change):
        """Takes a player object, new coordinate tuple, and checks to see if a left move is valid. Returns True if
        valid and False if not. """
        if abs(x_change) == 2:              # are we jumping
            if "P" in self.find_space((coord_tuple[0] + 1, coord_tuple[1])):            # is the other player adjacent
                if "|" not in self.find_space((coord_tuple[0] + 1, coord_tuple[1])):
                    if self.find_space(player.get_position())[0] != "|":
                        return True
        else:
            if self.find_space(player.get_position())[0] == " ":            # is a fence in the way?
                if self.find_space(coord_tuple) == "   " or "|  ":          # is the target space clear?
                    return True
        return False

    def check_move_right(self, coord_tuple, x_change):
        """Takes a player object, new coordinate tuple, and checks to see if a right move is valid. Returns True if
        valid and False if not. """
        if abs(x_change) == 2:      # are we jumping
            if "P" in self.find_space((coord_tuple[0] - 1, coord_tuple[1])):        # is the other player adjacent
                if "|" not in self.find_space((coord_tuple[0] - 1, coord_tuple[1])):
                    if self.find_space(coord_tuple)[0] != "|":
                        return True
        else:
            if (self.find_space(coord_tuple) == "   " or
                    self.find_space(coord_tuple) == "   |"):         # is a fence in the way?
                return True
        return False

    def check_move_up(self, player, coord_tuple, y_change):
        """Takes a player object, new coordinate tuple, and checks to see if an up move is valid. Returns True if
        valid and False if not. """
        if abs(y_change) == 2:          # are we jumping
            if "P" in self.find_space((coord_tuple[0], coord_tuple[1] + 1)):        # is the other player adjacent
                if "=" not in self.find_space((coord_tuple[0], coord_tuple[1] + 1), True):
                    if "=" not in self.find_space(player.get_position(), True):
                        return True
        else:
            if self.find_space(coord_tuple) == "   " or "|  ":                  # is the target space clear?
                if "=" not in self.find_space(player.get_position(), True):     # is there no fence in the way?
                    return True
        return False

    def check_move_down(self, player, coord_tuple, y_change):
        """Takes a player object, new coordinate tuple, and checks to see if a down move is valid. Returns True if
        valid and False if not. """
        if abs(y_change) == 2:          # are we jumping
            if "P" in self.find_space((coord_tuple[0], coord_tuple[1] - 1)):        # is other player adjacent
                if "=" not in self.find_space((player.get_position()[0], player.get_position()[1] + 1), True):
                    if "=" not in self.find_space(coord_tuple, True):
                        return True
        else:
            if self.find_space(coord_tuple) == "   " or "|  " or "   |":           # is the target space clear?
                if "=" not in self.find_space(coord_tuple, True):
                    return True
        return False

    def check_diagonal(self, player, coord_tuple, x_change, y_change):
        """Helper method that takes a player object, new coordinates tuple, the change in x axis value,
        and the change in y axis value and routes the data to the proper sub sub method for diagonal move validation.
        """
        if y_change == -1:
            if x_change == 1:
                return self.check_up_right_diagonal(player, coord_tuple)
            if x_change == -1:
                return self.check_up_left_diagonal(player, coord_tuple)
        if y_change == 1:
            if x_change == 1:
                return self.check_down_right_diagonal(player, coord_tuple)
            if x_change == -1:
                return self.check_down_left_diagonal(player, coord_tuple)

    def check_up_right_diagonal(self, player, coord_tuple):
        """Takes a player object, new coordinates tuple, and checks to see if an up right diagonal move is valid.
        Only valid if player is blocked directly by other player's pawn. """
        if "P" in self.find_space((player.get_position()[0], player.get_position()[1] - 1)):
            if "+==" in self.find_space((player.get_position()[0], player.get_position()[1] - 1), True):
                if self.find_space(player.get_position(), True) != "+==":
                    if "|" not in self.find_space(coord_tuple):
                        if "P" not in self.find_space(coord_tuple):
                            return True
        if "P" in self.find_space((player.get_position()[0] + 1, player.get_position()[1])):
            if "|" not in self.find_space(coord_tuple):
                if "=" not in self.find_space((player.get_position()[0] + 1, player.get_position()[1]), True):
                    if "P" not in self.find_space(coord_tuple):
                        return True
        return False

    def check_up_left_diagonal(self, player, coord_tuple):
        """Takes a player object, new coordinates tuple, and checks to see if an up left diagonal move is valid. Only
        valid if player is blocked directly by other player's pawn. """
        if "P" in self.find_space((player.get_position()[0], player.get_position()[1] - 1)):
            if "=" not in self.find_space(player.get_position(), True):
                if self.find_space((player.get_position()[0], player.get_position()[1] - 1))[0] != "|":
                    if "P" not in self.find_space(coord_tuple):
                        return True
        if "P" in self.find_space((player.get_position()[0] - 1, player.get_position()[1])):
            if "|" not in self.find_space(player.get_position()):
                if "=" not in self.find_space((player.get_position()[0] - 1, player.get_position()[1]), True):
                    if "P" not in self.find_space(coord_tuple):
                        return True
        return False

    def check_down_right_diagonal(self, player, coord_tuple):
        """Takes a player object, new coordinates tuple, and checks to see if a down right diagonal move is valid.
        Only valid if player is blocked directly by other player's pawn. """
        if "P" in self.find_space((player.get_position()[0], player.get_position()[1] + 1)):
            if "+==" not in self.find_space((player.get_position()[0], player.get_position()[1] + 1), True):
                if self.find_space(coord_tuple, True) != "+==":
                    if "|" not in self.find_space(coord_tuple):
                        if "P" not in self.find_space(coord_tuple):
                            return True
        if "P" in self.find_space((player.get_position()[0] + 1, player.get_position()[1])):
            if "|" not in self.find_space(coord_tuple):
                if "=" not in self.find_space(coord_tuple, True):
                    if "P" not in self.find_space(coord_tuple):
                        return True
        return False

    def check_down_left_diagonal(self, player, coord_tuple):
        """Takes a player object, new coordinates tuple, and checks to see if a down left diagonal move is valid.
        Only valid if player is blocked directly by other player's pawn. """
        if "P" in self.find_space((player.get_position()[0], player.get_position()[1] + 1)):
            if "=" not in self.find_space((player.get_position()[0], player.get_position()[1] + 1), True):
                if self.find_space((player.get_position()[0], player.get_position()[1] + 1))[0] != "|":
                    if "P" not in self.find_space(coord_tuple):
                        return True
        if "P" in self.find_space((player.get_position()[0] - 1, player.get_position()[1])):
            if "|" not in self.find_space(player.get_position()):
                if "=" not in self.find_space(coord_tuple, True):
                    if "P" not in self.find_space(coord_tuple):
                        return True
        return False

    def validate_fence(self, direction, coord_tuple):
        """Takes a fence direction, new coordinate tuple, and validates fence placement by using find_space method to
        ascertain a particular space on the board and checking it for other fences. Returns True if valid,
        false if not. """
        x_coord = coord_tuple[0]
        y_coord = coord_tuple[1]
        if direction == "v":                                            # vertical validation
            if 1 <= x_coord <= 8 and 0 <= y_coord <= 8:                 # are new coordinates within boundaries
                return self.check_vertical_placement(coord_tuple)
        if direction == "h":
            if 0 <= x_coord <= 8 and 1 <= y_coord <= 8:                 # are new coordinates within boundaries
                return self.check_horizontal_placement(coord_tuple)

    def check_vertical_placement(self, coord_tuple):
        """Takes the new coordinate tuple and checks if a vertical fence placement is valid. Returns True if valid,
        false if not. """
        if len(self.find_space(coord_tuple)) == 3:
            if "|" not in self.find_space(coord_tuple):
                return True
        if len(self.find_space(coord_tuple)) == 4:          # right edge spaces
            if self.find_space(coord_tuple)[0] == " ":
                return True
        return False

    def check_horizontal_placement(self, coord_tuple):
        """Takes the new coordinate tuple and checks if a horizontal fence placement is valid. Returns True if valid,
        false if not. """
        if "=" not in self.find_space(coord_tuple, True):
            return True
        return False

    def move_pawn(self, player, coord_tuple):
        """Takes a Player object and new coordinates tuple and changes pawn's location on the board while clearing
        the pawn's previous space. Uses find_space() to locate the real position on the board and set_space() to
        change the space we're moving to. Validation occurs elsewhere so there's no need to crunch those numbers
        here. """
        if "|" in self.find_space(player.get_position()):
            self.move_with_fence_in_space(player, coord_tuple)         # if player is vacating a space with a fence
        else:
            self.set_space(player.get_position(), "   ")
            if self.find_space(coord_tuple) == "   ":
                self.set_space(coord_tuple, " " + player.get_player_name())
            if self.find_space(coord_tuple) == "   |":
                self.set_space(coord_tuple, " " + player.get_player_name() + "|")
            if self.find_space(coord_tuple)[0] == "|":
                self.set_space(coord_tuple, "|" + player.get_player_name())
        player.set_position(coord_tuple)

    def move_with_fence_in_space(self, player, coord_tuple):
        """Used in move_pawn() to clear previously occupied spaces and inhabit new spaces. Takes a player object and
        new coordinates tuple. Takes player name data from player object for use in reprinting spaces."""
        if len(self.find_space(player.get_position())) == 3:
            self.set_space(player.get_position(), "|  ")                                # clear
            if self.find_space(coord_tuple) == "   ":
                self.set_space(coord_tuple, " " + player.get_player_name())             # reprint
            elif self.find_space(coord_tuple)[-1] == "|":
                self.set_space(coord_tuple, " " + player.get_player_name() + "|")       # reprint
            else:
                self.set_space(coord_tuple, "|" + player.get_player_name())             # reprint
        else:
            if len(self.find_space(player.get_position())) == 4:          # if player is in a right edge space
                if self.find_space(player.get_position())[0] == " ":
                    self.set_space(player.get_position(), "   |")                       # clear
                if self.find_space(player.get_position())[0] == "|":
                    self.set_space(player.get_position(), "|  |")
            if self.find_space(coord_tuple) == "   ":
                self.set_space(coord_tuple, " " + player.get_player_name())             # reprint
            else:
                if self.find_space(coord_tuple) == "|  ":
                    self.set_space(coord_tuple, "|" + player.get_player_name())         # reprint
                else:
                    self.set_space(coord_tuple, " " + player.get_player_name() + "|")   # reprint

    def place_fence(self, direction, coord_tuple):
        """Takes direction and a new coordinates tuple and places a fence on the game board using the set_space
        method. """
        if direction == "v":
            self.set_space(coord_tuple, "|" + self.find_space(coord_tuple)[1:])
        if direction == "h":
            if len(self.find_space(coord_tuple)) == 3:
                self.set_space(coord_tuple, "+==")
            else:                                           # if it's a right edge
                self.set_space(coord_tuple, "+==+")

    def remove_fence(self, direction, coord_tuple):
        """Takes a fence direction and new coordinates tuple and removes a fence if that fence violated the fair play
        rule. """
        if direction == "v":
            self.set_space(coord_tuple, " " + self.find_space(coord_tuple)[1:])
        if direction == "h":
            if self.find_space(coord_tuple, True) == "+==":
                self.set_space(coord_tuple, "+  ")
            else:
                self.set_space(coord_tuple, "+  +")

    def fair_play_iterate(self, player, memo=None):
        """Takes the fair_player object and moves it around the board to see if a path to the goal line is open.
        Returns True if so and False if not. Keeps iterating through memo list and checking those coordinates against
        the fair_player position to see if moves are valid and if so it adds those coordinates to memo. If it has
        iterated through all coordinates without adding any more it will return False because there are no more legal
        moves to achieve a win. """
        if memo is None:
            memo = [player.get_position()]
        for coords in memo:
            player.set_position(coords)
            x_coord = coords[0]
            y_coord = coords[1]
            if player.get_player_name() == "P1":
                if coords[1] == 8:
                    return True
            if player.get_player_name() == "P2":
                if coords[1] == 0:
                    return True
            self.append_memo(player, x_coord, y_coord, memo)
        return False

    def append_memo(self, player, x_coord, y_coord, memo):
        """Takes a player object, x and y coordinates, the memo list, and calls methods for testing spaces that are
        one space orthogonally, two spaces orthogonally, or diagonal. """
        self.append_single_space_move(player, x_coord, y_coord, memo)
        self.append_diagonal_move(player, x_coord, y_coord, memo)
        self.append_jump_move(player, x_coord, y_coord, memo)

    def append_single_space_move(self, player, x_coord, y_coord, memo):
        """Checks the validity of moving to each neighboring space and adds it to memo if valid."""
        if (x_coord - 1, y_coord) not in memo:
            if self.validate_pawn(player, (x_coord - 1, y_coord)) is True:
                memo.append((x_coord - 1, y_coord))
        if (x_coord, y_coord - 1) not in memo:
            if self.validate_pawn(player, (x_coord, y_coord - 1)) is True:
                memo.append((x_coord, y_coord - 1))
        if (x_coord + 1, y_coord) not in memo:
            if self.validate_pawn(player, (x_coord + 1, y_coord)) is True:
                memo.append((x_coord + 1, y_coord))
        if (x_coord, y_coord + 1) not in memo:
            if self.validate_pawn(player, (x_coord, y_coord + 1)) is True:
                memo.append((x_coord, y_coord + 1))

    def append_diagonal_move(self, player, x_coord, y_coord, memo):
        """Checks the validity of moving diagonally and adds to memo if valid."""
        if (x_coord - 1, y_coord - 1) not in memo:
            if self.validate_pawn(player, (x_coord - 1, y_coord - 1)) is True:
                memo.append((x_coord - 1, y_coord - 1))
        if (x_coord - 1, y_coord + 1) not in memo:
            if self.validate_pawn(player, (x_coord - 1, y_coord + 1)) is True:
                memo.append((x_coord - 1, y_coord + 1))
        if (x_coord + 1, y_coord + 1) not in memo:
            if self.validate_pawn(player, (x_coord + 1, y_coord + 1)) is True:
                memo.append((x_coord + 1, y_coord + 1))
        if (x_coord + 1, y_coord - 1) not in memo:
            if self.validate_pawn(player, (x_coord + 1, y_coord - 1)) is True:
                memo.append((x_coord + 1, y_coord - 1))

    def append_jump_move(self, player, x_coord, y_coord, memo):
        """Checks the validity of potential two space moves (jumps) and adds those to memo if valid."""
        if (x_coord - 2, y_coord) not in memo:
            if self.validate_pawn(player, (x_coord - 2, y_coord)) is True:
                memo.append((x_coord - 2, y_coord))
        if (x_coord, y_coord - 2) not in memo:
            if self.validate_pawn(player, (x_coord, y_coord - 2)) is True:
                memo.append((x_coord, y_coord - 2))
        if (x_coord + 2, y_coord) not in memo:
            if self.validate_pawn(player, (x_coord + 2, y_coord)) is True:
                memo.append((x_coord + 2, y_coord))
        if (x_coord, y_coord + 2) not in memo:
            if self.validate_pawn(player, (x_coord, y_coord + 2)) is True:
                memo.append((x_coord, y_coord + 2))

    def fair_play(self, player, fair_player):
        """Fair play helper method that copies the player object to be tested into the fair_player object for
        movement around the board. """
        fair_player.set_player_name(player.get_player_name())
        fair_player.set_position(player.get_position())
        return self.fair_play_iterate(fair_player)


class GameState:
    """Keeps track of the current state of the game, who's turn it is and if a player has won. The
    determine_game_state method uses the Board class object to obtain board data, and analyzes it for winning
    conditions. """

    def __init__(self):
        """Initializes game state and turn private data members."""
        self._game_state = None
        self._turn = "P1"

    def get_turn(self):
        """Get method for player turn."""
        return self._turn

    def get_game_state(self):
        """Get method for game_state."""
        return self._game_state

    def determine_game_state(self, board, player):
        """Takes the game board and determines if there's a winner, changing the game state data member."""
        for space in board.get_board()[1]:
            if "P2" in space:
                self._game_state = "P2"
                player.set_winning()

        for space in board.get_board()[17]:
            if "P1" in space:
                self._game_state = "P1"
                player.set_winning()

    def change_turn(self):
        """Changes whose turn it is."""
        if self._turn == "P1":
            self._turn = "P2"
        else:
            self._turn = "P1"


class Player:
    """Creates a player object that contains private data members for position, name, fences remaining, and winning.
    Contains methods for getting and setting data members and one for decrementing a player's number of fences
    remaining. """
    def __init__(self, position, player_name):
        """Initializes player position, name ("P1" or "P2), number of fences remaining, and if they've won. """
        self._position = position
        self._player_name = player_name
        self._fences_remaining = 10
        self._winning = False

    def get_position(self):
        """Get method for position."""
        return self._position

    def set_position(self, new_position):
        """Takes new position coordinates and sets the Player object's current position to those coordinates. """
        self._position = new_position

    def get_player_name(self):
        """Get method for player name."""
        return self._player_name

    def set_player_name(self, name):
        """Set method for player name."""
        self._player_name = name

    def get_fences_remaining(self):
        """Get method for number of fences remaining."""
        return self._fences_remaining

    def dec_fences_remaining(self):
        """Reduces number of fences remaining by 1."""
        self._fences_remaining -= 1

    def get_winning(self):
        """Get method for whether a player has won."""
        return self._winning

    def set_winning(self):
        """Changes a player's _winning variable to True."""
        self._winning = True
