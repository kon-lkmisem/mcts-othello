import math
import sys
import time
import copy

import pygame

from OthelloMCTS import othello

BLOCK_SIZE = 50
PADDING_SIZE = 5
WINDOW_WIDTH = BLOCK_SIZE * 8
WINDOW_HEIGHT = BLOCK_SIZE * 8 + 20
FRAME_PER_SECOND = 60

HUMAN = 0
AI = 1

ALPHAZERO = 'alpha'
MINMAX = 'minmax'

class Game_Engine(object):
    def __init__(self):
        super().__init__()
        self.images = {}  # image resources
        self.keys_down = {}  # records of down-keys

        self.player_info =[AI,HUMAN]

        self.AI_info=[ALPHAZERO,ALPHAZERO]

        # create game object
        self.game = othello.Othello(self.AI_info)

        self.debug = False  # True for debugging

    def preparation(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Othello')

        # set font
        self.font = pygame.font.SysFont("Helvetica", 48)

        # set images
        self.images['board'] = pygame.image.load('OthelloMCTS/images/board.png')
        self.images['black'] = pygame.image.load('OthelloMCTS/images/black.png')
        self.images['white'] = pygame.image.load('OthelloMCTS/images/white.png')

        self.drawBoard()

    def newGame(self):
        self.game.__init__(self.AI_info)

    def quitGame(self):
        pygame.quit()
        sys.exit()

    def start(self):
        self.preparation()
        self.newGame()

        while True:
            # if self.game.AIReadyToMove:
            #     self.game.AIMove()
            # else:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             self.quitGame()
            #         elif event.type == pygame.KEYDOWN:
            #             self.keydownHandler(event)
            #         elif event.type == pygame.KEYUP:
            #             self.keyupHandler(event)
            #         elif event.type == pygame.MOUSEBUTTONDOWN:
            #             self.mousedownHandler(event)
            #         elif event.type == pygame.MOUSEBUTTONUP:
            #             self.mouseupHandler(event)
            #         elif event.type == pygame.MOUSEMOTION:
            #             self.mousemoveHandler(event)
            #         else:
            #             pass
            if self.player_info[self.game.player-1]==HUMAN:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quitGame()
                    elif event.type == pygame.KEYDOWN:
                        self.keydownHandler(event)
                    elif event.type == pygame.KEYUP:
                        self.keyupHandler(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mousedownHandler(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouseupHandler(event)
                    elif event.type == pygame.MOUSEMOTION:
                        self.mousemoveHandler(event)
                    else:
                        pass
            else:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.quitGame()
                        elif event.type == pygame.KEYDOWN:
                            pass
                        elif event.type == pygame.KEYUP:
                            pass
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pass
                        elif event.type == pygame.MOUSEBUTTONUP:
                            # self.game.playerMove(0,0)
                            pass
                        elif event.type == pygame.MOUSEMOTION:
                            # self.mousemoveHandler(event)
                            pass
                        else:
                            pass
                self.game.playerMove(0,0)
            
            if self.game.changed:
                # drawBoard에서 게임 종료메시지 출력
        # Othello의 victory 변수를 통해서 게임 종료 체크
                self.drawBoard()
                self.game.changed = False
            
                time.sleep(1)

            # if self.game.AIReadyToMove:
            #     self.game.AIMove()

            self.clock.tick(FRAME_PER_SECOND)
        self.quitGame()

    def drawText(self, text, font, screen, x, y, rgb):
        textObj = font.render(text, 1, (rgb[0], rgb[1], rgb[2]))
        textRect = textObj.get_rect()
        textRect.topleft = (x, y)
        screen.blit(textObj, textRect)

    def drawBoard(self):
        # draw the board
        board = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.screen.blit(self.images['board'], board)

        # draw the menu at the bottom
        menu = pygame.Rect(0, 8 * BLOCK_SIZE, WINDOW_WIDTH, 20)
        pygame.draw.rect(self.screen, (255, 255, 255), menu)
        self.menuFont = pygame.font.SysFont("comicsansms", 15)
        self.drawText("Restart", self.menuFont, self.screen, WINDOW_WIDTH / 2 - 80, 8 * BLOCK_SIZE - 1, (0, 0, 0))
        self.drawText("Exit", self.menuFont, self.screen, WINDOW_WIDTH / 2 + 20, 8 * BLOCK_SIZE - 1, (0, 0, 0))
        # draw blocks and tiles
        for row in range(0, 8):
            for col in range(0, 8):
                block = self.game.board[row][col]
                chessman_size = BLOCK_SIZE - 2 * PADDING_SIZE
                chessman = pygame.Rect(row * BLOCK_SIZE + PADDING_SIZE, col * BLOCK_SIZE + PADDING_SIZE, chessman_size,
                                       chessman_size)
                if block == 1:
                    self.screen.blit(self.images['black'], chessman)
                elif block == 2:
                    self.screen.blit(self.images['white'], chessman)
                elif block == 0:
                    pass
                else:
                    sys.exit('Error occurs - player number incorrect!')

        # game ending check
        if self.game.victory == -1:
            self.drawText("Draw! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles), self.font,
                          self.screen, 50, 10, (255, 128, 0))
        elif self.game.victory == 1:
            if self.game.useAI:
                self.drawText("You Won! " + str(self.game.blackTiles) + ":" + str(self.game.whiteTiles), self.font,
                              self.screen, 50, 10, (255, 128, 0))
            else:
                self.drawText("Black Won! " + str(self.game.blackTiles) + ":" + str(self.game.whiteTiles), self.font,
                              self.screen, 50, 10, (255, 128, 0))
        elif self.game.victory == 2:
            if self.game.useAI:
                self.drawText("AI Won! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles), self.font,
                              self.screen, 50, 10, (255, 128, 0))
            else:
                self.drawText("White Won! " + str(self.game.whiteTiles) + ":" + str(self.game.blackTiles), self.font,
                              self.screen, 50, 10, (255, 128, 0))

        # update display
        pygame.display.update()

    # Definition of Event Handlers
    def keydownHandler(self, event):
        self.keys_down[event.key] = time.time()

    def keyupHandler(self, event):
        if event.key in self.keys_down:
            del (self.keys_down[event.key])

    def mousedownHandler(self, event):
        pass

    def mouseupHandler(self, event):
        x, y = event.pos
        print("x: " + str(x) + " y: " + str(y))
        # tested - need to change if window size has been changed
        if x >= 115 and x <= 175 and y >= 8 * BLOCK_SIZE:
            self.newGame()
        elif x >= WINDOW_WIDTH / 2 + 20 and x <= WINDOW_WIDTH / 2 + 20 + self.menuFont.size("Exit")[
            0] and y > 8 * BLOCK_SIZE:
            self.quitGame()
        else:
            chessman_x = int(math.floor(x / BLOCK_SIZE))
            chessman_y = int(math.floor(y / BLOCK_SIZE))

            if self.debug:
                print("player " + str(self.game.player) + " x: " + str(chessman_x) + " y: " + str(chessman_y))

            try:
                if len(self.game.history)>0:
                    if self.game.history[-1]['turn']==self.game.player:
                        self.game.history.append(self.game.history[-1])
                        self.game.history[-1]['turn']=3-self.game.player
                self.game.history.append({'state':copy.deepcopy(self.game.board),'turn':copy.deepcopy(self.game.player)})
                self.game.performMove(chessman_x, chessman_y)
            except othello.IllegalMove as e:
                print("Illegal Move " + e.message)
            except Exception as e:
                raise

    def mousemoveHandler(self, event):
        pass


if __name__ == '__main__':
    engine = Game_Engine()
    engine.start()
