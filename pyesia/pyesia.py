# -*- coding: utf-8 -*-
"""
pyesia
A toolbox for spanish poetry analysis
@author: Guillermo Serrano Nájera
"""
from spanish_poetry_functions import *

class poemAnalysis:
    
    def __init__(self, poem_path):
        self.poem_path = poem_path
        
        [self.poem, self.metric_syllables, self.phonologic_syllables, self.verse_classification,\
             self.accents, self.synalephas, self.synalephas_hyatus]=perform_analysis(poem_path)
        
        self.con_rhymes, self.aso_rhymes, self.rhyme_dict = rhyme_scheme(self.poem)
        self.correct_syllables, self.correct_accents = syllable_correction(self)
        
        self.compass, self.mean_compass = compass_analysis(self)
    
    def plot_analyisis(self):
        plotPoemAnalysis(self)
        plot_compass(self)
        
        
#p = poemAnalysis("Sombras_De_Los_Dias_De_Venir.txt")
#p = poemAnalysis("XXIX_Antonio_Machado.txt")
#p = poemAnalysis("Tus_Ojos_Octavio_Paz.txt")
p = poemAnalysis("caiman.txt")
p.plot_analyisis