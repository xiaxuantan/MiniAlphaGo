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
    s = ''
    for i in range(8):
        for j in range(8):
            s += pieces[i][j]
        # s += '\n'
    return s

def simulate(state, board):

    step = 0
    wpos = 0
    bpos = 0
    credit = 1.0
    pos = ((0,7),(7,0),(0,0),(7,7))
    stage = 45
    while True:

        player = board.current_player(state)
        legal = board.legal_plays(state)

        moves_states = [(p, board.next_state(state, p)) for p in legal]
        if len(legal)==0:           
            state = (player, state[1])
        else:
            move, state = choice(moves_states)
            if move in pos and board.stage(state)<stage :
                if player=='w':
                    wpos += credit 
                else:
                    bpos += credit
            
        winner = board.winner(state)
        if winner:
            break

    return (winner,wpos,bpos)

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
        # UCB1的参数，先从根号2开始，目前来看越小越好--simlulation数太小了
        self.C = 0.5
        # simulation里面，每个儿子至少的模拟次数
        self.threshold = 5
        self.pos = ((0,7),(7,0),(0,0),(7,7))

        self.stage = 45
        self.credit = 1.0

        self.simulateTimes = 20
        self.processes = 10

    def update(self, state):
        # Takes a game state, and appends it to the history.
        
        self.states.append(state)

        # black_and_white = 0
        # for i in [0,7]:
        #     for j in [0,7]:
        #         if state[1][i][j]!='n':
        #             black_and_white += 1

        # if black_and_white>self.board.stage:
        #     self.board.stage += 1
        #     # self.wins = {}
        #     # self.plays = {}

        # print 'stage',self.board.stage

    def get_play(self, queue):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        # state = copy.deepcopy(self.states[-1])
        (player,pieces) = self.states[-1]
        pieces_copy = [ i[:] for i in pieces ]
        state = (player,pieces_copy)

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
        # print '************************'
        print 'games', games

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]
    
        # Pick the move with the highest percentage of wins.
        # player是造成state S的玩家

        percent_wins, move = max((self.wins.get((player, state_to_string(S)), 0)/self.plays.get((player, state_to_string(S)), 1), p) for p, S in moves_states)

        # print '************************'
        print 'percent wins: ', percent_wins

        queue.put(move)
        return

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        
        visited_states = set()
        (player,pieces) = self.states[-1] 
        pieces_copy = [ i[:] for i in pieces ]
        state = (player, pieces_copy)
    
        expand = True

        wpos = 0.0
        bpos = 0.0

        # for t in xrange(self.max_moves):
        while expand==True:

            print 'expand'

            player = self.board.current_player(state)

            # legal：从state出发的可行步
            legal = self.board.legal_plays(state)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            # 选择p，以及state更新为选择了p后的状态
            # if len(moves_states)!=0 and all([plays.get((player, state_to_string(S))) for p, S in moves_states]) and all ([(plays[(player, state_to_string(S))]>self.threshold) for p, S in moves_states]):
            if len(moves_states)!=0 and all([plays.get((player, state_to_string(S))) for p, S in moves_states]):
                # If we have stats on all of the legal moves here, use them.
                summation = sum([plays[(player, state_to_string(S))] for p, S in moves_states])
                log_total = log(summation)

                # 下面用的是UCT来选择
                value, move, state = max(
                    ((wins[(player, state_to_string(S))] / plays[(player, state_to_string(S))]) +
                     self.C * sqrt(log_total / plays[(player, state_to_string(S))]), p, S)
                    for p, S in moves_states
                )

                print [plays.get((player, state_to_string(S))) for p, S in moves_states]

            elif len(moves_states)!=0:
                for p, S in moves_states:
                    if plays.get((player, state_to_string(S))) == None:
                        (move,state) = (p,S)
                        break
                print [plays.get((player, state_to_string(S))) for p, S in moves_states]

                # print state_to_string(state)
                # print 'player',state[0]
            elif len(moves_states)==0:
                (temp_player, temp_pieces) = state
                state = (player, temp_pieces)
            else:
                print 'unexpected'


            visited_states.add((player, state_to_string(state)))


            # 'player' here and below refers to the player
            # who moved into that particular state.

            if move in self.pos and self.board.stage(state)< self.stage:
                if player=='w':
                    wpos += self.credit 
                else:
                    bpos += self.credit

            if (player, state_to_string(state)) not in self.plays:
                expand = False
                self.plays[(player, state_to_string(state))] = 0
                self.wins[(player, state_to_string(state))] = 0

            winner = self.board.winner(state)
            if winner:
                break

        # self.current_state = state
        pool = multiprocessing.Pool(processes=self.processes)
        resultSet = []
        for i in range(self.simulateTimes):
            resultSet.append(pool.apply_async(simulate, (state, self.board)))
        pool.close()
        pool.join()

        totalBlackWins = 0
        totalWhiteWins = 0
        totalTies = 0
        temp = []
        
        # for result in resultSet:
        #     if result.get() == 'b':
        #         totalBlackWins += 1
        #     elif result.get() == 'w':
        #         totalWhiteWins += 1
        #     elif result.get() == 't':
        #         totalTies += 1

        for result in resultSet:
            temp = result.get()
            # print 'temp: ',temp
            if temp[0] == 'b':
                totalBlackWins += 1
            elif temp[0] == 'w':
                totalWhiteWins += 1
            elif temp[0] == 't':
                totalTies += 1

            wpos += temp[1]
            bpos += temp[2]

                
        totalPlays = totalBlackWins + totalWhiteWins + totalTies

        # 更新经过路径的数据
        for player, state in visited_states:
            self.plays[(player, state)] += totalPlays
            print 'totalBlackWins',totalBlackWins,' totalWhiteWins', totalWhiteWins
            print 'bpos ', bpos, ' wpos', wpos
            if player == 'b':
                self.wins[(player, state)] += totalBlackWins + bpos
            elif player == 'w':
                self.wins[(player, state)] += totalWhiteWins + wpos
