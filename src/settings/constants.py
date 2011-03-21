# -*- coding: utf-8 -*-
'''
Created on Feb 26, 2011

@author: Yadavito
'''

"""Global/useful constants"""

# external #
from enum import Enum

##########################
### dialog positioning ###
##########################

# quiz dialog
D_WIDTH = 660
D_HEIGHT = 176
H_INDENT = D_WIDTH + 10 #indent from right
V_INDENT = D_HEIGHT + 40 #indent from bottom

# info dialog
I_WIDTH = 220
I_HEIGHT = D_HEIGHT
I_INDENT = 2

# status dialog
S_WIDTH = D_WIDTH
S_HEIGHT = 30
S_INDENT = I_INDENT
S_CORRECTION = 0

# options dialog
O_WIDTH = 360
O_HEIGHT = 550

# about dialog
A_WIDTH = 400
A_HEIGHT = 200

# options status dialog
OS_HEIGTH = 30
OS_INDENT = 2 

# quick dictionary        
Q_WIDTH = 700
Q_HEIGTH = 305
Q_INDENT = 400
Q_VINDENT = 56
Q_SPACE = 30

###########################
### paths and resources ###
###########################

SQLITE = 'sqlite:///'
PATH_TO_RES = '../res/'
DBNAME = 'studying.db'
EXAMPLES = 'sentences.csv'
LINKS = 'links.csv'
RESULTING_DICTIONARY = 'tatoeba.pck'
FREQUENCIES_XL = 'SUBTLEX.xlsx'
FREQUENCIES_TXT = 'SUBTLEX.txt'
XL_SHEET = 'out1g'
RESULTING_FREQUENCIES = 'frequencies.pck'

ICONS = 'icons/'
LOGOS = 'logo/'
TRAY = 'tray/'
FREQ = 'frequency/'

###########################
### version information ###
###########################

__version__ = '0.0.1'       #beware: is not imported with '*'
__application__ = 'suzu_ei'    #輪廻／りんね or 鈴ね

###########################
###    quiz generator   ###
###########################

###########################
###      quiz modes     ###
###########################

#modes = Enum('kanji', 'words', 'all')
#
#def modeByKey(key):
#    try:
#        return { 
#                    modes.kanji.key  : modes.kanji,
#                    modes.words.key  : modes.words,
#                    modes.all.key  : modes.all
#                }[key]
#    except KeyError:
#        return modes.all
    
###########################
###     tatoeba urls    ###
###########################

sentences_url = 'http://tatoeba.org/files/downloads/sentences.csv'
links_url = 'http://tatoeba.org/files/downloads/links.csv'