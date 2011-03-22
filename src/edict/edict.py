# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2011

@author: Yadavito
'''

# internal #
#from collections import defaultdict
import codecs, pickle

# own #
from settings.constants import PATH_TO_RES, DICT, RESULTING_DICT
from utilities.utils import redict

# external #
#from  sdictviewer import dictutil
#from sdictviewer import detect_format

class EdictParser:
    def __init__(self):
        self.dictionary = redict({})
    
    def dumpDictToPickle(self):
        #file = open(PATH_TO_RES + DICT + 'mueller4.txt')
        #file = open('../' + PATH_TO_RES + DICT + 'mueller4.txt', 'r', 'windows-1251')    #test
        #file = codecs.open('../' + PATH_TO_RES + DICT + 'mueller4.txt', 'r', 'windows-1251')    #test
        file = codecs.open(PATH_TO_RES + DICT + 'mueller4.txt', 'r', 'windows-1251')    #test
        
        results_dict = redict({})
        for line in file.readlines():
            if not line.startswith('_'):
                word, trans = line.strip().split('  ')
                #trans = unicode.encode(trans, 'utf-8')
                trans = unicode(trans)
                
                results_dict[word] = { 'rus' : trans.replace(trans[trans.find('['): trans.find(']') + 1], ''), 'eng' : word }
                
        file.close()
        
#        dump = open('../' + PATH_TO_RES + RESULTING_DICT, 'w')
        dump = open(PATH_TO_RES + RESULTING_DICT, 'w')
        pickle.dump(results_dict, dump)
        
        del results_dict
        dump.close()
        
    def loadDict(self):
#        dump = open('../' + PATH_TO_RES + RESULTING_DICT, 'r')
        dump = open(PATH_TO_RES + RESULTING_DICT, 'r')
        self.dictionary = pickle.load(dump)
        dump.close()
        
    def lookupExactWord(self, word):
        results = []
        
        #TODO: normalize before search
        for item in self.dictionary[word]:
            results.append(item)
            
        if len(results) == 0:
            pass
            
        return results
            
#test = EdictParser()
#test.dumpDictToPickle()
#test.loadDict()
#res = test.lookupExactWord('word')
#print ''

#class WordLookupByWord(dict):
#    def __missing__(self, word):
#        value = dictutil.WordLookup(word)
#        return value
#
#class EdictParser:
#    def __init__(self):
#        self.dictionaries = dictutil.DictionaryCollection()
#    
#    def loadDict(self, file):
#        fmt = detect_format(file)
#        if fmt:
#            dict = fmt.open(file)
#            #gobject.idle_add(self.update_status_display, dict.title)
#            dict.load()
#            self.add_dict(dict, fmt)
#        else:
#            raise Exception("Unknown format")
#        
#    def add_dict(self, dict, fmt):
#        if (self.dictionaries.has(dict)):
#            return
#        self.last_dict_file_location = dict.file_name
#        self.dictionaries.add(dict)
##        self.dict_formats[dict] = fmt
##            if not self.article_formatters.has_key(fmt):
##                self.article_formatters[fmt] = fmt.create_article_formatter(self, self.word_ref_clicked, self.external_link_callback)
##            gobject.idle_add(self.add_to_menu_remove, dict)
##            gobject.idle_add(self.update_title)
#
#    def lookupWord(self, word):
#        #interrupted = False
#        lang_word_list = {}
#        skipped = defaultdict(list)
#        for lang in self.dictionaries.langs():
#            word_lookups = WordLookupByWord()
#            for item in self.dictionaries.get_word_list_iter(lang, word):
##                time.sleep(0)
##                if self.lookup_stop_requested:
##                    interrupted = True
##                    return (lang_word_list, interrupted)
#                if isinstance(item, dictutil.WordLookup):
#                    word_lookups[item.word].add_articles(item)
#                else:
#                    skipped[item.dict].append(item)
#            word_list = word_lookups.values()
#            #word_list.sort(key=self.sort_key)
#            if len (word_list) > 0: lang_word_list[lang] = word_list
##            for dict, skipped_words in skipped.iteritems():
##                for stats in dict.index(skipped_words):
##                    time.sleep(0)
##                    if self.lookup_stop_requested:
##                        interrupted = True
##                        return (lang_word_list, interrupted)
#        return lang_word_list
#        #return dictutil.WordLookup(word)
#
#test = EdictParser()
##test.loadDict('../' + PATH_TO_RES + 'sdict/' + 'mueller24.dct')
#test.loadDict('../' + PATH_TO_RES + 'sdict/' + 'eng_rus_short2.dct')
#res = test.lookupWord(u'word')
#print 'ok'