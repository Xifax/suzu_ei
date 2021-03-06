# -*- coding: utf-8 -*-
'''
Created on Feb 11, 2011

@author: Yadavito
'''
# own #
from settings.constants import __version__
# external #
from userconfig import UserConfig

class Options:
    
    def __init__(self):
        #self.APP_NAME = __application__
        self.APP_NAME = 'suzu_ei'
        
        #default settings    #TODO: group fonts settings
        self.OPTIONS = [('SentenceFont',    #sentences font
                {'name' : u'Cambria',
                 'size' : 14,
                 }),
                 ('QuizFont',               #quiz answers font
                  {'name' : u'Calibri',
                   'size' : 12,
                   }),
                  ('MessageFont',           #messages font
                  {'name' : u'Cambria',
                   'size' : 12,
                   }),
                  ('InfoFont',              #messages font
                  {'name' : u'Calibri',
                   'size' : 12,
                   }),
                 ('Intervals',              #time constraints
                  {'repetition' : 1,        #minutes
                   'countdown'  : 30,       #seconds
                   }),
                 ('Active',                 #active tags and mode
                  {'tags' : [],             #tags names (as, jlpt2,3 etc)
                   'mode' : 'kanji',        #kanji, words or both
                   }),
                 ('Launch',                 #launch options
                  {'autoquiz'   : False,    #start quiz on launch
                   'splash'     : False,    #splash on start
                   }),
                ('Runtime',                 #runtime options
                  {'ontop'      : True,     #always on top
                   'global'     : True,     #enable global hotkeys
                   'log'        : False,    #enable errors logging
                   'sound'      : False,    #enable sound
                   'fade'       : True,     #enable fade effect
                   'background' : False,    #draw item color in background
                   'plastique'  : True,    #use plastique theme
                   'preload'    : True,    #preload jmdict
                   }),
                 ('Session',                #session parameters
                  {'size'       : 300,      #number of items in session
                   'length'     : 600,      #maximum repetitions/day
                   }),
                 ('Dict',                   #dictionary options
                  {'lang'       : 'eng',    #translation language
                   'default'    : 'jmdict', #default dictionary
                   }),
               ]
        
        #creates or reads from app.ini in Users/username/
        self.CONFIG = UserConfig(self.APP_NAME, self.OPTIONS, version=__version__)
    ### fonts ###
    def getSentenceFont(self):
        return self.CONFIG.get('SentenceFont', 'name')   
    
    def getQuizFont(self):
        return self.CONFIG.get('QuizFont', 'name')
    
    def getMessageFont(self):
        return self.CONFIG.get('MessageFont', 'name')
    
    def getInfoFont(self):
        return self.CONFIG.get('InfoFont', 'name')
    
    def getSentenceFontSize(self):
        return self.CONFIG.get('SentenceFont', 'size')
    
    def getQuizFontSize(self):
        return self.CONFIG.get('QuizFont', 'size')
    
    def getMessageFontSize(self):
        return self.CONFIG.get('MessageFont', 'size')
    
    ### intervals ###
    def getRepetitionInterval(self):
        return self.CONFIG.get('Intervals', 'repetition')
    
    def getCountdownInterval(self):
        return self.CONFIG.get('Intervals', 'countdown')
    
    def setRepetitionInterval(self, interval):
        self.CONFIG.set('Intervals', 'repetition', interval)
    
    def setCountdownInterval(self, interval):
        self.CONFIG.set('Intervals', 'countdown', interval)
    
    ### session ###
    def getSessionSize(self):
        return self.CONFIG.get('Session', 'size')
    
    def getSessionLength(self):
        return self.CONFIG.get('Session', 'length')
    
    def setSessionSize(self, number):
        self.CONFIG.set('Session', 'size', number)
    
    def setSessionLength(self, number):
        self.CONFIG.set('Session', 'length', number)
    
    ### launch ###
    def isQuizStartingAtLaunch(self):
        return self.CONFIG.get('Launch', 'autoquiz')
    
    def setQuizStartingAtLaunch(self, flag):
        self.CONFIG.set('Launch', 'autoquiz', flag)
        
    def isSplashEnabled(self):
        return self.CONFIG.get('Launch', 'splash')
    
    def setSplashEnabled(self, flag):
        return self.CONFIG.get('Launch', 'splash', flag)
    
    ### quiz ###
    def getQuizMode(self):
        return self.CONFIG.get('Active', 'mode')
    
    ### runtime ###
    def isAlwaysOnTop(self):
        return self.CONFIG.get('Runtime', 'ontop')
        
    def isSoundOn(self):
        return self.CONFIG.get('Runtime', 'sound')
    
    def isGlobalHotkeyOn(self):
        return self.CONFIG.get('Runtime', 'global')
    
    def isLoggingOn(self):
        return self.CONFIG.get('Runtime', 'log')
    
    def isBackgroundOn(self):
        return self.CONFIG.get('Runtime', 'background')
        
    def isFadeEffectOn(self):
        return self.CONFIG.get('Runtime', 'fade')
    
    def isPlastique(self):
        return self.CONFIG.get('Runtime', 'plastique')
    
    def isPreloading(self):
        return self.CONFIG.get('Runtime', 'preload')
    
    def setAlwaysOnTop(self, flag):
        self.CONFIG.set('Runtime', 'ontop', flag)
        
    def setSoundOn(self, flag):
        self.CONFIG.set('Runtime', 'sound', flag)
    
    def setGlobalHotkeyOn(self, flag):
        self.CONFIG.set('Runtime', 'global', flag)
    
    def setLoggingOn(self, flag):
        self.CONFIG.set('Runtime', 'log', flag)
        
    def setFadeEffectOn(self, flag):
        self.CONFIG.set('Runtime', 'fade', flag)
    
    def setBackgroundOn(self, flag):
        self.CONFIG.set('Runtime', 'background', flag)
        
    def setPlastique(self, flag):
        self.CONFIG.set('Runtime', 'plastique', flag)
        
    def setPreloading(self, flag):
        self.CONFIG.set('Runtime', 'preload', flag)
    
    ### dictionary ###
    def getLookupLang(self):
        return self.CONFIG.get('Dict', 'lang')
    
    def setLookupLang(self, lang):
        self.CONFIG.set('Dict', 'lang', lang)
        
    def getLookupDict(self):
        return self.CONFIG.get('Dict', 'default')
    
    def setLookupDict(self, dict):
        self.CONFIG.set('Dict', 'default', dict)