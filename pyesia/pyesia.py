# -*- coding: utf-8 -*-
"""
pyesia
A toolbox for spanish poetry analysis
@author: Guillermo Serrano Nájera
"""
class poemAnalysis:
    
    def __init__(self, poem_path):
        self.poem_path = poem_path
        [self.poem, self.metric_syllables, self.phonologic_syllables, self.verse_classification,\
             self.accents, self.synalephas, self.synalephas_hyatus]=perform_analysis(poem_path)
