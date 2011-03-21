# -*- coding: utf-8 -*-
'''
Created on Mar 19, 2011

@author: Yadavito
@version: 0.0.1
@requires: Python 2.6.6
@requires: PySide 1.0.0
'''

# -> this is main application module <- #
#===============================================================================
# --- suzu_ei ---
# english/russian fork
# -> main project file <-
# -> contains: 
#   - central GUI dialog
#   - TODO list
#   - dependencies & packages
#   - notes and iformation
# -> structure:
#   - gui ~ Qt frontend
#   - settings ~ options backend, constants
#   - srs ~ spaced repetition scheduler, db interface
#   - utilities ~ useful utilites
#   - jtools ~ jisho examples downloader
#   - jdict ~ db aggregator
#   - mParser ~ interface to mecab parser 
# -> dependencies setup:
#   - python install.py
# -> launch:
#   - python suzu.py
#===============================================================================

####################################
#            Dependencies          #
####################################

# PySide 1.0.0
# SQLAlchemy 0.6.6
# Elixir
# UserConfig
# nltk
# pymorphy
# openpyxl                            http://goo.gl/NvAD7

####################################
#            Resources             #
####################################

# NLTK
# Tatoeba examples                    http://goo.gl/QFEe2
# Muller dictionary
# SUBTLEXus                           http://goo.gl/5WiTP

####################################
#        Aptana built-ins:         #
####################################

# PySide
# elixir
# enum
# openpyxl
# pymorphy

####################################
#    here goes global TODO list    #
####################################

# urgent
# ...

# concept
# ...

# functionality
# ...

# utilitarian
# ...

####################################
#            Imports               #
####################################

# internal packages #
import sys

# external packages #
from PySide.QtGui import QApplication, QIcon

# own packages #
from gui.guiMain import Quiz
from gui.about import About
from gui.guiOpt import OptionsDialog
from gui.guiQuick import QuickDictionary
from utilities.log import log
#from utilities.utils import BackgroundDownloader
#from edict.db import redict      # for redict, elusive import

from etools.tatoeba import TatoebaLookup
from etools.frequency import FrequencyLookup

####################################
#        QT application loop       #
####################################    

if __name__ == '__main__':
    
    #from srs.srsManager import srsScheduler
    
#    srs = srsScheduler()
#    srs.initializeAll()
#    srs.db.addItemsToDb(18000, 29000)
#    srs.initializeCurrentSession(100)
#    srs.getNextItem()
#    item = srs.getCurrentItem()
#    example = srs.getCurrentExample()
#    translation = srs.getCurrentSentenceTranslation()
#    pass

    app = QApplication(sys.argv)
    
    quiz = Quiz()
    if quiz.options.isPlastique():  app.setStyle('plastique')
    quiz.setWindowIcon(QIcon('../res/icons/suzu.png'))
    
    about = About()
    options = OptionsDialog(quiz.srs.db, quiz.srs.db.frequency, quiz.options)
    #qdict = QuickDictionary(quiz.jmdict, quiz.edict, quiz.kjd, quiz.srs.db, quiz.options)
        
    #updater = BackgroundDownloader(quiz.options.getRepetitionInterval())
    #updater.start()
    qdict = (); updater = ()
    
    quiz.addReferences(about, options, qdict, updater)
    quiz.initGlobalHotkeys() 
    
    try:
        sys.exit(app.exec_())
    except Exception, e:
        log.debug(e)
                    
#    test = TatoebaLookup()
#    #test.parseTatoebaExamples()
#    test.loadExamplesFromPickled()
#    results = test.lookupExactWorld('to')
#    pass

#===============================================================================
#    from datetime import datetime
# 
#    start = datetime.now()
#    
#    test = FrequencyLookup()
#    test.parseXLSXSource()
#    
#    print datetime.now() - start
#===============================================================================
    
#    test.loadFrequencyDict()
#    
#    start = datetime.now()
#    print test.getFrequencyRangeLimits()
#    print datetime.now() - start

    print 'ok'