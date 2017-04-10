# -*- coding:utf-8 -*-  
import pygame
import chess
from element import *
from pygame.locals import *
from sys import exit
import datetime

##########################################################################

# 各种长宽高设置
frame_width = 480
frame_height = 640
# 棋盘的大小
chessboard_width = 400
chessboard_height = 400
# 棋盘的位置
chessboard_x = (frame_width - chessboard_width)/2
chessboard_y = (frame_height - chessboard_height)/4
# 棋子的大小
piece_width = 42
piece_height = 42
# 棋盘每个格子的大小
grid_width = chessboard_width/8
grid_height = chessboard_height/8
# 信息框 占棋盘的4/5
info_x = chessboard_x
info_y = chessboard_y + chessboard_height + 30
info_width = (chessboard_width / 5) * 4
info_height = 100
# 主页和刷新按钮的位置依赖于信息框
button_width = 64
button_height = 64
home_button_x = info_x + info_width + 30
home_button_y = info_y - 15
refresh_button_x = home_button_x
refresh_button_y = home_button_y + button_height + 5

# 标题高度占150
homepage_header_width = 300
homepage_header_height = 120
homepage_header_y = (180 - homepage_header_height)/2
homepage_header_x = (frame_width - homepage_header_width)/2

mode_button_width = 200
mode_button_height = 80
mode_button_frame_height = 120
mode_button_left = 140
mode_button_up = 160


##########################################################################

# pygame基本设置
pygame.init()
# 创建了一个窗口
screen = pygame.display.set_mode((frame_width, frame_height), 0, 32)
# 设置窗口标题
pygame.display.set_caption("Reversi")

##########################################################################

#导入各种图片
img_path = '../img/'
homepage_header_image_filename = img_path + 'homepage_header.png'
background_image_filename = img_path + 'background.jpg'
blackpiece_image_filename = img_path + 'black_resize.png'
whitepiece_image_filename = img_path + 'white_resize.png'
home_button_image_filename = img_path + 'home_button.png'
refresh_button_image_filename = img_path + 'refresh_button.png'

#加载并转换图像
background = pygame.image.load(background_image_filename).convert()
blackpiece = pygame.image.load(blackpiece_image_filename).convert_alpha()
whitepiece = pygame.image.load(whitepiece_image_filename).convert_alpha()
home_button = pygame.image.load(home_button_image_filename).convert_alpha()
refresh_button = pygame.image.load(refresh_button_image_filename).convert_alpha()
homepage_header = pygame.image.load(homepage_header_image_filename).convert_alpha()


# 各种颜色
color_black = (0,0,0)
color_white = (255,255,255)
color_deep_green = (0,87,55)
color_gray = (50,50,50)

##########################################################################

# 比赛是否已经开始
is_game_start = False
# 比赛是否有人获得胜利
is_game_finished = False
# 是否在主页
is_homepage = True

##########################################################################

def fetch_chessboard_position(pos):
	x = pos[0]-chessboard_x
	y = pos[1]-chessboard_y
	if x>=0 and x<=chessboard_width and y>=0 and y<=chessboard_height:
		return (x/grid_width,y/grid_height)
	else:
		return (-1,-1)

def fetch_mode_position(pos):
	if pos[0]>=mode_button_left and pos[0]<=mode_button_left+mode_button_width:
		for i in range(4):
			if pos[1]>=mode_button_up+i*mode_button_frame_height and pos[1]<=mode_button_up+i*mode_button_frame_height+mode_button_height:
				return i+1
	else:
		return 0


