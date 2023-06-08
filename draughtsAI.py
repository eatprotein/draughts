# -*- coding: utf8 -*-
#
# INFO-F106 - Projet d'année - Partie 4
#
# GÉRARD Pierre  000379259


from random import choice,shuffle
from draughtsFunctions import *

# Nouvelle variable défini dans config.py et réecrit ici dans le cas ou l'on
# ne pouvait pas modifier config.py
PLAYER_VS_PLAYER = 0
PLAYER_VS_WHITE_COMPUTER = 1
PLAYER_VS_BLACK_COMPUTER = -1


class ArtificialIntelligence(object):
    """docstring for ArtificialIntelligence"""
    def __init__(self, board, player):
        """ """
        self.player = player
        self.listOfComputerPawn = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 0 and playerColor(board[i][j]) == player:
                    coordinates = (i, j)
                    self.listOfComputerPawn.append(coordinates)

    def checkListComputerPawn(self, board):
        """verifie si tout les pions contenues dans la liste listOfComputerPawn
        sont bien encore sur le damier. Les retire sinon"""
        toRemove = []
        for pawn in self.listOfComputerPawn:
            i, j = pawn
            if isFree(board,i,j) or playerColor(board[i][j]) != self.player:
                toRemove.append(pawn)
        for pawnToRemove in toRemove:
            self.listOfComputerPawn.remove(pawnToRemove)

    def willCapture(self,board, i, j, direction, length):
        """Verifie si le mouvement passé en paramètre va capture un pion"""
        newpos = getNewCoord(i, j, direction, self.player, length)
        destI, destJ = newpos
        if not isFree(board,destI,destJ):
            return True
        return False

    def safeMove(self, board, i, j, direction, length):
        """Check that the arrival square of the move passed as a parameter cannot lead to an immediate capture
        by the opposing player, i.e. check that: on the new position there is not at the same time an opposing
        piece in one direction and a free square just after the piece in the opposite direction. If the movement
        passed as a parameter indicates a capture, shift the whole by 1 in the direction of the movement."""
        newpos = getNewCoord(i, j, direction, self.player, length)
        destI, destJ = newpos
        capture = False
        if not isFree(board,destI,destJ): #Capture => On decale
            i,j = destI,destJ
            newpos = getNewCoord(destI, destJ, direction, self.player, 1)
            destI, destJ = newpos
            capture = True
        for possibleDirection in ("L", "LB", "R", "RB"):
            if possibleDirection != reverseDirection(direction) or capture:
                nbrFree = countFree(board, destI, destJ, possibleDirection, -self.player)
                adversePossible = getNewCoord(destI, destJ, possibleDirection, self.player, nbrFree + 1)  
                freeSpace = getNewCoord(destI, destJ, possibleDirection, self.player, -1)
                advI, advJ = adversePossible
                frI, frJ = freeSpace
                if not outside(board,advI,advJ) and not outside(board,frI,frJ):
                    if nbrFree == 0:
                        if (board[advI][advJ] != 0 and playerColor(board[advI][advJ]) == -self.player) and (board[frI][frJ] == 0 or (frI, frJ) == (i, j)):
                            return False
                    else: # If the opponent's piece is not on the adjacent square => check if it is a king
                        if (board[advI][advJ] != 0 and playerColor(board[advI][advJ])) == -self.player and isKing(board,advI,advJ) and (board[frI][frJ] == 0 or (frI, frJ) == (i, j)):
                            return False
        return True

    def multiCapt(self,board,i,j):
        """Manage roundups, continue to make catches as long as possible"""
        movementWithCapture = []
        for direction in ("L", "LB", "R", "RB"):
            maxLenght = 1
            if isKing(board,i,j):
                maxLenght += countFree(board, i, j, direction)
            for length in range(1, maxLenght + 1):
                if checkMove(board, i, j, direction, self.player,length) == 0:
                    if self.willCapture(board,i, j, direction, length):
                        movementParameters = (i, j, direction, length)
                        movementWithCapture.append(movementParameters)
        if movementWithCapture != []:
            return choice(movementWithCapture)
        return False

    def findMove(self, board):
        """Reflects the movement chosen according to precise characteristics that  the player can perform"""
        shuffle(self.listOfComputerPawn)  # melange pour choisir N pion aleatoirement
        consideredPawn = self.listOfComputerPawn[:N_PAWN] # choisit N pion
        for pawnCoordinates in consideredPawn:
            i, j = pawnCoordinates
            for direction in ("L", "LB", "R", "RB"):
                maxLenght = 1
                if isKing(board,i,j):
                    maxLenght += countFree(board, i, j, direction)
                for length in range(1, maxLenght + 1):
                    if checkMove(board, i, j, direction, self.player, length) == NO_ERROR:
                        movementParameters = (i, j, direction, length)
                        if self.willCapture(board,i, j, direction, length):
                            return movementParameters
        # On remelange une fois pour choisir aleatoirement un mouvement parmis
        # N pions
        shuffle(self.listOfComputerPawn)
        consideredPawn = self.listOfComputerPawn[:N_PAWN]
        for pawnCoordinates in consideredPawn:
            i, j = pawnCoordinates
            for direction in ("L", "LB", "R", "RB"):
                maxLenght = 1
                if isKing(board,i,j):
                    maxLenght += countFree(board, i, j, direction)
                for length in range(1, maxLenght + 1):
                    if checkMove(board, i, j, direction, self.player, length) == NO_ERROR:
                        movementParameters = (i, j, direction, length)
                        if self.safeMove(board, i, j, direction, length):
                            return movementParameters
        # On remelange une fois pour choisir aleatoirement un mouvement parmis
        # tout les pions
        shuffle(self.listOfComputerPawn)
        for pawnCoordinates in self.listOfComputerPawn:
            i, j = pawnCoordinates
            for direction in ("L", "LB", "R", "RB"):
                maxLenght = 1
                if isKing(board,i,j):
                    maxLenght += countFree(board, i, j, direction)
                for length in range(1, maxLenght + 1):
                    if checkMove(board, i, j, direction, self.player, length) == NO_ERROR:
                        return (i, j, direction, length)
        raise ValueError("There is no movement possible on this board for AI")

    def play(self, board):
        """Fonction principal, fait jouer le joueur"""
        self.checkListComputerPawn(board)
        i, j, direction, length = self.findMove(board)
        des, capt = movePiece(board, i, j, direction, length)
        self.listOfComputerPawn.append(des)
        self.listOfComputerPawn.remove((i, j))
        becomeKing(board, des[0], des[1])
        if capt != None:
            i, j = des
            capture(board, capt[0], capt[1])
            nextMove = self.multiCapt(board ,i, j)
            while nextMove:
                i, j, direction, length = nextMove
                des, capt = movePiece(board, i, j, direction, length)
                self.listOfComputerPawn.append(des)
                self.listOfComputerPawn.remove((i, j))
                becomeKing(board, des[0], des[1])
                i, j = des
                capture(board, capt[0], capt[1])
                nextMove = self.multiCapt(board ,i, j)