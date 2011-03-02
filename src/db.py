# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2011

@author: Yadavito
'''

from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc, and_
from elixir import Entity,Field,Unicode,Integer,TIMESTAMP,ManyToMany,\
metadata,session,create_all,setup_all,BOOLEAN

#import time
from datetime import datetime
import os.path
from random import shuffle, sample, randrange
from itertools import permutations

from leitner import Leitner
from constants import *
from jcconv import hira2kata

def removeDuplicates(list):
    set = {}
    return [set.setdefault(e,e) for e in list if e not in set]

class Kanji(Entity):
    character = Field(Unicode(1))
    tags = Field(Unicode(128))
    
    # srs params for kanji mode
    next_quiz = Field(TIMESTAMP)
    leitner_grade = Field(Integer)
    
    # session params
    active = Field(BOOLEAN)
    current_session = Field(BOOLEAN)
    been_in_session = Field(Integer)        #for statistics and control
    # additional
    #wrong_in_current_session = Field(Integer)    #NB: uncomment when db is recreated  
    
    # relationns
    example = ManyToMany('Example')
    word = ManyToMany('Word')
    
class Word(Entity):
    word = Field(Unicode(16))
    
    # srs params for words mode
    next_quiz = Field(TIMESTAMP)
    leitner_grade = Field(Integer)
    
    # session params
    active = Field(BOOLEAN)
    current_session = Field(BOOLEAN)
    been_in_session = Field(Integer) 
    # additional
    #wrong_in_current_session = Field(Integer)
    
    # relations
    kanji = ManyToMany('Kanji')
    example = ManyToMany('Example') #is it correct?

class Example(Entity):
    sentence = Field(Unicode(256))
    translation = Field(Unicode(256))
    
    # relations
    kanji = ManyToMany('Kanji')
    word = ManyToMany('Word') #is it correct?

class DBoMagic:
    
    def __init__(self):
        self.metadata = metadata
        self.metadata.bind = SQLITE + PATH_TO_RES + DBNAME      #TODO add check up
        self.db = ()    #kanjidic2 db
        
    def setupDB(self):  
        """Initialize/read database on disk"""
        self.db = SqlSoup(SQLITE + PATH_TO_RES + KANJIDIC2)     #TODO: add check up
        setup_all()
        if not os.path.exists(PATH_TO_RES + DBNAME):
            create_all()
    
    def getNextQuizItem(self):          #mode and active check does not needed
        #TODO: implement witch great verve and so on!
        #TODO: check if item.next_quiz is the same for multiple items
        #...
        return  Kanji.query.filter_by(current_session = True).order_by(asc(Kanji.next_quiz)).first()
        
    # each time application is launched    (session_size from options) #mode for kanji, words or both
    def initializeCurrentSession(self, mode, sessionSize):
        if mode == 'kanji':
            selection = Kanji.query.filter_by(active = True).all()
        elif mode == 'words':
            selection = Word.query.filter_by(active = True).all()
        else:
            selection = () # Kanji && Words?
        
        n = sessionSize
        
        shuffle(selection)
        if n > len(selection) : n = len(selection)      # without any try's and ValueErrors
        random_selection = sample(selection, n)

        # serious stuff ahead!
        for item in random_selection:
            # mark n random items as 'current' 
            item.current_session = True
            item.been_in_session = item.been_in_session + 1     #may be useful later on
            
        session.commit()

    def endCurrentSesion(self):
        for kanji in Kanji.query.all():
            kanji.current_session = False
        for word in Word.query.all():
            word.current_session = False    
        
        session.commit()

    def updateQuizItem(self, item):
        session.commit()
    '''    
    def updateQuizItemByValue(self, itemValue, newGrade, nextQuiz):
        
        result = Kanji.query.filter_by(character = itemValue).all()
        if 2 > len(result) > 0:
            result[0].leitner_grade = newGrade
            result[0].next_quiz = nextQuiz
        else:
            result = Word.query.filter_by(word = itemValue).all()
            if 2 > len(result) > 0:
                result[0].leitner_grade = newGrade
                result[0].next_quiz = nextQuiz
                
        session.commit()
    '''   
    
    def addWordToDbAndLinkToExample(self, kanji, word, sentence):
        if len(word) > 1:
            if(len(Word.query.filter_by(word = word).all()) == 0):
                newWord = Word(word = word, next_quiz = datetime.now(), leitner_grade = Leitner.grades.None.index, active = True, 
                    current_session = False, been_in_session = 0)
                kanji.word.append(newWord)
                sentence.word.append(newWord)
                session.commit()
    
    def addKanjiToDb(self, character):
        Kanji(character = character)
        session.commit()
        
    def addSentenceToDb(self, kanji, sentence, translation):
        Kanji.query.filter_by(character = kanji).one().example.append(Example(sentence = sentence,translation = translation))          #or get_by
        #k.example.append(Example(sentence = sentence,translation = translation)) 
        session.commit()
        
    def addWordToDb(self, kanji, word):
        """Adds word corresponding to kanji from quiz/example"""
        if len(word) > 1:
            if(len(Word.query.filter_by(word = word).all()) == 0):
                kanji.word.append(Word(word = word, next_quiz = datetime.now(), leitner_grade = Leitner.grades.None.index, active = True, 
                    current_session = False, been_in_session = 0))
                session.commit()
    
    def addExamplesForKanji(self, kanji, examples):
        for example in examples:
            kanji.example.append(Example(sentence = example,translation = examples[example]))
        session.commit()
            
    def getExample(self, kanji):
        examples = kanji.example
        return examples[randrange(0, len(examples))]
        
    #TODO: throw away unneeded implementation
    '''
    def checkIfKanjiHasExamplesByValue(self, kanjiValue):
        try:
            if len(Kanji.query.filter_by(character = kanjiValue).one().example) > 0:
                return True
            else: 
                return False
        except NoResultFound:
            return False
        
    def checkIfKanjiHasWordsByValue(self, kanjiValue):
        try:
            if len(Kanji.query.filter_by(character = kanjiValue).one().word) > 0:
                return True
            else: 
                return False
        except NoResultFound:
            return False
    '''    
    def checkIfKanjiHasWords(self, kanji):
        if len(kanji.word) > 0:
            return True
        else:
            return False
        
    def checkIfKanjiHasExamples(self, kanji):
        if len(kanji.example) > 0:
            return True
        else:
            return False
        
    def findSimilarReading(self, kana):
        """Generate quiz variants based on correct reading ('kana' argument)"""
        #print kana  #NB: somewhere around here there is a bug!
        
        size = len(kana) - 1
        #size = len(kana) - 2
        readings = []
        selection = []
        count = 0
        
        #selection = self.db.kunyomi_lookup.filter(self.db.kunyomi_lookup.reading.like(kana[0] + u'_' * size + kana[len(kana) - 1])).all()
        #TODO: debug this section
        #while len(selection) < 4:
        while True:
            selection = self.db.kunyomi_lookup.filter(self.db.kunyomi_lookup.reading.like(kana[0] + u'_' * size)).all()
            #selection = removeDuplicates(selection)
        
            if len(selection) >= 4:
                rand = sample(selection, 4)
                for read in rand:
                    readings.append(read.reading)
                    
            else:
                perm = list(map(''.join, permutations(kana)))
                if len(perm) >= 4:
                    readings = sample(perm, 4)
                else:
                    kanaTable = KANA_TABLE
                    i = 0; variant = u''
                    while i < 4:
                        j = 0
                        while j < size:
                            variant += kanaTable[randrange(0, len(kanaTable))];    j = j + 1
                        readings.append(variant);   variant = u'';  i = i + 1
                
            readings = removeDuplicates(readings)   
            #print ' '.join(readings) #THIS IS FOR TEST ONLY     
            count = count + 1
            
            if len(readings) >= 4: break
            if count > 3: break
                
        #inserting correct reading at random position (if not already)
        print ' '.join(readings) #THIS IS FOR TEST ONLY     
        if kana not in readings:
            if len(readings) >= 4:
                readings[randrange(0, 4)] = kana
            else:
                readings[randrange(0, len(readings))] = kana
        print ' '.join(readings) #THIS IS FOR TEST ONLY     

        return readings
    
    def addItemsToDbJlpt(self, jlptGrade):
        try:
            jlptGrade = int(jlptGrade)
            if 0 < jlptGrade < 5:
                selection = self.db.character.filter(self.db.character.jlpt==jlptGrade).all()
                #TODO: add or_ for grade, jlpt and frequency
                #time for next quiz
                now = datetime.now()
                
                jlpt = u'jlpt' + str(jlptGrade)
                
                for kanji in selection:
                    # VERY time consuming
                    #_now = time.time()
                    # in theory, it can be thrown away
                    '''
                    readings_kun = self.db.reading.filter(and_(self.db.reading.fk==kanji.id, self.db.reading.type=='ja_kun')).all()
                    readings_on = self.db.reading.filter(and_(self.db.reading.fk==kanji.id, self.db.reading.type=='ja_on')).all()
                    meaning = self.db.meaning.filter(and_(self.db.meaning.fk==kanji.id, self.db.meaning.lang=='en')).all()
                    #_after = time.time()
                    
                    #sum += _after - _now
                    #print _after - _now
                
                    kun_string = u''
                    on_string = u''
                    meaning_string = u''
                
                    if len(readings_kun) > 0:
                        for kun in readings_kun:
                            kun_string += kun.value + ';'
                        
                    if len(readings_on) > 0:
                        for on in readings_on:
                            on_string += on.value + ';'
                    
                    if len(meaning) > 0:
                        for m in meaning:
                            meaning_string += m.value + ';'
                
                    Kanji(character = kanji.literal, tags = jlpt, reading_kun = kun_string, reading_on = on_string, meaning = meaning_string, 
                          next_quiz = now, leitner_grade = Leitner.grades.None.index, active = True, current_session = False, been_in_session = 0)
                    '''
                    #check if already exists    (time consuming?)
                    if len(Kanji.query.filter_by(character = kanji.literal).all()) == 0:
                    # for easier management
                        Kanji(character = kanji.literal, tags = jlpt, next_quiz = now, leitner_grade = Leitner.grades.None.index, active = True, 
                        current_session = False, been_in_session = 0)
                    
                try: 
                    session.commit()
                except IntegrityError:
                    #print 'Already in db'
                    session.rollback()      #is it ok?
        except ValueError:
            print 'oops'    #TODO: add logger
            
    def countTotalItemsInDb(self):
        return { 'kanji' : Kanji.query.count(), 'words': Word.query.count() }
    
    def countItemsByGrades(self):
        results = {}
        i = 1
        jlpt = u'jlpt'
        grade = u'grade'
        
        while True:    
            results[jlpt + str(i)] = session.query(Kanji).filter(Kanji.tags.like(u'%' + jlpt + str(i) + '%' )).count()  
            #results[jlpt + str(i)] = session.query(Kanji).group_by(Kanji.tags.like(u'%' + jlpt + str(i) + '%' )).count()
            #results[jlpt + str(i)] = len(Kanji.query.filter(Kanji.tags.like(u'%' + jlpt + str(i) + '%' )).all())
            
            #results[jlpt + str(i)] = Kanji.query.count_by(Kanji.tags.like(u'%' + jlpt + str(i) + '%' ))
            #results[jlpt + str(i)] = Kanji.query.count(tags=u'%' + jlpt + str(i) + '%' )
            if i > 3 : break
            else: i = i + 1
        i = 1    
        while True:
            results[grade + str(i)] = session.query(Kanji).filter(Kanji.tags.like(u'%' + grade + str(i) + '%' )).count()
            #results[grade + str(i)] = session.query(Kanji).group_by(Kanji.tags.like(u'%' + grade + str(i) + '%' )).count()
            #results[grade + str(i)] = len(Kanji.query.filter(Kanji.tags.like(u'%' + grade + str(i) + '%' )).all())
            
            #results[grade + str(i)] = Kanji.query.count(tags=u'%' + grade + str(i) + '%' )
            #results[grade + str(i)] = Kanji.query.count_by(Kanji.tags.like(u'%' + grade + str(i) + '%' ))
            if i > 9 : break
            else: i = i + 1
            #Kanji.query.count
            
        return results
            
class DictionaryLookup:
       
    def __init__(self):
        self.db = SqlSoup(SQLITE + PATH_TO_RES + JMDICT)
        
    def looseLookupByReading(self, item):
        return self.lookupItemByReading(item + u'%')
    
    def lookupItemByReading(self, item):
        #add interconvert: search both hiragana and katakana variants
        lookup = self.db.r_ele.filter(self.db.r_ele.value==item).all()
        
        results = []
        if len(lookup) > 0:
            for item in lookup:
                words = self.db.k_ele.filter(self.db.k_ele.fk==item.fk).all()
                if len(words) > 0:
                    for word in words:
                        results.append(word.value)
                        
        return results
    
    #TODO: add universal method to get readings, translations altogether 
    
    def lookupReadingsByItem(self, item):
        lookup = self.db.k_ele.filter(self.db.k_ele.value==item).all()
        
        results = []
        if len(lookup) > 0:
            for item in lookup:
                readings = self.db.r_ele.filter(self.db.r_ele.fk==item.fk).all()
                if len(readings) > 0:
                    for reading in readings:
                        results.append(reading.value)
        #NB: perfomance, strangely, unaffected!
        else: 
            lookup = self.db.k_ele.filter(self.db.k_ele.value==hira2kata(item)).all()
            if len(lookup) > 0:
                for item in lookup:
                    readings = self.db.r_ele.filter(self.db.r_ele.fk==item.fk).all()
                    if len(readings) > 0:
                        for reading in readings:
                            results.append(reading.value)

        
        return removeDuplicates(results)

    #TODO: add implementation searching both words and readings
    def lookupItemTranslationJoin(self, item, lang='eng'):
        '''Much faster than without join'''
        join_sense = self.db.join(self.db.k_ele, self.db.sense, self.db.k_ele.fk==self.db.sense.fk, isouter=True)
        join_sense_labels = self.db.with_labels(join_sense)
        join_gloss = self.db.join(join_sense_labels, self.db.gloss, join_sense_labels.sense_id==self.db.gloss.fk)
        
        lookup = join_gloss.filter_by(k_ele_value=item).all()
        result = []
        if len(lookup) > 0:
            for item in lookup:
                if item.lang == lang: result.append(item.value)
                
        return removeDuplicates(result)
    
    def lookupTranslationByReadingJoin(self, item, lang='eng'):
        '''Much faster than without join'''
        join_sense = self.db.join(self.db.r_ele, self.db.sense, self.db.r_ele.fk==self.db.sense.fk, isouter=True)
        join_sense_labels = self.db.with_labels(join_sense)
        join_gloss = self.db.join(join_sense_labels, self.db.gloss, join_sense_labels.sense_id==self.db.gloss.fk)
        
        lookup = join_gloss.filter_by(r_ele_value=item).all()
        result = []
        if len(lookup) > 0:
            for item in lookup:
                if item.lang == lang: result.append(item.value)
                
        return removeDuplicates(result)
    
    def lookupItemByReadingJoin(self, item):
        '''Sometimes, a wee bit faster than without join'''
        join = self.db.join(self.db.k_ele, self.db.r_ele, self.db.k_ele.fk==self.db.r_ele.fk, isouter=True)
        lookup = self.db.with_labels(join).filter_by(r_ele_value=item).all()
        
        result = []
        if len(lookup) > 0:
            for item in lookup:
                result.append(item.k_ele_value)
            
        return removeDuplicates(result)
    
    '''
    def lookupItemTranslation(self, item, lang='eng'):
        lookup = self.db.k_ele.filter(self.db.k_ele.value==item).all()
        
        results = []
        if len(lookup) > 0:
            for item in lookup:
                senses = self.db.sense.filter(self.db.sense.fk==item.fk).all()
                if len(senses) > 0:
                    for sense in senses:
                        translations = self.db.gloss.filter(and_(self.db.gloss.fk==sense.id, self.db.gloss.lang==lang)).all()
                        if len(translations) > 0:
                            for trans in translations:
                                results.append(trans.value)
        return self.removeDuplicates(results)
    '''

#dlookup = DictionaryLookup()
'''
db = DBoMagic()
db.setupDB()
#db.initializeCurrentSession('kanji', 300)
count = db.countTotalItemsInDb()
'''
'''
res = dlookup.lookupItemByReading(u'かれ')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'漢字')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'かんじ')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'おん')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'くれぐれも')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'みられる')
print ' '.join(res)
res = dlookup.lookupItemByReading(u'あそんだ')
print ' '.join(res)
'''

#start = datetime.now()
#res = dlookup.lookupItemTranslationJoin(u'彼')
#res = dlookup.lookupItemByReading(u'かんじ')
#print datetime.now() - start
#print ' '.join(res)

'''
start = datetime.now()
res = dlookup.lookupItemTranslation(u'彼')
print ' '.join(res)
print datetime.now() - start
'''
'''
start = datetime.now()
res = dlookup.lookupItemByReading(u'し')
print datetime.now() - start
print ' '.join(res)

start = datetime.now()
res = dlookup.lookupItemByReadingJoin(u'し')
print datetime.now() - start
print ' '.join(res)
#print ' '.join(res)
'''

'''
start = datetime.now()
res = dlookup.lookupReadingsByItem(u'空')
print datetime.now() - start
print ' '.join(res)
res = dlookup.lookupReadingsByItem(u'繋がる')
print ' '.join(res)
'''

'''
#start = datetime.now()
#res = dlookup.lookupItemTranslation(u'手')
#res = dlookup.lookupItemTranslation(u'軈て')
#res = dlookup.lookupItemTranslation(u'顔')
print ' '.join(res)
print datetime.now() - start
'''
print 'ok'