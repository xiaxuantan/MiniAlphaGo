# -*- coding:utf-8 -*-  

# from element import Piece

directions = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]

# 找到当前棋局 下一步可能的方案
def next_possible_steps(pieces, turn):
	solutions = []
	flips = []
	aim = 'w' if turn == 'b' else 'b'
	for i in range(8):
		for j in range(8):
			if not pieces[i][j]=='n' :
				continue
			flag = False
			total_cnt = 0
			for k in range(8):
				x = i + directions[k][0]
				y = j + directions[k][1]
				cnt = 0
				while x>=0 and x<=7 and y>=0 and y<=7 and not pieces[x][y]=='n' and pieces[x][y]==aim:
					x += directions[k][0]
					y += directions[k][1]
					cnt += 1
				# 没有找到路径
				if x == i + directions[k][0] and y == j + directions[k][1]:
					continue
				if x<0 or x>7 or y<0 or y>7 or pieces[x][y]=='n':
					continue
				flag = True
				total_cnt += cnt
			if flag == True:
				solutions.append((i,j))
				flips.append(total_cnt)
	return solutions, flips

# 在合法的pos位置 轮到turn 放下棋子
def put_piece(pos, turn, pieces):
	aim = 'w' if turn == 'b' else 'b'
	i, j = pos
	pieces[i][j] = turn
	for k in range(8):
		x = i + directions[k][0]
		y = j + directions[k][1]
		while x>=0 and x<=7 and y>=0 and y<=7 and not pieces[x][y]=='n' and pieces[x][y]==aim:
			x += directions[k][0]
			y += directions[k][1]
		if x == i + directions[k][0] and y == j + directions[k][1]:
			continue
		if x<0 or x>7 or y<0 or y>7 or pieces[x][y]=='n' or pieces[x][y]==aim:
			continue
		while not x==i or not y==j:
			x -= directions[k][0]
			y -= directions[k][1]
			pieces[x][y] = turn

	return pieces

