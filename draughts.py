# -*- coding: utf8 -*-
#
# INFO-F106 - Projet d'année - Partie 4
#
# GÉRARD Pierre  000379259

from draughtsAI import *
from draughtsFunctions import *
import sys
from os.path import *

# Le code de draughts.py a été repris du corrigé en grande partie (plus claire)
# et placé en classe avec gestion des exceptions

class Draughts(object):
    """Gère la structure du damier"""
    def __init__(self,mode):
        self.dimension = DIMENSION
        self.board = initBoard(self.dimension)
        self.player = WHITE_PLAYER
        self.computerPlayer = False
        self.finished = False
        self.captured = False
        self.played = False
        self.mode = mode
        self.setMode(mode)

    def setPlayer(self, newPlayer):
        """Modifie le joueur actuel"""
        self.player = newPlayer

    def setMode(self,mode):
        """docstring """
        self.mode = mode
        if mode == PLAYER_VS_PLAYER:
            self.computerPlayer = False
        if mode == PLAYER_VS_WHITE_COMPUTER:
            self.player = BLACK_PLAYER
            self.computerPlayer = ArtificialIntelligence(self.board, WHITE_PLAYER)
            self.nextPlayer(self.player)
        if mode == PLAYER_VS_BLACK_COMPUTER:
            self.player = WHITE_PLAYER
            self.computerPlayer = ArtificialIntelligence(self.board, BLACK_PLAYER)

    def setBoard(self, newBoard):
        """Modifie le damier"""
        self.board = newBoard

    def setFinished(self, newFinished):
        """modifie la fin de la partie"""
        self.finished = newFinished

    def getBoard(self):
        """Renvoi le damier"""
        return self.board

    def getMode(self):
        """docstring """
        return self.mode

    def getPlayer(self):
        """Renvoi le joueur actuel"""
        return self.player

    def getDimension(self):
        """Renvoi la dimension du damier"""
        return self.dimension

    def getPlayed(self):
        """Renvoi si le joueur a joué ou pas"""
        return self.played

    def getCaptured(self):
        """Renvoi la capture effectué par le joueur"""
        return self.captured

    def getFinished(self):
        """Renvoi si le jeu est terminé ou pas"""
        return self.finished

    def sayWinner(self):
        """Indique le gagnant"""
        return 'Draw game, both players are blocked' if(self.finished == 0) else (nameOf(self.finished) + " wins the game !")

    def askEndOfTurn(self):
        """ Permet de savoir si un joueur peut terminer son tour"""
        if self.played:
            self.player = self.nextPlayer(self.player)
            self.played = False
            self.captured = False
            return True
        return False

    def makeMove(self, row, col, direction, moves):
        """Effectue un mouvement si possible et renvoi l'erreur si une erreur
        se produit"""
        direction = direction.upper()
        error = checkMove(self.board, row, col, direction, self.player, moves, self.played, self.captured)
        if(error == NO_ERROR):
            dst, self.captured = movePiece(self.board, row, col, direction, moves)
            if(self.captured != None):
                y, x = self.captured
                capture(self.board, y, x)
                self.captured = True
            row, col = dst
            self.played = row, col
            if(not self.captured):
                self.playAgain = False
            becomeKing(self.board, row, col)
            self.finished = checkEndOfGame(self.board, self.player)
        return error

    def prompt(self):
        """Permet en ligne de commande au joueur de terminer son tour"""
        print(nameOf(self.player), "player, type one of:")
        print("\t- 'r' to send an interrupt request (ask to the other player)")
        print("\t- 's' to save the game")
        print("\t- 'l' to load a game")
        print("\t- 'p' to print board")
        print("\t- a character from 'a' to 'j' to select a piece (x-coordinate)")
        choice = stdread(True)
        if(len(choice) == 1 and ((choice >= 'a' and choice <= 'j') or (choice in ('r', 's', 'l')))):
            if(choice == 'r'):  # <<< Draw
                print(nameOf(self.player), " send an interrupt request.")
                print(nameOf(self.nextPlayer(self.player)), " player, do you accept? ([y]es/[n]o)")
                if(stdread(True) in ('y', 'yes')):
                    print("Accepted. Interrupt.")
                    return False, 0, -1
                else:
                    print("Refused. Continue")
            elif(choice in ('l', 's')):  # <<< load or save
                print("Give a path to the file ending by '.dat', please.")
                fileName = stdread()
                if(isDAT(fileName)):
                    saveAction = choice == 's'
                    loadAction = not saveAction
                    if(isfile(fileName)):
                        if(saveAction):
                            print("Are you sure to overwrite? ([y]es/[n]o)")
                            saveAction = stdread(True) in ('y', 'yes')
                    elif(loadAction):
                        print("Cannot load, file not found.")
                    if(saveAction):
                        try:
                                save(fileName, self.board, self.player, PLAYER_VS_PLAYER)
                                print("file saved.")
                        except IOError:
                            print("I/O Error")
                    elif(loadAction):
                        try:
                            self.player,mode, self.board = load(fileName)
                            print("file loaded.")
                            return False, self.player, self.board
                        except TypeError:
                            print("Bad format")
                        except IOError:
                            print("I/O Error")
                    else:
                        print("Abording")
                else:
                    print("Not a *.dat file")
            else:   # <<<<    Play
                print("Enter the y-coordinate to select the piece.")
                try:
                    y = int(stdread())
                    if(y < 1 or y > 10):
                        raise ValueError("invalid number to select a row : '", y, "'")
                    return True, y - 1, ord(choice) - ord('a')
                except ValueError:
                    print("Not a correct row number.")
        elif(choice == 'p'):    # < Print
            printBoard(self.board, self.player)
        else:
            print("Wrong input, please try again")
        return self.prompt()

    def main(self):
        """Fonction principale du jeu en ligne de commande"""
        while(isinstance(self.finished, bool) and (not self.finished)):  # not self.finished is not useful
            printBoard(self.board, self.player)
            normalInput, row, col = self.prompt()
            if(normalInput):
                self.playAgain = True
                self.captured = False
                self.played = False
                while(self.playAgain):
                    direction, moves = self.promptDirection(isKing(self.board, row, col))
                    # ---- cut -----
                    if(direction == 's'):
                        self.playAgain = False
                        if(not self.played):
                            print('Player want to select another piece.')
                            self.player = self.nextPlayer(self.player)
                    else:
                        error = self.makeMove(row, col, direction, moves)
                        if error == NO_ERROR:
                            printBoard(self.board, self.player)
                        else:
                            print('Error: ' + strerr(error) + '.')
                            if(error in (NO_PIECE, OPPONENT_PIECE)):
                                self.playAgain = False
                                self.player = self.nextPlayer(self.player)
                    self.finished = checkEndOfGame(self.board, self.player)
                    if(isinstance(self.finished, int) and self.finished != 0):
                        self.playAgain = False
                becomeKing(self.board, row, col)
                self.player = self.nextPlayer(self.player)
                self.finished = checkEndOfGame(self.board, self.player)
            elif(row != 0):
                self.player, self.board = row, col  # game loaded
            else:
                self.finished = 0  # Abording (interrupt request)
        self.player = self.nextPlayer(self.player)
        print(self.sayWinner())


    def promptDirection(self,askNumberOfMoves=False):
        """Demande la direction du déplacement au joueur"""
        print("Select a direction, please.")
        print("\tL, R, LB, RB or S ((L)eft, (R)ight, (B)ack, (S)top).")
        direction = stdread(True)
        if(askNumberOfMoves and direction != 's'):
            try:
                print("Give the number of successive moves")
                moves = int(stdread())
                if(moves < 1):
                    raise ValueError("invalid number of moves, must be > 1 : '", moves, "'")
                return direction, moves
            except ValueError:
                print("Not a correct number of moves.")
                return self.promptDirection(askNumberOfMoves)
        return direction, 1

    def nextPlayer(self,player):
        if not self.computerPlayer:
            return (-1) * player
        else:
            self.computerPlayer.play(self.board)
            self.finished = checkEndOfGame(self.board,-player)
            return player


if __name__ == '__main__':
    game = Draughts(PLAYER_VS_PLAYER)
    game.main()
