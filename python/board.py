# -*- coding:utf-8 -*- 

import copy

from chess import *
from element import *

# 对应pieces
class Board:
    def __init__(self):
        self.black_and_white = 0

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        # 返回轮到谁下了
        (last_player, pieces) = state
        this_player = 'w' if last_player == 'b' else 'b'
        return this_player

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        (last_player,pieces) = state

        pieces_copy = [i[:] for i in pieces]
        
        this_player = 'w' if last_player == 'b' else 'b'

        # 下了solution这一步之后的pieces
        new_pieces = put_piece(play, this_player, pieces_copy)
        return (this_player,new_pieces)

    def legal_plays(self, state):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        (last_player,pieces) = state
        this_player = 'w' if last_player == 'b' else 'b'
        (solutions, flips) = next_possible_steps(pieces,this_player)
        return solutions

    def winner(self, state):
        '''
        Takes a sequence of game states representing the full
        game history.  If the game is now won, return the player
        number.  If the game is still ongoing, return zero.  If
        the game is tied, return a different distinct value, e.g. -1.
        last_state = state_history[-1]
        '''
        (player, pieces) =  state

        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if not pieces[i][j] == 'n' :
                    if pieces[i][j] == 'b':
                        black += 1
                    else:
                        white += 1

        if black > white:
            return 'b'
        elif black < white:
            return 'w'
        else:
            return 't'
