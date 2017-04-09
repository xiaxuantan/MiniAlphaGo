# -*- coding:utf-8 -*-  

#棋子
class Piece:
	def __init__(self, color):
		self.color = color # 'b' or 'w'

#玩家
class Player:
	def __init__(self, name, kind):
		self.name = name
		self.kind = kind
		self.own = 0
