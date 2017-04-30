# -*- coding:utf-8 -*- 

import copy

from chess import *
from element import *

# 对应pieces
class Board:
    def __init__(self):
        self.stage = 0
        # black - white
        self.deficit = 0 

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        # 返回轮到谁下了
        (last_player,pieces) = state
        this_player = 'w' if last_player == 'b' else 'b'
        return this_player

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        (last_player,pieces) = state
        pieces_copy = [ i[:] for i in pieces ]
        # new_pieces = copy.deepcopy(pieces)
        this_player = 'w' if last_player == 'b' else 'b'
        
        #(solutions, flips) = next_possible_steps(pieces, this_player)
        
        #if play in solutions:

        # 下了solution这一步之后的pieces
        new_pieces = put_piece(play, this_player, pieces_copy)
        return (this_player,new_pieces)
        
        #else:
        #    pass

    def legal_plays(self, state):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        (last_player,pieces) = state
        this_player = 'w' if last_player == 'b' else 'b'
        (solutions, flips) = next_possible_steps(pieces,this_player)
        return solutions

    def winner(self, state):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        # last_state = state_history[-1]
        (player,pieces) =  state

        white_corner = 0
        black_corner = 0
        black_and_white = 0
        for i in range(8):
            for j in range(8):
                if pieces[i][j]!='n':
                    black_and_white += 1
                    if (i,j) in ((0,0),(0,7),(7,0),(7,7)):
                        if pieces[i][j]=='b':
                            black_corner += 1
                        else:
                            white_corner += 1

        if (black_corner+white_corner>self.stage) and black_and_white<=36:
            # if white_corner>black_corner:
            #     return 'w'
            # if black_corner>white_corner:
            #     return 'b'
            if black_corner - white_corner > self.deficit:
                return 'b'
            else:
                return 'w'

        next_player = 'w' if player == 'b' else 'b'
        # 判断结束
        (solutions,flips) = next_possible_steps(pieces, next_player)
        if solutions:
            return False
        else:
            (solutions,flips) = next_possible_steps(pieces, player)
            if solutions:
                return False
            else:
                # 双方没得下，游戏结束
                black = 0
                white = 0
                for i in range(8):
                    for j in range(8):
                        if not pieces[i][j] == 'n' :
                            if pieces[i][j] == 'b':
                                black += 1
                            else:
                                white += 1

                if black>white:
                    return 'b'
                elif black < white:
                    return 'w'
                else:
                    return 't'