# 很多东西都写死了 参数mode代表鼠标移到了哪个模式的位置上
def draw_homepage(mode):
	offset = 22
	font_type = '../img/huakangwawa.TTF'
	show_text((80,30), 'Reversi', color=(0,0,0), font_size = 100, font_type=font_type)	
	color1 = color_white if mode == 1 else color_black
	color2 = color_white if mode == 2 else color_black
	color3 = color_white if mode == 3 else color_black
	color4 = color_white if mode == 4 else color_black
	bold1 = 0 if mode == 1 else 5
	bold2 = 0 if mode == 2 else 5
	bold3 = 0 if mode == 3 else 5
	bold4 = 0 if mode == 4 else 5
	pygame.draw.ellipse(screen, color_black, (mode_button_left, mode_button_up+0*mode_button_frame_height, mode_button_width, mode_button_height), bold1)
	pygame.draw.ellipse(screen, color_black, (mode_button_left, mode_button_up+1*mode_button_frame_height, mode_button_width, mode_button_height), bold2)
	pygame.draw.ellipse(screen, color_black, (mode_button_left, mode_button_up+2*mode_button_frame_height, mode_button_width, mode_button_height), bold3)
	pygame.draw.ellipse(screen, color_black, (mode_button_left, mode_button_up+3*mode_button_frame_height, mode_button_width, mode_button_height), bold4)
	show_text((165, mode_button_up+0*mode_button_frame_height+offset), 'Man vs Man', color=color1, font_size = 30, font_type=font_type)
	show_text((171, mode_button_up+1*mode_button_frame_height+offset), 'Man vs AI',  color=color2, font_size = 30, font_type=font_type)
	show_text((165, mode_button_up+2*mode_button_frame_height+offset), 'Man vs NET', color=color3, font_size = 30, font_type=font_type)
	show_text((171, mode_button_up+3*mode_button_frame_height+offset), 'AI vs NET',  color=color4, font_size = 30, font_type=font_type)
	
def show_text(pos, text, color=(0,0,0), font_bold = False, font_size = 13, font_italic = False, font_type='../img/MONACO.TTF'):         
    #获取系统字体，并设置文字大小  
    text_font = pygame.font.Font(font_type, font_size)  
    #设置是否加粗属性  
    text_font.set_bold(font_bold)  
    #设置是否斜体属性  
    text_font.set_italic(font_italic)  
    #设置文字内容  
    text = text_font.render(text, 1, color)  
    #绘制文字  
    screen.blit(text, pos)

def draw_chessboard():
	
	bold = 3

	for i in range(8):
		for j in range(8):
			pygame.draw.rect(screen, color_deep_green, Rect(chessboard_x+grid_width*i,chessboard_y+grid_height*j,grid_width,grid_height))
	for i in range(9):
		pygame.draw.line(screen, color_gray, 
			(chessboard_x+grid_width*i,chessboard_y), (chessboard_x+grid_width*i,chessboard_y+chessboard_height), bold)
	for i in range(9):
		pygame.draw.line(screen, color_gray,
			(chessboard_x,chessboard_y+grid_height*i), (chessboard_x+chessboard_width,chessboard_y+grid_height*i), bold)

def draw_piece(pieces):
	for x in range(8):
		for y in range(8):
			if not pieces[x][y]==None:
				piece_image = blackpiece if pieces[x][y].color == 'b' else whitepiece
				offset = ((chessboard_width)/8 - piece_width)/2
				screen.blit(piece_image, (chessboard_x + x*grid_width + offset, chessboard_y + y*grid_height + offset))	

def draw_hint(places, focus, turn):
	if len(places)==0:
		return

	color = color_black if turn=='b' else color_white

	# 边框大小 默认为0就是填充矩形
	bold = 5
	#闪烁效果
	for i in range(len(places)):
		if places[i][0]==focus[0] and places[i][1]==focus[1]:
			pygame.draw.rect(screen, color, 
				Rect(chessboard_x+grid_width*places[i][0],chessboard_y+grid_height*places[i][1],grid_width,grid_height))
		else:
			pygame.draw.rect(screen, color, 
				Rect(chessboard_x+grid_width*places[i][0],chessboard_y+grid_height*places[i][1],grid_width,grid_height), bold)	

