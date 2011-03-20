# -*- coding: utf-8 -*-
'''
Created on Mar 19, 2011

@author: Yadavito
'''

# internal #
import csv, pickle, random, os, urllib

# own #
from settings.constants import PATH_TO_RES, EXAMPLES, LINKS, RESULTING_DICTIONARY,\
                                sentences_url, links_url
from utilities.utils import redict

# external $
#from pymorphy import get_morph

class TatoebaLookup:
    
    def __init__(self):
        self.readyState = self.checkExamples()
        #self.en_morph = get_moprh(PATH_TO_RES + 'dicts/en')
    
    def checkExamples(self):
        return ( os.path.exists(PATH_TO_RES + EXAMPLES) and os.path.exists(PATH_TO_RES + LINKS) )
    
    def downloadTatoebaExamples(self):
        try:
            urllib.urlretrieve(sentences_url,  sentences_url.split('/')[-1])
            urllib.urlretrieve(links_url,  links_url.split('/')[-1])
            return True
        except:
            return False
    
    def clearOriginalCsv(self):
        os.remove(PATH_TO_RES + EXAMPLES)
        os.remove(PATH_TO_RES + LINKS)
    
    def parseTatoebaExamples(self):
        csv_examples = csv.reader(open(PATH_TO_RES + EXAMPLES), delimiter='\t')
        csv_links = csv.reader(open(PATH_TO_RES + LINKS), delimiter='\t')
        
        links = {}
        for link in csv_links:
            if links.has_key(link[0]):
                links[link[0]].append(link[1])
            else:
                links[link[0]] = [ link[1] ]
        
        examples = {}
        for example in csv_examples:
            if example[1] == 'eng' or example[1] == 'rus':
                try:
                    translation_ids = links[example[0]]
                    examples[example[0]] = {'lang' : example[1], 'sentence' : example[2], 'translation' : translation_ids }
                except:
                    pass
                
        examples_dictionary = redict({})
        for item in examples:
            if examples[item]['lang'] == 'eng':
                for id in examples[item]['translation']:
                    try:
                        if examples[id]['lang'] == 'rus':
                            examples_dictionary[examples[item]['sentence']] = { 'eng' : examples[item]['sentence'], 'rus' : examples[id]['sentence'] }
                    except:
                        pass
        del links
        del examples
        
        dump = open(PATH_TO_RES + RESULTING_DICTIONARY, 'w')
        pickle.dump(examples_dictionary, dump)
        
        del examples_dictionary
        dump.close()
                
        print 'well, well, well'
        
    def loadExamplesFromPickled(self):
        dump = open(PATH_TO_RES + RESULTING_DICTIONARY, 'r')
        self.dictionary = pickle.load(dump)
        dump.close()
        
    def lookupExactWorld(self, word):
        results = []
        
        for item in self.dictionary[word]:
            results.append(item)
            
        if len(results) == 0:
            
            pass
        #TODO: add search for inflected forms
            
        return results
    
    def getRandomExample(self, word):
        examples = self.lookupExactWorld(word)
        if len(examples) > 0:  return examples[random.randrange(0, len(examples))]
        
    def updateExamples(self):
        pass