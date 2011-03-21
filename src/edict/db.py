# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2011

@author: Yadavito
'''

# internal #
from datetime import datetime
from itertools import permutations, repeat
from random import shuffle, sample, randrange
import os.path, pickle, re
# own #
from settings.constants import *
from srs.leitner import Leitner
from etools.frequency import FrequencyLookup

# external #
from elixir import Entity, Field, Unicode, Integer, TIMESTAMP, ManyToMany, \
    metadata, session, create_all, setup_all, BOOLEAN#, cleanup_all
from sqlalchemy import asc, and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.sqlsoup import SqlSoup
#from sqlalchemy.orm.exc import NoResultFound
from jcconv import hira2kata

def removeDuplicates(list):
    set = {}
    return [set.setdefault(e,e) for e in list if e not in set]

class Session(Entity):
    date = Field(TIMESTAMP)
    items = Field(Integer)
    time = Field(Integer)

class Item(Entity):
    item = Field(Unicode(16))
    
    # srs params for words mode
    next_quiz = Field(TIMESTAMP)
    leitner_grade = Field(Integer)
    
    # session params
    active = Field(BOOLEAN)
    current_session = Field(BOOLEAN)
    been_in_session = Field(Integer) 
    # additional
    wrong_in_current_session = Field(Integer)
    
    # relations
#    kanji = ManyToMany('Kanji')
#    example = ManyToMany('Example') #is it correct?

#class Example(Entity):
#    sentence = Field(Unicode(256))
#    translation = Field(Unicode(256))
#    
#    # relations
#    kanji = ManyToMany('Kanji')
#    word = ManyToMany('Word') #is it correct?
    
#class DBBackgroundUpdater:
#    def __init__(self):
#        self.metadata = metadata
#        self.metadata.bind = SQLITE + PATH_TO_RES + DBNAME
#        setup_all()
#        
#    def addExamples(self, item, examples):
#        '''Item is either kanji or word'''
#        
#        if item is not None:
#            for example in examples:
#                item.example.append(Example(sentence = example,translation = examples[example]))
#            session.commit()
#    
#    def getSomeItem(self):
##        kanji = Kanji.query.filter_by(current_session = True).order_by(asc(Kanji.next_quiz)).first()
##        if len(kanji.example) == 0:
##            return kanji
#
#        items = Kanji.query.filter_by(current_session = True).order_by(asc(Kanji.next_quiz)).all()
#        for kanji in items:
#            if len(kanji.example) == 0:
#                return kanji
        
class DBoMagic:
    
    def __init__(self):
        self.metadata = metadata
        self.metadata.bind = SQLITE + PATH_TO_RES + DBNAME      
        self.frequency = FrequencyLookup()
        self.count = 0
        
    def setupDB(self):  
        """Initialize/read database on disk"""
#        self.db = SqlSoup(SQLITE + PATH_TO_RES + KANJIDIC2) 
        setup_all()
        if not os.path.exists(PATH_TO_RES + DBNAME):
            create_all()
             
        session.bind = metadata.bind
        #self.frequency.loadFrequencyDict()
    
    def getNextQuizItem(self):
        #TODO: implement with great verve and so on!
        #TODO: check if item.next_quiz is the same for multiple items
        #...
        return  Item.query.filter_by(current_session = True).order_by(asc(Item.next_quiz)).first()
        
    def initializeCurrentSession(self, sessionSize):
        
        selection = Item.query.filter_by(active = True).all()
            
        self.endCurrentSesion()
        n = sessionSize
        
        shuffle(selection)
        if n > len(selection) : n = len(selection)
        random_selection = sample(selection, n)

        for item in random_selection:
            # mark n random items as 'current' 
            item.current_session = True
            item.been_in_session = item.been_in_session + 1     #may be useful later on
            
        session.commit()

    def endCurrentSesion(self):
        for item in Item.query.all():
            item.current_session = False
        
        session.commit()

    def updateQuizItem(self, item):
        session.commit()
    
    def addItemToDb(self, item):
        if(len(Item.query.filter_by(item = item).all()) == 0):
            Item(item = item, tags = u'user', next_quiz = datetime.now(), leitner_grade = Leitner.grades.None.index, active = True, 
                                current_session = False, been_in_session = 0)
            session.commit()
            
    def addWordToDbByValue(self, item):
        if len(item) > 1:
            if(len(Item.query.filter_by(item = item).all()) == 0):
                Item(item = item, tags = u'user', next_quiz = datetime.now(), leitner_grade = Leitner.grades.None.index, active = True, 
                                    current_session = False, been_in_session = 0)
                session.commit()
        
#    def addSentenceToDb(self, kanji, sentence, translation):
#        Kanji.query.filter_by(character = kanji).one().example.append(Example(sentence = sentence,translation = translation))          #or get_by
#        #k.example.append(Example(sentence = sentence,translation = translation)) 
#        session.commit()
        
#    def addExamplesForKanji(self, kanji, examples):
#        for example in examples:
#            kanji.example.append(Example(sentence = example,translation = examples[example]))
#        session.commit()
            
#    def getExample(self, item):
#        examples = item.example
#        return examples[randrange(0, len(examples))]
        
#    def checkIfKanjiHasExamples(self, kanji):
#        if len(kanji.example) > 0:
#            return True
#        else:
#            return False
        
#    def findSimilarReading(self, kana):
#        """Generate quiz variants based on correct reading ('kana' argument)"""
#        
#        size = len(kana) - 1
#        readings = []
#        selection = []
#        count = 0
#        
#        if len(kana) > 1:
#            while True:
#                selection = self.db.kunyomi_lookup.filter(self.db.kunyomi_lookup.reading.like(kana[0] + u'_' * size)).all()
#            
#                if len(selection) >= 4:
#                    rand = sample(selection, 4)
#                    for read in rand:
#                        readings.append(read.reading)
#                        
#                else:
#                    perm = list(map(''.join, permutations(kana)))
#                    if len(perm) >= 4:
#                        readings = sample(perm, 4)
#                    else:
#                        i = 0; variant = u''
#                        while i < 4:
#                            j = 0
#                            while j < size:
#                                variant += KANA_TABLE[randrange(0, len(KANA_TABLE))];    j = j + 1
#                            readings.append(variant);   variant = u'';  i = i + 1
#                    
#                readings = removeDuplicates(readings)   
#                count = count + 1
#                
#                if len(readings) >= 4: break
#                if count > 3: break
#                
#        elif len(kana) == 1:
#            i = 0
#            while True:
#                for _ in repeat(None, 4):
#                    readings.append(KANA_TABLE[randrange(0, len(KANA_TABLE))]) 
#                readings = removeDuplicates(readings)   
#                if len(readings) >= 4: break
#                elif i < 4: i = i + 1
#                else: break
#                
#        #inserting correct reading at random position (if not already)
#        print ' '.join(readings) #THIS IS FOR TEST ONLY     
#        if kana not in readings[:4]:
#            if len(readings) >= 4:
#                readings[randrange(0, 4)] = kana
#            else:
#                readings[randrange(0, len(readings))] = kana
#        print ' '.join(readings) #THIS IS FOR TEST ONLY     
#
#        return readings
    
    def addItemsToDb(self, min, max, exact=False, tag='user'):
        self.count = 0
        success = False
        
        items = self.frequency.getFrequencyRange(min, max, exact)
        
        now = datetime.now()
        for item in items:
            if session.query(Item).filter_by(item = item).count()  == 0:
                Item(item = item, tags = tag, next_quiz = now, leitner_grade = Leitner.grades.None.index, active = True, 
                current_session = False, been_in_session = 0)
                
                self.count = self.count + 1
                success = True
                try: 
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    success = False
        return success
    
    def countTotalItemsInDb(self):
        return { 'items' : Item.query.count() }
    
#    def countItemsByGrades(self):
#        results = {}
#        i = 1
#        jlpt = u'jlpt'
#        grade = u'grade'
#        
#        while True:    
#            results[jlpt + str(i)] = session.query(Kanji).filter(Kanji.tags.like(u'%' + jlpt + str(i) + '%' )).count()  
#            if i > 3 : break
#            else: i = i + 1
#        i = 1    
#        while True:
#            results[grade + str(i)] = session.query(Kanji).filter(Kanji.tags.like(u'%' + grade + str(i) + '%' )).count()
#            if i > 9 : break
#            else: i = i + 1
#            
#        return results
    
    def updateActive(self, criteria, flag):
        lookup = Item.query.filter(Item.tags.like(u'%' + criteria + '%' )).all()
        for item in lookup:
            item.active = flag
            
        session.commit()
        
    def checkIfActive(self, criteria):
        kanji = session.query(Item).filter(Item.tags.like(u'%' + criteria + '%' )).first()
        if kanji is not None:
            return kanji.active
        
    def getAllItemsInFull(self):
        return Item.query.all()
        
    def clearDB(self):
        Item.query.delete()
        session.commit()
        session.execute('VACUUM')
            
class DictionaryLookup:
    
    #FIXME: REFACTOR, REFACTOR, friggin' REFACTOR all this mess!
    def __init__(self):
        self.db = SqlSoup(SQLITE + PATH_TO_RES + JMDICT)
        #self.joinTables()   #TODO: should move somewhere (may be pre-dump routine?)
        self.dictionary = {}
        self.loadJmdictFromDumpRegex()	#TODO: add check
        
    def joinTables(self):
        '''Join tables on init for better perfomance'''
        join_word = self.db.join(self.db.k_ele, self.db.r_ele, self.db.k_ele.fk==self.db.r_ele.fk, isouter=True)
        join_sense = self.db.join(join_word, self.db.sense, join_word.fk==self.db.sense.fk )
        join_sense_labels = self.db.with_labels(join_sense)
        
        self.join_gloss = self.db.join(join_sense_labels, self.db.gloss, join_sense_labels.sense_id==self.db.gloss.fk)
    
    def dumpJmdictToFileMulilang(self, languages):
        '''VERY time (and memory) consuming'''
                
        dictionary = {}
        everything = self.join_gloss.all()
        print len(everything)
        for item in everything:
#            if item.lang == 'eng':
#                if dictionary.has_key(item.r_ele_value):
#                    dictionary[item.r_ele_value].append({'word' : item.k_ele_value, 'sense' : item.value})
#                else:
#                    dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'sense' : item.value}]    #what about r_ele_nokanji?
#            if item.lang == 'eng' or item.lang == 'rus':    #(*)
            if item.lang in languages:
                if dictionary.has_key(item.r_ele_value):
                    if dictionary[item.r_ele_value].has_key(item.k_ele_value):
                        if dictionary[item.r_ele_value][item.k_ele_value].has_key(item.lang):
                            dictionary[item.r_ele_value][item.k_ele_value][item.lang].append(item.value)
                        else:
                            dictionary[item.r_ele_value][item.k_ele_value][item.lang] = [item.value]
                    else:
                            dictionary[item.r_ele_value][item.k_ele_value] = { item.lang : [item.value] } 

    #                if item.lang == 'eng':
    #                    dictionary[item.r_ele_value]['sense']['eng'].append(item.value)
    #                if item.lang == 'rus':
    #                    dictionary[item.r_ele_value]['sense']['rus'].append(item.value)
                    
#                    dictionary[item.r_ele_value][item.lang].append(item.value)         #without (*) check - will copy everythig
#                    dictionary[item.r_ele_value]['word'] = item.k_ele_value

                else:
                    #dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, item.lang : [item.value] }] 
                    dictionary[item.r_ele_value] = { item.k_ele_value : { item.lang : [item.value] } }

            #===================================================================
            # if item.lang == 'eng':
            #    if dictionary.has_key(item.r_ele_value):
            #        dictionary[item.r_ele_value]['word'] = item.k_ele_value
            #        dictionary[item.r_ele_value]['sense']['eng'].append(item.value)
            #    else:
            #        dictionary[item.r_ele_value] = [{ 'word' : item.k_ele_value, 'eng' : [item.value] }] 
            # elif item.lang == 'rus':
            #    if dictionary.has_key(item.r_ele_value):
            #        dictionary[item.r_ele_value]['word'] = item.k_ele_value
            #        dictionary[item.r_ele_value]['sense']['rus'].append(item.value)
            #    else:
            #        dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'rus' : [item.value] }] 
            #===================================================================

            #NB:[{ 'word' : ..., 'sense' : { 'rus' : [], 'eng' : [] } ]
            #or
            #NB: [{ 'word' : ..., 'rus' : [], 'eng' : [] } <--- the best?
            #or (even better)
            #additionally, check if 'word' is the same ~ append to rus/eng/... senses, not to item by key;
            #then, not dict[key] = [{ ... }] but dict[key] = { ... [], [] }
            #(probably won't work, reading : word is not 1:1)
                    
#            if item.lang == 'eng':
#                if dictionary.has_key(item.r_ele_value):
#                    dictionary[item.r_ele_value]['word'] = item.k_ele_value
#                    dictionary[item.r_ele_value]['sense']['eng'] = item.value
#                else:
#                    dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'sense' : {'eng' : item.value}}] 
#            elif item.lang == 'rus':
#                if dictionary.has_key(item.r_ele_value):
#                    dictionary[item.r_ele_value]['word'] = item.k_ele_value
#                    dictionary[item.r_ele_value]['sense']['rus'] = item.value
#                else:
#                    dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'sense' : {'rus' : item.value}}] 
            
        dump = open(PATH_TO_RES + JMDICT_DUMP, 'w')
        pickle.dump(dictionary, dump)
        
        del dictionary
        del everything
        dump.close()
    
    def dumpJmdictToFile(self, lang='eng'):
        
        dictionary = {}
        everything = self.join_gloss.all()
        print len(everything)
        for item in everything:
            if item.lang == lang:
                #NB:[ { 'word' : .., 'sense' : [..] } ] ~ dictionary composed of list of dictionaries
                #===============================================================
                # if dictionary.has_key(item.r_ele_value):
                #    dictionary[item.r_ele_value].append({'word' : item.k_ele_value, 'sense' : item.value})
                # else:
                #    dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'sense' : item.value}]
                #===============================================================
                
                #NB: { word : [ senses ] } ~ dictionary of dictionaries
                if dictionary.has_key(item.r_ele_value):
                    if dictionary[item.r_ele_value].has_key(item.k_ele_value):
                        dictionary[item.r_ele_value][item.k_ele_value].append(item.value)
                    else:
                        dictionary[item.r_ele_value][item.k_ele_value] = [item.value]
                else:
                    dictionary[item.r_ele_value] = { item.k_ele_value : [item.value]  }
                    
        dump = open(PATH_TO_RES + JMDICT_DUMP, 'w')
        pickle.dump(dictionary, dump)
        
        del dictionary
        del everything
        dump.close()
        
    def dumpJmdictToFileWithRegex(self, lang='eng'):
        '''VERY time consuming'''
                
        dictionary = redict({})     #NB: regex dictionary, [] is an generator object (iterator)
        everything = self.join_gloss.all()
        print len(everything)
        for item in everything:
            #NB:[ { 'word' : .., 'sense' : [..] } ] ~ dictionary composed of list of dictionaries
            #===================================================================
            #    if dictionary.has_key(item.r_ele_value):
            #        dictionary.get(item.r_ele_value).append({'word' : item.k_ele_value, 'sense' : item.value})
            #    else:
            #        dictionary[item.r_ele_value] = [{'word' : item.k_ele_value, 'sense' : item.value}]
            #===================================================================
            
            #NB: { word : [ senses ] } ~ dictionary of dictionaries
            if item.lang == lang:
                if dictionary.has_key(item.r_ele_value):
                    if dictionary.get(item.r_ele_value).has_key(item.k_ele_value):
                        dictionary.get(item.r_ele_value).get(item.k_ele_value).append(item.value)
                    else:
                        dictionary.get(item.r_ele_value)[item.k_ele_value] = [item.value]
                else:
                    dictionary[item.r_ele_value] = { item.k_ele_value : [item.value], 'kana' : item.r_ele_value }     
            
        dump = open(PATH_TO_RES + JMDICT_DUMP + '_rx', 'w')
        pickle.dump(dictionary, dump)
        
        del dictionary
        del everything
        dump.close()
        
    def loadJmdictFromDump(self):
        dump = open(PATH_TO_RES + JMDICT_DUMP, 'r')
        self.dictionary = pickle.load(dump)
        dump.close()
           
    def loadJmdictFromDumpRegex(self):
        dump = open(PATH_TO_RES + JMDICT_DUMP + '_rx', 'r')
        self.dictionaryR = pickle.load(dump)
        dump.close()
        