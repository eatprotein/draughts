#!/usr/bin/python
# -*- coding: utf8 -*-

# uncomment the following lines if you have a problem of characters
#import sys,codecs
#if(sys.stdout.encoding != 'UTF-8'):
#	sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Part 1
DIMENSION=10

WHITE_SQUARE = "\u2587"
BLACK_SQUARE = "\u0020"

WHITE_PAWN = "\u25CF"
BLACK_PAWN = "\u25CB"

FREE_SPACE = 0
WHITE_PLAYER = 1
BLACK_PLAYER = -1

# Part 2
BLACK_KING = "\u25CE"
WHITE_KING = "\u25C9"

NO_ERROR					= 0
PAWN_ONLY_ONE_MOVE	= 1
BAD_DIRECTION_FORMAT	= 2
ONLY_KING_GO_BACK		= 3
SPACE_OCCUPIED			= 4
CANNOT_JUMP_OUTSIDE	= 5
TOO_LONG_JUMP			= 6
CANNOT_GO_OUTSIDE		= 7
NO_FREE_WAY				= 8
NO_PIECE					= 9
OPPONENT_PIECE			= 10
MUST_CAPTURE			= 11

# Part 4 

N_PAWN = 10
PLAYER_VS_PLAYER = 0
PLAYER_VS_WHITE_COMPUTER = 1
PLAYER_VS_BLACK_COMPUTER = -1