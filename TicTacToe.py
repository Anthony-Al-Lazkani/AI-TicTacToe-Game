import sys
import pygame
from Constants import *
import numpy as np
import random
import copy


#PYGAME INIT
pygame.init()
screen = pygame.display.set_mode(( WIDTH,HEIGHT) )
pygame.display.set_caption("Tic Tac Toe")


#PYGAME BOARD
class Board :
    def __init__(self):
        self.Squares = np.zeros( (Rows, Columns) )
        self.Empty_squares = self.Squares
        self.marked_squares = 0



    def Final_State(self, show=False):

        #Vertical Wins
        for col in range(Columns):
            if self.Squares[0][col] == self.Squares[1][col] == self.Squares[2][col] != 0:
                if show:
                    color = Circle_Color if self.Squares[0][col] == 2 else Cross_Color
                    iPos = (col * Square_Size + Square_Size //2, 20)
                    fPos = (col * Square_Size + Square_Size //2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, Line_width)
                return self.Squares[0][col]
            
        
        #Horizontal Wins
        for row in range(Rows):
            if self.Squares[row][0] == self.Squares[row][1] == self.Squares[row][2] != 0:
                if show:
                    color = Circle_Color if self.Squares[row][0] == 2 else Cross_Color
                    iPos = (20, row * Square_Size + Square_Size //2 )
                    fPos = (WIDTH -20,row * Square_Size + Square_Size //2)
                    pygame.draw.line(screen, color, iPos, fPos, Line_width)
                
                return self.Squares[row][0]
            


        #Descending Diagonal Wins
        if self.Squares[0][0] == self.Squares[1][1] == self.Squares[2][2] != 0:
            if show:
                    color = Circle_Color if self.Squares[1][1] == 2 else Cross_Color
                    iPos = (20, 20 )
                    fPos = (WIDTH -20,HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, Cross_Width)
            return self.Squares[1][1]
    

        #Ascending Diagonal Wins
        if self.Squares[2][0] == self.Squares[1][1] == self.Squares[0][2] != 0:
            if show:
                    color = Circle_Color if self.Squares[1][1] == 2 else Cross_Color
                    iPos = (20, HEIGHT - 20 )
                    fPos = (WIDTH -20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, Cross_Width)
            return self.Squares[1][1]
        
        #No Win Yet
        return 0
    

    def Mark_Square(self, row, column, player):
        self.Squares[row][column] = player
        self.marked_squares += 1

    def Empty_Square(self, row, col):
        return self.Squares[row][col] == 0
    

    def Get_Empty_Squares(self):
        Empty_Squares = []
        for row in range(Rows):
            for col in range(Columns):
                if self.Empty_Square(row, col):
                    Empty_Squares.append( (row, col))

        return Empty_Squares
    

    def IsFull(self):
        return self.marked_squares == 9
    

    def IsEmpty(self):
        return self.marked_squares == 0
    


#Artificial Intelligence Implementation
class AI:
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player


    def Random_Choice(self, Board):
        Empty_sqrs = Board.Get_Empty_Squares()
        index = random.randrange(0, len(Empty_sqrs))

        return Empty_sqrs[index]
    
    def minimax(self, Board, maximizing):
        #Terminal cases
        case = Board.Final_State()

        #Player 1 wins
        if case == 1:
            return 1, None
        
        #Player 2 wins
        if case == 2:
            return -1, None
        
        # Draw
        elif Board.IsFull():
            return 0, None
        
        if maximizing:
            alpha = -2
            best_move = None
            Empty_sqrs = Board.Get_Empty_Squares()


            for (row, col) in Empty_sqrs:
                temp_board = copy.deepcopy(Board)
                temp_board.Mark_Square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > alpha:
                    alpha = eval
                    best_move = (row, col)

            return alpha, best_move

        elif not maximizing:
            beta = 2
            best_move = None
            Empty_sqrs = Board.Get_Empty_Squares()


            for (row, col) in Empty_sqrs:
                temp_board = copy.deepcopy(Board)
                temp_board.Mark_Square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < beta:
                    beta = eval
                    best_move = (row, col)

            return beta, best_move



    def eval(self, Main_Board):
        if self.level == 0:
            #Random Choice
            eval = 'random'
            move = self.Random_Choice(Main_Board)


        else:
            #Minimax algorithm choice
            eval, move = self.minimax(Main_Board, False)

        print(f'AI has chosen to mark the square in position {move} with an eval of {eval}')

        return move 





#PYGAME Game
class Game :
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 2 # Player 1 - Cross,  Player 2 - Cicrle
        self.gamemode = 'ai'    # Player vs Player or AI
        self.running = True 
        self.show_lines()


    def make_move(self, row, col):
        self.board.Mark_Square(row, col, self.player)
        self.draw_fig(row, col)
        self.Next_Turn()



    def show_lines(self) :
        #Background color for restarting
        screen.fill( Background_Color)
        #Vertical Lines
        pygame.draw.line(screen, Line_color, (Square_Size, 0), (Square_Size, HEIGHT), Line_width)
        pygame.draw.line(screen, Line_color, (WIDTH - Square_Size, 0), (WIDTH - Square_Size, HEIGHT), Line_width)



        #Horizontal Lines
        pygame.draw.line(screen, Line_color, (0, Square_Size), (WIDTH, Square_Size), Line_width)
        pygame.draw.line(screen, Line_color, (0, HEIGHT - Square_Size), (WIDTH, HEIGHT - Square_Size), Line_width)

        
    def draw_fig(self, row, col) :
        if self.player == 1 :
            #Cross Drawing

            #Descending Line
            Start_Descending = (col * Square_Size+ Offset, row * Square_Size + Offset)
            End_Descending = (col * Square_Size + Square_Size - Offset, row * Square_Size + Square_Size - Offset)
            pygame.draw.line(screen, Cross_Color, Start_Descending, End_Descending, Cross_Width)

            #Ascending Line
            Start_Ascending = (col * Square_Size+ Offset, row * Square_Size + Square_Size - Offset)
            End_Ascending = (col * Square_Size + Square_Size - Offset, row * Square_Size +  Offset)
            pygame.draw.line(screen, Cross_Color, Start_Ascending, End_Ascending, Cross_Width)


        elif self.player == 2 :
            #Draw a Circle
            Center = (col * Square_Size + Square_Size //2, row* Square_Size + Square_Size // 2)
            pygame.draw.circle(screen, Circle_Color, Center, RADIUS, Circle_Width)



    def Next_Turn(self) :
        self.player = self.player %2 + 1


    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def IsOver(self):
        return self.board.Final_State(show=True) != 0 or self.board.IsFull()


    def restart(self):
        self.__init__()



#PYGAME THEME
screen.fill( Background_Color )


def main():

    #Object
    game = Game()
    board = game.board
    ai = game.ai
    
    #Main Loop
    while True :

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                #g --Gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()


                #r-Restart
                if event.key == pygame.K_r:
                    game.restart()
                    board = game.Board
                    ai = game.ai

                #0 - random ai
                if event.key == pygame.K_0:
                    ai.level =0

                #0 - random ai
                if event.key == pygame.K_1:
                    ai.level =1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // Square_Size
                col = pos[0] // Square_Size

                if board.Empty_Square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.IsOver():
                        game.running = False

                    

                
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()    #update the screen


            #ai methods
            row, col = ai.eval(board)


            board.Empty_Square(row, col)
            board.Mark_Square(row, col, game.player)
            game.draw_fig(row, col)
            game.Next_Turn()

            if game.IsOver():
                        game.running = False




        pygame.display.update()




main()
