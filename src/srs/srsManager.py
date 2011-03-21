# -*- coding: utf-8 -*-
'''
Created on Feb 7, 2011

@author: Yadavito
'''

# own #
from edict.db import DBoMagic
from leitner import Leitner
from etools.tatoeba import TatoebaLookup

class srsScheduler:

    def __init__(self):
        self.db = DBoMagic()
        self.tatoeba = TatoebaLookup()
        
    def initializeAll(self):
        self.tatoeba.loadExamplesFromPickled()
        self.db.frequency.loadFrequencyDict()
        self.db.setupDB()
        
    def activeDB(self):
        return self.db
        
    def initializeCurrentSession(self, sessionSize):
        self.currentItem = u''
        self.currentExample = u''
        
        self.db.initializeCurrentSession(sessionSize)
        
    def endCurrentSession(self):
        self.db.endCurrentSesion()
        
    def getNextItem(self):
        """Get next quiz item reading, set current quiz item"""
        self.currentItem = self.db.getNextQuizItem()
        print self.currentItem.item
        self.currentExample = u''
        #TODO: add check for NoneType
    
    def getCurrentItem(self):
        return self.currentItem.item
    
#    def getCurrentItemKanji(self):
#        return self.currentItem
     
    def getCurrentExample(self):
        self.currentExample = self.tatoeba.getRandomExample(self.currentItem.item)
        return self.currentExample['eng']
    
    def parseCurrentExample(self):
        result = []
        words = self.currentExample['eng'].split(' ')
        for word in words:
            result.append(word + ' ')

#            if not word.endswith('.'):
#                result.append(word + ' ')
#            else:
#                result.append(word)
        return result
        #return self.currentExample['eng'].split(' ')
    
    def getCurrentSentenceTranslation(self):
        return unicode(self.currentExample['rus'], 'utf-8')

    def getQuizVariants(self):
        return self.db.findSimilarReading(self.getCorrectAnswer())
    
    '''    #does not parse the word itself 
    def getCorrectAnswer(self):
        return kata2hira(''.join(MecabTool.parseToReadingsKana(self.currentItem.character)))
    '''
    def answeredWrong(self):
        self.currentItem.leitner_grade = Leitner.grades.None.index
        self.currentItem.next_quiz = Leitner.nextQuiz(self.currentItem.leitner_grade)
        self.db.updateQuizItem(self.currentItem)
        
    def answeredCorrect(self):
        if self.currentItem.leitner_grade != Leitner.grades.Shelved.index:
            self.currentItem.leitner_grade = self.currentItem.leitner_grade + 1            
        self.currentItem.next_quiz = Leitner.nextQuiz(self.currentItem.leitner_grade)
        
        self.db.updateQuizItem(self.currentItem)
    
#    def getCorrectAnswer(self):
#        words = MecabTool.parseToWordsFull(self.currentExample.sentence)
#        answer = self.find(lambda word: self.currentItem.character in word['word'] , words)
#        return kata2hira(answer['pronunciation'])
    
#    def getWordFromExample(self):
#        words = MecabTool.parseToWordsFull(self.currentExample.sentence)
#        answer = self.find(lambda word: self.currentItem.character in word['word'] , words)
#        return answer['word']
    
    # get reading based on word from parse results?
#    def getWordPronunciationFromExample(self, item):
#        words = MecabTool.parseToWordsFull(self.currentExample.sentence)
#        answer = self.find(lambda word: item in word['word'] , words)
#        return kata2hira(answer['pronunciation'])
    
    def find(self, f, seq):
        """Return first item in sequence where f(item) == True."""
        for item in seq:
            if f(item): 
                return item
            
#    def getParsedExampleInFull(self):
#        return MecabTool.parseToWordsFull(self.currentExample.sentence)
#    
#    def getWordNonInflectedForm(self, item):
#        try:
#            return MecabTool.parseToWordsFull(item)[0]['nform']
#        except:
#            return item
        
#    def getWordPronounciation(self, item):
#        try:
#            return kata2hira(MecabTool.parseToWordsFull(item)[0]['pronunciation'])
#        except:
#            return item
    
    def getNextQuizTime(self):
        return self.currentItem.next_quiz.strftime('%d %b %H:%M:%S')
    
    def getLeitnerGradeAndColor(self):
        return {'grade' : str(self.currentItem.leitner_grade), 'name' : Leitner.grades[self.currentItem.leitner_grade].key, 'color' : Leitner.correspondingColor(self.currentItem.leitner_grade)}
