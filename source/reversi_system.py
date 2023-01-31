import pygame as pg
import sys

class Option:
    size = 8
    start_player = 1 #1=黒, 2=白
    frame_rate = 30
    title = ""
    screen_size = (640, 480)

class Frame_rate:
    def __init__(self, value):
        self.fps = value
    
    @property
    def fps(self):
        return self.__fps
    @property
    def speed(self):
        return self.__speed
    @fps.setter
    def fps(self, fps):
        self.__fps = int(fps)
        self.__speed = int(1000 / fps)

class Screen_calc:
    def __init__(self, option):
        self.option = option

        self.padding_x = self.option.screen_size[0] * 0.1
        self.padding_y = self.option.screen_size[0] * 0.1
        self.x = self.option.screen_size[0]
        self.y = self.option.screen_size[1]
        self.board_length_x = (self.x - self.padding_x*2)/self.option.size
        self.board_length_y = (self.y - self.padding_y*2)/self.option.size
        self.grid_padding_x = 10 * self.option.screen_size[0] / 1000
        self.grid_padding_y = 10 * self.option.screen_size[1] / 1000
        self.stone_size_x = 95 * self.option.screen_size[0] / 1000
        self.stone_size_y = 95 * self.option.screen_size[1] / 1000

class Stone:
    color = 1 #1=黒, 2=白

    def __init__(self, color):
        self.color = color

class Board:
    size = 8
    data = 0

    def __init__(self, size):
        self.size = size
        self.data = [[0 for i in range(self.size)] for i in range(self.size)]

class Display:
    def __init__(self, screen_calc, option):
        self.op = option
        self.sc = screen_calc
        self.screen = pg.display.set_mode((self.sc.x, self.sc.y))

    def draw(self, sys):
        self.screen.fill((0, 0, 0))
        self.__draw_board(sys.board.data, sys.select_area)

        if(sys.winner == "None"):
            if(sys.current_player == 1):
                self.__draw_text("黒プレイヤーの番です", (self.sc.padding_x, self.sc.padding_y*0.65), 20)
            else:
                self.__draw_text("白プレイヤーの番です", (self.sc.padding_x, self.sc.padding_y*0.65), 20)
        else:
            if(sys.winner == 1):
                self.__draw_text("黒プレイヤーの勝利です", (self.sc.padding_x, self.sc.padding_y*0.65), 20)
            elif(sys.winner == 2):
                self.__draw_text("白プレイヤーの勝利です", (self.sc.padding_x, self.sc.padding_y*0.65), 20)
            elif(sys.winner == 0):
                self.__draw_text("引き分けです", (self.sc.padding_x, self.sc.padding_y*0.65), 20)

        stone_count = sys.stone_count
        self.__draw_text(f'white:{stone_count[0]} / black:{stone_count[1]} [{stone_count[2]}]', (self.sc.padding_x, self.sc.padding_y*0.25), 20)
        pg.display.update()

    def __draw_text(self, text, pos, font_size = 40): #pos : (x, y), text : array, font_size : int
        font = pg.font.Font("DotGothic16-Regular.ttf", font_size)
        text = font.render(text, True, (220,220,220))   # 描画する文字列の設定
        self.screen.blit(text, pos)

    def __draw_board(self, data, pos="None"):
        #ボードを用意
        pg.draw.rect(self.screen, (0, 155, 0), pg.Rect(self.sc.padding_x, self.sc.padding_y, self.sc.x - self.sc.padding_x*2 , self.sc.y - self.sc.padding_y*2))
        
        #選択領域を描画
        if(not(pos == "None")):
            pg.draw.rect(self.screen, (0, 200, 0), pg.Rect(self.sc.padding_x + self.sc.board_length_x*pos[0], self.sc.padding_y + self.sc.board_length_y*pos[1], self.sc.board_length_x , self.sc.board_length_y))

        #グリッド線
        for i in range(self.op.size + 1):
            pg.draw.line(self.screen, (50, 50, 50), (self.sc.padding_x + self.sc.board_length_x*i, self.sc.padding_y), (self.sc.padding_x + self.sc.board_length_x*i, self.sc.y - self.sc.padding_y), 2)
        for i in range(self.op.size + 1):
            pg.draw.line(self.screen, (50, 50, 50), (self.sc.padding_x, self.sc.padding_y + self.sc.board_length_y*i), (self.sc.x - self.sc.padding_x, self.sc.padding_y + self.sc.board_length_y*i), 2)
        #石の配置
        for i, x in enumerate(data):
            for j, y in enumerate(x):
                if(y == 0):
                    pass
                else:
                    if(y.color == 1):
                        pg.draw.ellipse(self.screen, (50, 50, 50), (self.sc.padding_x + i*self.sc.board_length_x + self.sc.grid_padding_x, self.sc.padding_y + j*self.sc.board_length_y + self.sc.grid_padding_y, self.sc.stone_size_x - self.sc.grid_padding_x, self.sc.stone_size_y - self.sc.grid_padding_y, ))
                    elif(y.color == 2):
                        pg.draw.ellipse(self.screen, (200, 200, 200), (self.sc.padding_x + i*self.sc.board_length_x + self.sc.grid_padding_x, self.sc.padding_y + j*self.sc.board_length_y + self.sc.grid_padding_y, self.sc.stone_size_x - self.sc.grid_padding_x, self.sc.stone_size_y - self.sc.grid_padding_y, ))
        