def draw_infoboard(game):
	offset = 20
	# screen.blit(infoboard, (info_x,info_y))
	pygame.draw.rect(screen, color_black, Rect(info_x, info_y, info_width, info_height))
	pygame.draw.rect(screen, color_deep_green, Rect(info_x+5, info_y+5, info_width-10, info_height-10))

	header = 'Player  Step  Total  Chess'
	p1text = ' %-8s %-6s %-6s  %-6s' % (game.player1.name, str(game.player1.t_step_total)+'s', str(game.player1.t_total+game.player1.t_step_total)+'s' ,game.player1.own)
	p2text = ' %-8s %-6s %-6s  %-6s' % (game.player2.name, str(game.player2.t_step_total)+'s', str(game.player2.t_total+game.player2.t_step_total)+'s' ,game.player2.own)
	#print header
	#print p1text
	#print p2text
	show_text(pos=(info_x+offset,info_y+1*offset),text=header,font_size=17, font_bold=True)
	show_text(pos=(info_x+offset,info_y+2*offset),text=p1text,font_size=16,color=(0,0,0))
	show_text(pos=(info_x+offset,info_y+3*offset),text=p2text,font_size=16,color=(255,255,255))

	screen.blit(home_button, (home_button_x, home_button_y))
	screen.blit(refresh_button, (refresh_button_x, refresh_button_y))

##########################################################################


# 人人、人机、人网、机网

game = Game()

#游戏主循环
while True:

	#绘制背景
	screen.blit(background, (0,0))

	#是否按键
	click = False
	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		#接收到退出事件后退出程序
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			click = True

	# 在主页
	if is_homepage == True:
		
		mode = fetch_mode_position(mouse_pos)
		draw_homepage(mode)

		if click == True and not mode == 0:
			if mode == 1:	
				is_homepage = False
				is_game_start = True
				is_game_finished = False
				game.players_config()	
				game.start()
			elif mode == 2:
				pass
			elif mode == 3:
				pass
			elif mode == 4:
				pass
		
	# 如果比赛已经开始
	if is_game_start == True:

		# 两边都走不了
		if game.unwalkable == 2:
			is_game_finished = True
			game.player1.step_stop()
			game.player2.step_stop()		

		# 画棋盘
		draw_chessboard()
		# 画棋子
		draw_piece(game.pieces)
		# 画玩家数据
		draw_infoboard(game)

		focus = fetch_chessboard_position(mouse_pos)

		# 按了刷新按钮
		if click == True and mouse_pos[0]>=refresh_button_x and mouse_pos[0]<=refresh_button_x+button_width and mouse_pos[1]>=refresh_button_y and mouse_pos[1]<=refresh_button_y+button_height:
			is_game_finished = False
			game.start()
		# 按了回到桌面按钮
		if click == True and mouse_pos[0]>=home_button_x and mouse_pos[0]<=home_button_x+button_width and mouse_pos[1]>=home_button_y and mouse_pos[1]<=home_button_y+button_height:
			is_game_finished = True
			is_game_start = False
			is_homepage = True

		if is_game_finished == False:

			# 更新时间和棋子数目
			game.player1.update(game.turn)
			game.player2.update(game.turn)
			game.player1.count(game.pieces)
			game.player2.count(game.pieces)

			# 求出下一步的解
			solutions = chess.next_possible_steps(game.pieces, game.turn)

			next_turn = 'w' if game.turn == 'b' else 'b'
			this_player = game.player1 if game.turn == 'b' else game.player2
			next_player = game.player2 if game.turn == 'b' else game.player1

			if len(solutions)==0:
				game.unwalkable += 1
				game.turn = next_turn
			else:
				game.unwalkable = 0
				if this_player.kind=='Human':

					# 画出可能的解
					draw_hint(solutions, focus, game.turn)

					# 在棋盘内
					if not focus == (-1,-1):
						# 合法位置
						if click == True and focus in solutions:
							# 摆棋子
							chess.put_piece(focus, game.turn, game.pieces)
							game.turn = next_turn
							this_player.step_stop()
							next_player.step_start()
				elif this_player.kind=='AI':
					pass
				elif this_player.kind=='Net':
					pass
		else:
			# print 'game end'
			# 输出获胜方
			pass

	pygame.display.update()
		
    