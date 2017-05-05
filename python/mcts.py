# -*- coding:utf-8 -*- 
from __future__ import division

from random import choice
from math import log, sqrt
import datetime
import copy

from board import *
import chess
import element

import multiprocessing


# 把state从指针的二维数组变为string类型
def state_to_string(state):
    (player, pieces) = state
    return ''.join([''.join(line) for line in pieces])

def simulate(state, board):

    no_move = 0
    black_and_white = 0

    for i in range(8):
        for j in range(8):
            if state[1][i][j]!='n':
                black_and_white += 1
    while 1:
        player = board.current_player(state)
        legal = board.legal_plays(state)

        moves_states = [(p, board.next_state(state, p)) for p in legal]
        if len(legal)==0:           
            state = (player, state[1])
            no_move += 1
        else:
            move, state = choice(moves_states)
            black_and_white += 1
            if move in ((0,7),(7,0),(0,0),(7,7)) and black_and_white<=45:
                return player
            no_move = 0
            
        if no_move == 2:
            break

    return board.winner(state)

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
        self.calculation_time = datetime.timedelta(seconds=10)
        # 模拟中的最大步数
        self.max_moves = 64
        # 记录某个中间状态对应的模拟数、模拟中赢的盘数的字典
        self.plays = {}
        self.wins = {}
        # UCB1的参数，先从根号2开始，目前来看越小越好
        self.C = 0.1
        # simulation里面，每个儿子至少的模拟次数
        self.threshold = 5

        self.stage = 64

        self.simulateTimes = 20
        self.processes = 10

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)       

    def get_play(self, queue):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        # state = copy.deepcopy(self.states[-1])
        (player,pieces) = self.states[-1]
        pieces_copy = [ i[:] for i in pieces ]
        state = (player, pieces_copy)
        # player 是 'w' or 'b'

        player = self.board.current_player(state)
        legal = self.board.legal_plays(state)
        # (player,pieces)
        # Bail out early if there is no real choice to be made.
        if not legal:
            queue.put(None)
            return
        if len(legal) == 1:
            queue.put(legal[0])
            return 

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += self.simulateTimes
        print 'games', games

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]
    
        # Pick the move with the highest percentage of wins.
        # player是造成state S的玩家
        percent_wins, move = max([(self.wins.get((player, state_to_string(S)), 0)/self.plays.get((player, state_to_string(S)), 1), p) for p, S in moves_states])

        print 'win_step',[(self.wins.get((player, state_to_string(S)), 0)/self.plays.get((player, state_to_string(S)), 1)) for p, S in moves_states]
        print 'percentage', percent_wins
        queue.put(move)
        return

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        
        visited_states = []

        (player,pieces) = self.states[-1] 
        pieces_copy = [ i[:] for i in pieces ]
        state = (player, pieces_copy)
    
        expand = True
        no_move = 0

        # for t in xrange(self.max_moves):
        while expand is True:

            player = self.board.current_player(state)

            # legal：从state出发的可行步
            legal = self.board.legal_plays(state)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            # 选择p，以及state更新为选择了p后的状态

            played_states = [plays.get((player, state_to_string(S))) for p, S in moves_states]

            if len(moves_states)!=0 and all(played_states):

                # If we have stats on all of the legal moves here, use them.
                summation = sum(played_states)
                log_total = log(summation)

                # 下面用的是UCT来选择
                value, move, state = max(
                    ((wins[(player, state_to_string(S))] / plays[(player, state_to_string(S))]) +
                     self.C * sqrt(log_total / plays[(player, state_to_string(S))]), p, S)
                    for p, S in moves_states
                )
                no_move = 0

            elif len(moves_states)!=0:

                for p, S in moves_states:
                    if plays.get((player, state_to_string(S))) == None:
                        (move,state) = (p,S)
                        break
                no_move = 0

            elif len(moves_states)==0:
                (temp_player, temp_pieces) = state
                state = (player, temp_pieces)
                no_move += 1
            else:
                print 'unexpected'

            if no_move == 2:
                break
            else:
                visited_states.append((player, state_to_string(state)))

            # 'player' here and below refers to the player
            # who moved into that particular state.
            if (player, state_to_string(state)) not in self.plays:
                expand = False
                self.plays[(player, state_to_string(state))] = 0
                self.wins[(player, state_to_string(state))] = 0

        pool = multiprocessing.Pool(processes=self.processes)
        resultSet = []
        for i in range(self.simulateTimes):
            resultSet.append(pool.apply_async(simulate, (state, self.board)))
        pool.close()
        pool.join()

        totalBlackWins = 0
        totalWhiteWins = 0
        totalTies = 0
        
        for result in resultSet:
            if result.get() == 'b':
                totalBlackWins += 1
            elif result.get() == 'w':
                totalWhiteWins += 1
            elif result.get() == 't':
                totalTies += 1

        totalPlays = totalBlackWins + totalWhiteWins + totalTies

        # 更新经过路径的数据
        for player, state in visited_states:
            self.plays[(player, state)] += totalPlays
            if player == 'b':
                self.wins[(player, state)] += totalBlackWins
            elif player == 'w':
                self.wins[(player, state)] += totalWhiteWins