class sub_system:#リバーシのサブシステム / 設置可能、石置き換え、石カウント
    def stone_count(board):#board : Board, return : white, black, none
        white = 0
        black = 0

        for i in board.data:
            for j in i:
                if(not(j == 0)):
                    if(j.color == 1):
                        black += 1
                    elif(j.color == 2):
                        white += 1
        return white, black, board.size**2 - (white + black)

    def put_stone(board, pos, current_player):#board : Board, pos : (x, y), current_player : int, return : Board
        board.data[pos[0]][pos[1]] = Stone(current_player)
        rotate = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        place_pos = set() #置き換える石
        for i in rotate: #8方向調べる
            pos_ = list(pos)
            place_pos_r = set() #方向ごと置き換える石の一時的保存
            find_stone = False #自分の石ではないのを見つけたフラグ
            while True: #指定方向の石を置き換える
                pos_[0] += i[0]
                pos_[1] += i[1]
                if(not((0 <= pos_[0]) and (pos_[0] < len(board.data))) or not((0 <= pos_[1]) and (pos_[1] < len(board.data))) ): #端かどうか
                    break
                if(find_stone == False):
                    if(board.data[pos_[0]][pos_[1]] == 0):
                        break
                    if(board.data[pos_[0]][pos_[1]].color == current_player):
                        break
                    else:
                        find_stone = True
                        place_pos_r.add((pos_[0], pos_[1]))
                elif(find_stone == True):
                    if(board.data[pos_[0]][pos_[1]] == 0):
                        break
                    if(board.data[pos_[0]][pos_[1]].color == current_player):
                        place_pos |= place_pos_r
                        break
                    else:
                        place_pos_r.add((pos_[0], pos_[1]))
        for j in place_pos:
            board.data[j[0]][j[1]] = Stone(current_player)
        return board

    def search_put(board, current_player):#board : Board, current_player：int , return : **(x, y)
        can_put = set()
        rotate = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for i, x in enumerate(board.data): #size^2のボードを調べる
            for j, y in enumerate(x):
                if(y == 0): #石がなければスキップ
                    pass
                elif(y.color == current_player): #current_playerの石でなければスキップ
                    for z in rotate: #8方向調べる
                        pos_ = [i, j]
                        find_stone = False #自分の石ではないのを見つけたフラグ
                        while True: #指定方向の石を調べる
                            pos_[0] += z[0]
                            pos_[1] += z[1]
                            if(not((0 <= pos_[0]) and (pos_[0] < len(board.data))) or not((0 <= pos_[1]) and (pos_[1] < len(board.data))) ): #端かどうか
                                break
                            if(find_stone == False):
                                if(board.data[pos_[0]][pos_[1]] == 0):
                                    break
                                if(board.data[pos_[0]][pos_[1]].color == current_player):
                                    break
                                else:
                                    find_stone = True
                            elif(find_stone == True):
                                if(board.data[pos_[0]][pos_[1]] == 0):
                                    can_put.add((pos_[0], pos_[1]))
                                    break
                                if(board.data[pos_[0]][pos_[1]].color == current_player):
                                    break
        return can_put
                            
