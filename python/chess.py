# -*- coding:utf-8 -*-  

from element import Piece

directions = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]

# 找到当前棋局 下一步可能的方案
def next_possible_steps(pieces, turn):
	solutions = []
	aim = 'w' if turn == 'b' else 'b'
	for i in range(8):
		for j in range(8):
			if not pieces[i][j]==None:
				continue
			flag = False
			for k in range(8):
				x = i + directions[k][0]
				y = j + directions[k][1]
				while x>=0 and x<=7 and y>=0 and y<=7 and not pieces[x][y]==None and pieces[x][y].color==aim:
					x += directions[k][0]
					y += directions[k][1]
				# 没有找到路径
				if x == i + directions[k][0] and y == j + directions[k][1]:
					continue
				if x<0 or x>7 or y<0 or y>7 or pieces[x][y]==None:
					continue
				flag = True
				break
			if flag == True:
				solutions.append((i,j))
	return solutions

# 在合法的pos位置 轮到turn 放下棋子
def put_piece(pos, turn, pieces):
	aim = 'w' if turn == 'b' else 'b'
	i, j = pos
	pieces[i][j] = Piece(turn)
	for k in range(8):
		x = i + directions[k][0]
		y = j + directions[k][1]
		while x>=0 and x<=7 and y>=0 and y<=7 and not pieces[x][y]==None and pieces[x][y].color==aim:
			x += directions[k][0]
			y += directions[k][1]
		if x == i + directions[k][0] and y == j + directions[k][1]:
			continue
		if x<0 or x>7 or y<0 or y>7 or pieces[x][y]==None or pieces[x][y].color==aim:
			continue
		while not x==i or not y==j:
			x -= directions[k][0]
			y -= directions[k][1]
			pieces[x][y].color = turn

