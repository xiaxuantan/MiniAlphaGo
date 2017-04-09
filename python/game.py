# -*- coding:utf-8 -*-  
import pygame
import chess
from element import *
from pygame.locals import *
from sys import exit

##########################################################################

#各种长宽高设置
width = 480
height = 640
#棋盘的大小
chessboard_width = 400
chessboard_height = 400
#棋盘的位置
chessboard_x = (width - chessboard_width)/2
chessboard_y = (height - chessboard_height)/4
#棋子的大小
piece_width = 42
piece_height = 42
#棋盘每个格子的大小
grid_width = chessboard_width/8
grid_height = chessboard_height/8

##########################################################################

#pygame基本设置
pygame.init()
#创建了一个窗口
screen = pygame.display.set_mode((width, height), 0, 32)
#设置窗口标题
pygame.display.set_caption("Reversi")

##########################################################################

#导入各种图片
img_path = '../img/'
background_image_filename = img_path + 'background.jpg'
chessboard_image_filename = img_path + 'chessboard.png'
blackpiece_image_filename = img_path + 'black_resize.png'
whitepiece_image_filename = img_path + 'white_resize.png'
#加载并转换图像
background = pygame.image.load(background_image_filename).convert()
chessboard = pygame.image.load(chessboard_image_filename).convert()
blackpiece = pygame.image.load(blackpiece_image_filename).convert_alpha()
whitepiece = pygame.image.load(whitepiece_image_filename).convert_alpha()

##########################################################################

def draw_piece(piece, x, y):
	piece_image = blackpiece if piece.color == 'b' else whitepiece
	offset = ((chessboard_width)/8 - piece_width)/2
	screen.blit(piece_image, (chessboard_x + x*grid_width + offset, chessboard_y + y*grid_height + offset))	

def draw_hint(places, focus, turn):
	if len(places)==0:
		return
	deep_blue = (0,0,255)
	light_blue = (0,0,127)

	color = (0,0,0) if turn=='b' else (255,255,255)

	bold = 3
	#闪烁效果
	for i in range(len(places)):
		if places[i][0]==focus[0] and places[i][1]==focus[1]:
			pygame.draw.rect(screen, color, 
				Rect(chessboard_x+grid_width*places[i][0],chessboard_y+grid_height*places[i][1],grid_width,grid_height))
		else:
			pygame.draw.rect(screen, color, 
				Rect(chessboard_x+grid_width*places[i][0],chessboard_y+grid_height*places[i][1],grid_width,grid_height), bold)	

def fetch_position(pos):
	x = pos[0]-chessboard_x
	y = pos[1]-chessboard_y
	if x>=0 and x<=chessboard_width and y>=0 and y<=chessboard_height:
		return (x/grid_width,y/grid_height)
	else:
		return (-1,-1)

##########################################################################

#黑棋先 白棋后
turn = 'b'
#比赛是否已经开始
is_game_start = False
#比赛是否有人获得胜利
is_game_finished = False

#游戏主循环
while True:

	#绘制木质背景
	screen.blit(background, (0,0))

	#是否按键
	click = False

	pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		#接收到退出事件后退出程序
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			click = True

	#默认比赛直接开始 仅供测试 以后加入桌面拓展为各种模式
	if is_game_start == False:

		is_game_start = True
		is_game_finished = False

		player1 = Player(name='Peter', kind='Human')
		player2 = Player(name='June', kind='Human')
		#设置初始棋盘
		pieces = [[None for i in range(8)] for j in range(8)]
		pieces[3][3] = Piece(color='b')
		pieces[3][4] = Piece(color='w')
		pieces[4][3] = Piece(color='w')
		pieces[4][4] = Piece(color='b')
		
	#如果比赛已经开始
	if is_game_start == True:

		# 画棋盘
		screen.blit(chessboard, (chessboard_x, chessboard_y))
		# 画玩家1数据
		# 画玩家2数据


		#画棋子
		for i in range(8):
			for j in range(8):
				if not pieces[i][j]==None:
					draw_piece(pieces[i][j], i, j)

		solutions = chess.next_possible_steps(pieces, turn)
		focus = fetch_position(pos)

		# 到黑棋
		if turn=='b':

			if len(solutions)==0:
				turn = 'w'

			# 黑棋是玩家
			elif player1.kind=='Human':
				draw_hint(solutions, focus, turn)
				# 在棋盘内
				if not focus[0]==-1 and not focus[1]==-1:
					# 合法位置
					if click == True and focus in solutions:
						chess.put_piece(focus, turn, pieces)
						turn = 'w'
			elif player1.kind=='AI':
				pass
			elif player1.kind=='Net':
				pass
		# 到白棋
		elif turn=='w':

			if len(solutions)==0:
				turn = 'b'

			elif player2.kind=='Human':
				draw_hint(solutions, focus, turn)
				# 在棋盘内
				if not focus[0]==-1 and not focus[1]==-1:
					# 合法位置
					if click == True and focus in solutions:
						chess.put_piece(focus, turn, pieces)
						turn = 'b'
			elif player2.kind=='AI':
				pass
			elif player2.kind=='Net':
				pass

		pygame.display.update()
		
    