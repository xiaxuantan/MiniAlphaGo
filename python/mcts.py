# -*- coding:utf-8 -*- 
from __future__ import division

from random import choice
from math import log, sqrt
import datetime
import copy

from board import *
import chess
import element

# 把state从指针的二维数组变为string类型
def state_to_string(state):

    (player, pieces) = state
    s = ''
    for i in range(8):
        for j in range(8):
            if not pieces[i][j] == None:
                s += pieces[i][j].color
            else:
                s += 'n'

    return s

class MonteCarlo:
    def __init__(self, board):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.

        # state: 包含了player信息，棋盘信息

        self.board = board
        # state的结构是(player,pieces)，其中pieces是棋盘状态，player是导致当先棋盘的玩家
        self.states = []
        # 模拟的时间限制
        self.calculation_time = datetime.timedelta(seconds=5)
        # 模拟中的最大步数
        self.max_moves = 64
        # 记录某个中间状态对应的模拟数、模拟中赢的盘数的字典
        self.plays = {}
        self.wins = {}
        # UCB1的参数，先从根号2开始，目前来看越小越好
        self.C = 0.001

    def update(self, state):
        # Takes a game state, and appends it to the history.
        
        self.states.append(state)

    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]
        # player 是 'w' or 'b'

        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])
        # (player,pieces)
        # Bail out early if there is no real choice to be made.
        if not legal:
            return None
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1
        print '************************'
        print games
        #print '************************'
        #print self.plays.values()
        #print '************************'
        #print self.wins.values()

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]
    
        # Pick the move with the highest percentage of wins.
        # player是造成state S的玩家
        percent_wins, move = max((self.wins.get((player, state_to_string(S)), 0)/self.plays.get((player, state_to_string(S)), 1), p) for p, S in moves_states)

        return move

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        
        visited_states = set()
        states_copy = copy.deepcopy(self.states[:]) 
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in xrange(self.max_moves):
            # legal：从state出发的可行步
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            # 选择p，以及state更新为选择了p后的状态
            if len(moves_states)!=0 and all([plays.get((player, state_to_string(S))) for p, S in moves_states]):
                # If we have stats on all of the legal moves here, use them.
                summation = sum([plays[(player, state_to_string(S))] for p, S in moves_states])
                log_total = log(summation)
                #log_total = log(
                #    sum([plays[(player, state_to_string(S))] for p, S in moves_states]))
                # 下面用的是UCT来选择
                value, move, state = max(
                    ((wins[(player, state_to_string(S))] / plays[(player, state_to_string(S))]) +
                     self.C * sqrt(log_total / plays[(player, state_to_string(S))]), p, S)
                    for p, S in moves_states
                )
            elif len(moves_states)!=0:
                # Otherwise, just make an arbitrary decision.
                # 下面是用random选下一步
                # move, state = choice(moves_states)
                for p, S in moves_states:
                    if plays.get((player, state_to_string(S))) == None:
                        (move,state) = (p,S)
                        break
            else:
                # solution里面没有元素了
                next_player = 'w' if player=='b' else 'b'
                (temp_player, temp_pieces) = state
                state = (next_player, temp_pieces)


            states_copy.append(state)

            if expand==True:
                visited_states.add((player, state_to_string(state)))

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state_to_string(state)) not in self.plays:
                expand = False
                self.plays[(player, state_to_string(state))] = 0
                self.wins[(player, state_to_string(state))] = 0

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)

            if winner:
                break

        # 更新经过路径的数据
        for player, state in visited_states:
            self.plays[(player, state)] += 1
            # winner：赢的人的名字
            if player == winner:
                self.wins[(player, state)] += 1