class Reversi_system:#リバーシのメインシステム

    def __init__(self, option):
        self.op = option
        pg.init()
        self.board = Board(8)
        self.board = Board(option.size)
        self.current_player = option.start_player
        self.fps = Frame_rate(option.frame_rate)
        pg.display.set_caption(option.title)
        self.sc = Screen_calc(option)
        self.display = Display(self.sc, option)

        self.select_area = "None"
        self.winner = "None"
        self.current_player = 1 #1=黒, 2=白

        self.__stone_count = (0, 0, 0)

        self.board.data[3][3] = Stone(1)
        self.board.data[3][4] = Stone(2)
        self.board.data[4][3] = Stone(2)
        self.board.data[4][4] = Stone(1)
    
    def start(self):
        pass

    def main(self): #main_loop
        last_time = 0
        while True:
            self.select_area = self.mouse_select(pg.mouse.get_pos())

            for event in pg.event.get(): #イベント処理
                if event.type == pg.QUIT: #終了
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.MOUSEBUTTONDOWN: #左クリック
                    ret = self.click_board()

            self.display.draw(self) #描画
            
            current_time = pg.time.get_ticks()
            elapsed_time = current_time - last_time
            last_time = current_time
            if(elapsed_time < self.fps.speed):
                pg.time.wait(self.fps.speed - elapsed_time)

    def click_board(self): # return : bool
        if(self.select_area == "None"):
            return False

        can_put = sub_system.search_put(self.board, self.current_player)
        if(self.select_area in can_put):
            sub_system.put_stone(self.board, self.select_area, self.current_player)
            self.change_player()
            if(len(sub_system.search_put(self.board, self.current_player)) == 0): #置ける場所がなければもう一回
                self.change_player()
            white, black, none = sub_system.stone_count(self.board)
            if(white == 0 or black == 0 or none == 0): #終了条件
                self.result()
            return True

    def result(self):
        white, black, none = sub_system.stone_count(self.board)
        if(white < black): #黒の勝ち
            self.winner = 1
        elif(black < white): #白の勝ち
            self.winner = 2
        else: #引き分け
            self.winner = 0
        print("end reversi")


    def change_player(self):
        if(self.current_player == 1):
            self.current_player = 2
        else:
            self.current_player = 1

    def put_stone(self, pos, stone): #pos : (x,y)
        self.board.data[pos[0]][pos[1]] = stone

    def mouse_select(self, pos): #pos : (x,y), return : (x,y)
        self.sc.padding_x
        self.sc.x
        
        for i in range(self.op.size):
            for j in range(self.op.size):
                a = (int(self.sc.padding_x + self.sc.board_length_x*i) < pos[0]) and (pos[0] < int(self.sc.padding_x + self.sc.board_length_x*(i+1)))
                b = (int(self.sc.padding_y + self.sc.board_length_y*j) < pos[1]) and (pos[1] < int(self.sc.padding_y + self.sc.board_length_y*(j+1)))
                if (a and b):
                    return (i,j)
        return "None"

    @property
    def stone_count(self):
        white, black, none = sub_system.stone_count(self.board)
        self.__stone_count = (white, black, none)
        return self.__stone_count