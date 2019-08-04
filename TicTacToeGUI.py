import pygame as pg
import random

SIZE = 3

TILESIZE = 64
WIDTH = int(TILESIZE * SIZE ** 1.1 + 300)
HEIGHT = int(TILESIZE * SIZE ** 1.1 + 300)
OFFSET = WIDTH / 2 - TILESIZE * SIZE / 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARKRED = (128, 0, 0)
DARKYELLOW = (128, 128, 0)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 128, 0)
TITLE = 'Tic Tac Toe'
FPS = 30


class Game:
    def __init__(self, size):
        self.size = size
        pg.init()
        self.font_name = pg.font.match_font('arial')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.player_symbol = None
        self.clicked = False

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit() 
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    self.clicked = True

    def update(self):
        mx, my = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if self.is_tie():
            self.end_text = "It's tie"
            self.playing = False
        
        # check if AI wins
        if self.game_won(self.board, self.ai_symbol):
            self.end_text = "You Suck!"
            self.playing = False
                                
        if self.first == 'AI':
            self.update_board(self.ai_move(self.ai_symbol, self.player_symbol), self.ai_symbol)
            self.first = 'player'
        # make the player move
        for i in range(self.size):
            for j in range(self.size):
                if self.box_list[i][j].collidepoint(mx, my):
                    if self.clicked and self.is_valid_pos(self.board,[i, j]) and click[0]:
                        self.board[i][j] = self.player_symbol 
        # check for win or tie
                        if self.game_won(self.board, self.player_symbol):
                            self.end_text = "You win!"
                            self.playing = False  

                        if self.is_tie():
                            self.end_text = "It's tie"
                            self.playing = False
        # make AI move
                        if self.playing:
                            self.update_board(self.ai_move(self.ai_symbol, self.player_symbol), self.ai_symbol)
                            self.clicked = False
      
    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        pg.display.update()

    def rect_data_structure(self):
        # create the rectangle data structure for collision detection
        rect_list = []
        for i in range(self.size):
            for j in range(self.size):
                row = OFFSET + i * TILESIZE
                col = OFFSET + j * TILESIZE
                rect = pg.Rect(col, row, TILESIZE, TILESIZE)
                rect_list.append(rect)
        # convert the rect list to nested list [ , , ] -> [[],[],[]]
        self.box_list = []
        for i in range(0, len(rect_list), self.size):
            self.box_list.append(rect_list[i:i+self.size])

    def update_board(self, pos, val):
        self.board[pos[0]][pos[1]] = val
     
    def is_valid_pos(self, board, pos):
        if board[pos[0]][pos[1]] == ' ':
            return True
        return False

    def is_tie(self):
        # check if it's a draw
        count = 0
        for i in range(self.size):
            if ' ' not in self.board[i]:
                count += 1
                if count == self.size:
                    return True
    
    def game_won(self, board, val):
        # horizontally
        for i in board:
            h_win = 0
            for j in i:
                if val == j:
                    h_win += 1
            if h_win == self.size:
                return True

        # vertiically
        for i in range(self.size):
            v_win = 0
            for j in board:
                if j[i] == val:
                    v_win += 1
                    if v_win == self.size:
                        return True
       
        # diagonal right
        dr_win = 0
        for i in range(self.size):
            if board[i][i] == val:
                dr_win += 1
                if dr_win == self.size:
                    return True
                   
        # diagonal left
        dl_win = 0
        for i in range(self.size):
            if board[i][self.size-1-i] == val:
                dl_win += 1
            if dl_win == self.size:
                return True

    def ai_move(self, ai_symbol, player_symbol):
        ai_board = self.board
        corners = []
        sides = []
        # check if AI can win in one move
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_pos(ai_board, [row, col]):
                    ai_board[row][col] = ai_symbol
                    if self.game_won(ai_board, ai_symbol):
                        return [row, col]
                    ai_board[row][col] = ' '
        # block the player if he can win in one move
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_pos(ai_board, [row, col]):
                    ai_board[row][col] = player_symbol
                    if self.game_won(ai_board, player_symbol):
                        return [row, col]
                    ai_board[row][col] = ' '
        # choose a corner or side
                    if (row == 0 or row == self.size - 1) and (col == 0 or col == self.size -1):
                        corners.append([row, col])
                    else:
                        sides.append([row, col])
        if len(corners) > 0:
            return random.choice(corners)
        if len(sides) > 0:
            return random.choice(sides)

    def draw_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                row = OFFSET + i * TILESIZE
                col = OFFSET + j * TILESIZE
                pg.draw.rect(self.screen, BLACK, (col, row, TILESIZE, TILESIZE), 1)  
                self.draw_text(self.board[i][j], self.font_name, 50, BLACK, col+20, row)

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def button(self, pos_x, pos_y, color1, color2, text_color, text, text_size, width, height, function):
        rect = pg.Rect(pos_x, pos_y, width, height)
        pg.draw.rect(self.screen, color1, rect)
        pg.draw.rect(self.screen, BLACK, rect, 2)
        click = pg.mouse.get_pressed()
        mx, my = pg.mouse.get_pos()
        if rect.collidepoint(mx, my):
            pg.draw.rect(self.screen, color2, rect)
            if click[0]:
                function()
        self.draw_text(text, self.font_name, text_size, text_color, pos_x + width // 2, pos_y + height // 2, align='center')
          
    def symbol_choice_x(self):
        self.player_symbol = 'X'
        self.ai_symbol = 'O'
        self.start_run = False
        pg.time.wait(500)

    def symbol_choice_o(self):
        self.player_symbol = 'O'
        self.ai_symbol = 'X'
        self.start_run = False
        pg.time.wait(500)

    def show_start_screen(self):
        self.first = random.choice(['AI', 'player'])
        self.board = [[' ' for i in range(self.size)] for j in range(self.size)]
        self.rect_data_structure()
        self.start_run = True
        click = pg.mouse.get_pressed()
        while self.start_run:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.start_run = False 
            self.screen.fill(WHITE)

            # draw btexct box to choose a symbol
            self.button(WIDTH // 5, HEIGHT // 2, DARKGREEN, GREEN, BLACK, 'O', 50, 100, 60, self.symbol_choice_o)
            self.button(WIDTH * 3 // 5, HEIGHT // 2, DARKYELLOW, YELLOW, BLACK, 'X', 50, 100, 60, self.symbol_choice_x)
            self.draw_text('Choose a playing symbol', self.font_name, 50, BLACK, WIDTH // 2, HEIGHT // 5, align='center')
            pg.display.update()

    def show_go_screen(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_text(self.end_text, self.font_name, 50, DARKRED,
                         WIDTH / 2, HEIGHT / 8, align='center')
        self.draw_text('Press a key to play again', self.font_name, 35, BLACK,
                         WIDTH / 2, HEIGHT * 4 / 5, align='center')
        pg.display.update()
        self.wait_fof_key()

    def wait_fof_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONUP:
                    pg.time.wait(200)
                    waiting = False

if __name__ == "__main__":
    g = Game(SIZE)
    while g.running:
        g.show_start_screen()
        g.run()
        g.show_go_screen()

pg.quit