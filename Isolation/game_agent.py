"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - 2*opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - 3*opp_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):

        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        self.best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return self.best_move

    def minimax(self, game, depth):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return self.min_max_move(game, depth)[0]
    
    # TODO: finish this function!
    def min_max_move(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return (game.get_player_location(self), self.score(game, self))
        
        best_value, funct = None, None
        
        if game.get_legal_moves():
            best_move = game.get_legal_moves()[0]
        else:
            best_move = (-1, -1)
        
        if(game.active_player == self):
            funct, best_value = max, float("-inf")
        else:
            funct, best_value = min, float("inf")
            
        for move in game.get_legal_moves():
            next_play = game.forecast_move(move)
            score = self.min_max_move(next_play, depth - 1)[1]
            if funct(best_value, score) == score:
                best_move = move
                best_value = score

        return (best_move, best_value)
            
            


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
       
        self.time_left = time_left

        # TODO: finish this function!
        best_move = (-1, -1)
        search_depth = 1
        while True:
            try:
                best_move = self.alphabeta(game, search_depth)
                search_depth += 1
            except SearchTimeout:
                break
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
       
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return self.ab_move(game, depth)[0] 
        # TODO: finish this function!
    
    def ab_move(self,game,depth, alpha=float("-inf"), beta=float("inf")):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0:
            return ((-1, -1), self.score(game, self))
        
        best_value, funct, is_alpha = None, None, True
        
        if game.get_legal_moves():
            best_move = game.get_legal_moves()[0]
        else:
            best_move = (-1, -1)
        
        if(game.active_player == self):
            funct, best_value, is_alpha = max, float("-inf"), True
        else:
            funct, best_value, is_alpha = min, float("inf"), False
        
        legal_moves = game.get_legal_moves()
        
        for move in legal_moves:
            next_play = game.forecast_move(move)
            score = self.ab_move(next_play, depth - 1, alpha, beta)[1]
                
            if is_alpha:
                if(score > best_value):
                    best_value = score
                    best_move = move 
                if best_value >= beta:
                    return best_move, best_value
                else:
                    alpha = max(best_value, alpha)
            else:
                if(score < best_value):
                    best_value = score
                    best_move = move 
                if best_value <= alpha:
                    return best_move, best_value
                else:
                    beta = min(best_value, beta)

        return best_move, best_value
        
