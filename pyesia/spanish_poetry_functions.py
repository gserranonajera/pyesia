# -*- coding: utf-8 -*-
"""
spanish_poetry_functions.py
@author: Guillermo Serrano Nájera
"""
import re, string

def perform_analysis(poem_path):
    
    poem = []
    with open(poem_path, "r") as f:
        lines = f.readlines()
        poem = [l.strip() for l in lines if l.strip()]
                
    metric_syllables = list()
    phonologic_syllables = list()
    verse_classification = list()
    accents = list()
    synalephas = list()
    synalephas_hyatus = list()
    
        
    #analyse each individual verse
    for verse in poem:
        
        verse = clean_punctuation(verse)
        words_verse = verse.split()
        
        verse_accents = []
        syllable_number = 0
        verse_type = 0
        verse_synalephas = []
        verse_synalephas_hyatus = []
        total_words = len(words_verse)
        
        prev_syllables = []
        prev_tonic = []
        
        word_idx = 0
        
        for word in words_verse:

            current_syllables = syllables(word)
            current_tonic = tonic_syllable(current_syllables)
            length = len(current_syllables)
            syllable_number += length
            accentuated_word = not_clitic_word(word)
            
            if accentuated_word:
                verse_accents.append(syllable_number + current_tonic)
            else:
                current_tonic = 0
            
            [synalepha, synalepha_hyatus] = detect_synalephas(prev_syllables,\
                current_syllables, prev_tonic, current_tonic)
        
            if synalepha:
                if synalepha_hyatus:
                    verse_synalephas.append(syllable_number-length)
                    verse_synalephas_hyatus.append(syllable_number-length)
            
            prev_syllables = current_syllables
            prev_tonic = current_tonic
            
            if word_idx == total_words-1: # if it is the last word in the verse
                if current_tonic == -1: # aguda
                    verse_type = 1
                elif current_tonic < -2: # esdrújula o sbreesdrújula
                    verse_type = -1
                else: # llana
                    verse_type = 0
                                        
            [verse_metric_syllables, verse_accents] = correction_by_synalephas(syllable_number,\
                verse_accents, verse_synalephas)
            
            verse_metric_syllables += verse_type
            
        metric_syllables.append(verse_metric_syllables)
        phonologic_syllables.append(syllable_number)
        verse_classification.append(verse_type)
        accents.append(verse_accents)
        synalephas.append(verse_synalephas)
        synalephas_hyatus.append(verse_synalephas_hyatus)
        
    return [poem, metric_syllables, phonologic_syllables, verse_classification, accents, synalephas, synalephas_hyatus]
    
def clean_punctuation(text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

def syllables(word):  
    '''
    Returns a list with the syllables of word
    To do it, it finds all possible syllable begginings in spanish
    
    Devuelve una lista con las sílabas de la palabra (variable word)
    Para hacerlo encuentra los comienzos de silaba posibles en castellano
    '''
    creed = re.compile(u'''((b|br|bl|c|ch|cr|cl|d|dr|f|fr|fl|gu|g|
                 gr|gl|gü|h|j|k|kr|kl|l|ll|m|mn|n|ñ|p|ph|
                 pr|pl|ps|qu|q|rr|r|s|t|tr|tl|v|vr|vl|w|x|y|z))?          
                 (ih?u(?![aeoáéíóú])|                               
                  uh?i(?![aeoáéíóú])|                               
                  uy(?![aeiouáéíóú])|                               
                  [iuü]?[aeoáéíóú](h?[iuy](?![aeoiuáéíóú]))?|      
                  [ui]|                                             
                  y(?![aeiouáéíóú]))''', 
                 re.UNICODE | re.IGNORECASE | re.VERBOSE)

    pos = []
    for m in creed.finditer(word):
        pos.append(m.start())
    
    pos.append(len(word))
    
    syllables_word = [word[pos[x]:pos[x+1]] for x in range(len(pos)-1)]
    
    return syllables_word

def tonic_syllable(syllables_word):
    '''
    Takes a list with the syllables of a word, like the ones returned by
    syllables function and returns the postition of the tonic syllables, using:
    aguda = -1; llana = -2; esdrújula = -3; sobresdrújula < -3
    
    Toma una lista de silabas de una sola palabra, como las que devuelve
    la función syllables y retorna la posición de la silaba tónica, siendo:
    aguda = -1; llana = -2; esdrújula = -3; sobresdrújula < -3.
    '''
    accents = re.compile(u'[áéíóú]',re.UNICODE | re.IGNORECASE)
    llana_sin_acento = re.compile('[nsaeiou]',re.UNICODE | re.IGNORECASE)
    
    orthographic_accent = False
    syllables_number = len( syllables_word )
    syllabic_range = list( range( -1, -(syllables_number+1), -1 ) )

    # Test if there is ortographic accents
    # Comprueba la presencia de acentos ortográficos
    for syllable_idx in syllabic_range:

        current_syllable = syllables_word[syllable_idx]

        if accents.search( current_syllable ):
            orthographic_accent = True
            break
    
    # If the word has accent, the that is the tonic syllable
    # Si tiene acento, entonces la silaba tónica es la acentuada    
    if orthographic_accent:
        tonic = syllable_idx
    
    # If it has no accent, only can be llano or aguda
    # Si no tiene acento, entonces es llana o aguda   
    else:
        
        # if it has only one syllable, is aguda
        # Si es monosílaba es aguda
        if syllables_number == 1:
            tonic = -1
        
        else:
            last_syllable = syllables_word[len(syllables_word)-1]
            last_letter = last_syllable[len(last_syllable)-1]
       
            # If the last letter is n/s/vowel and no accents, is llana
            # Si la última letra es n/s/vocal y no tiene acento, será llana
            if llana_sin_acento.search(last_letter):
                tonic = -2
            
            # Otherwise is aguda
            # En los demás casos sera aguda
            else:
                tonic = -1              
        
    return tonic

def not_clitic_word(word):
    '''
    This function takes a word and returns a boolean specifying if it is a
    clitic word
    
    Esta función toma una palabra y retorna un booleano definiendo si se trata
    de una palabra inacentuada
    '''
    
    word = word.lower()
    palabras_cliticas = [
    'el','los','la','las','me','nos','te','os','lo','le','les','se','mi',
    'mis','tu','tus','su','sus','nuestro','nuestros','nuestra','nuestras','vuestro',
    'vuestra','vuestros','vuestras','que','quien','quienes','cuyo','cuya','cuyos',
    'cuyas','cual','cuales','como','cuando','do','donde','adonde','cuan','tan',
    'cuanto','cuanta','cuantos','cuantas','a','ante','bajo','cabe','con','contra',
    'de','desde','durante','en','entre','hacia','hasta','mediante','para','por',
    'sin','so','sobre','tras','versus','aunque','conque','cuando','luego','mas',
    'mientras','ni','o','u','pero','porque','pues','que','si','sino','y','e',
    'aun','excepto','hasta','incluso','don','doña','fray','frey','san','sor',
    'santo','santa','santos','santas','al'] #¿Al falta?
            
    accentuated_word = True        
    if word in palabras_cliticas:
        accentuated_word = False
        
    return accentuated_word
    
def coditional_clitic_word( word ):
    '''
    in development
    en desarrollo
    '''
    cliticas_condicionales = []
            
    warning = False        
    if word in cliticas_condicionales:
        warning = True
        
    return warning

def detect_synalephas(prev_syllables, current_syllables, prev_tonic, current_tonic):
    '''
    take a couple of words and return two booleans determining if there is a
    synalepha or a synalepha hiatus between both words
    
    toma una pareja de palabras y devuelve dos booleanos que determina si entre
    ambas palabras se encuentra una sinalfa o una sinalefa-hiato
    '''
    synalepha = False
    synalepha_hyatus = False
    
    #☺ It there is a previous word, look for synalepha
    # Si hay una palabra previa, entonces busca si hay synalepha
    if len(prev_syllables) > 0:
         
         # Determine if previous word finihs in vowel(v) vh
         # Busca si la palabra anterior acaba por vocal(V) o por Vh.
         vowels_final = re.compile('([aeiou]h?$)', re.UNICODE | re.IGNORECASE)
         
         # Determine if the next word starts with h
         # Busca si la palabra siguiente comienza por vocales o por h
         vowels_init = re.compile('h?[aeiou]', re.UNICODE | re.IGNORECASE)
         
         # Determine if the the word starts with "y" not followed by vowels
         # Busca si la palabra comienza por 'y' no seguida por vocales
         y_griega = re.compile( 'y[^aeiou]?$', re.UNICODE | re.IGNORECASE)
         
         last_syllable = prev_syllables[-1]
         first_syllable = current_syllables[0]
         
         # If the previous syllable finish with vowel or y
         # Si la sílaba previa acaba por vocal o por 'y' griega        
         if vowels_final.search( last_syllable ) or y_griega.match( last_syllable ):
             
             # If the next syllable starts with vowel or y
             # Si la sílaba siguiente empieza por vocal o por 'y' griega no seguida de vocal  
             if vowels_init.match( first_syllable ) or y_griega.match( first_syllable ):
                 
                 # There is a synalepha
                 # Hay sinalefa
                 synalepha = True
                 
                 # Identify the presence of hyatus
                 # Identificar la presencia de hiato
                 
                 # if next word finishs any of the syllables is tonic
                 # Si la palabra anterior acaba por sílaba tónica o la siguiente empeiza por tal       
                 if (prev_tonic == -1) or current_tonic == -len(current_syllables):
                     
                     # There is hyatus
                     # Hay hiato
                     synalepha_hyatus = True
                          
    return ( synalepha, synalepha_hyatus )

    
def correction_by_synalephas( verse_syllables, accents_vector, synalephas_vector ):
    
    # Calculate the number of synalephas
    # Calcula el número de sinalefas
    synalephas_number = len( synalephas_vector )

    # Calculate the number of metric syllables, substracting the synalephas
    # Calcula el número de silabas métricas restando las sinalefas
    metric_syllables = verse_syllables - synalephas_number
    
    # Relocate the accents from the synalepha
    # Reposiciona los acentos a partir de la sinalefa
    if synalephas_number > 0:
        
        # Go to all synalephas in the vector
        # Recorre las sinalefas registradas en el vector
        for synalepha in synalephas_vector:
            
            synalepha = synalepha-1
            
            # Initialize the vector with the accents
            # Inicializamos el vector de acentos            
            acc_idx = 0
            
            # Run through the vector of accents
            # Recorremos el vector de acentos
            for accent in accents_vector:
                
                # If the position of the accent exceeds the synalepha
                # Si la posición del acento supera la sinalefa
                if accent >= synalepha:
                    
                    # substract 1
                    # Le restamos 1 a su posición
                    accents_vector[ acc_idx ] = accent - 1
                
                # Actualize the vector of accents
                # Actualizamos el vector de acentos
                acc_idx += 1
                
    return( metric_syllables, accents_vector )

def rhyme(word1, word2):
    s1 = syllables(word1)
    s2 = syllables(word2)
    
    t1 = tonic_syllable(s1)
    t2 = tonic_syllable(s2)
    
    endC1 = sound_correction("".join(s1[t1:]))
    endC2 = sound_correction("".join(s2[t2:]))

    endA1 = re.sub(r'[^aeiouáéíóúáü]', '', endC1, flags=re.IGNORECASE)
    endA2 = re.sub(r'[^aeiouáéíóúáü]', '', endC2, flags=re.IGNORECASE)
    
    strong = (endC1 == endC2)
    soft = (endA1 == endA2)
    
    return strong, soft

def sound_correction(text):
    '''
    R suave y R fuerte?
    '''
    text = text.replace("v","b")
    
    text = text.replace("ca","ka")
    text = text.replace("ce","ze")
    text = text.replace("ci","zi")
    text = text.replace("co","ko")
    text = text.replace("cu","ku")
    
    text = text.replace("que","ke")
    text = text.replace("qui","ki")
    
    text = text.replace("ge","je")
    text = text.replace("gi","ji")
    
    text = text.replace("gue","ge")
    text = text.replace("gui","gi")
    
    return text

def final_rhyme_analysis(poem):
    final_words = []    
    for verse in poem:
        verse = clean_punctuation(verse)
        words_verse = verse.split()
        final_words.append(words_verse[-1])
        
    keys = string.ascii_lowercase
    rhyme_scheme = {}

    for word1 in enumerate(final_words):
        for word2 in enumerate(final_words):
            [R,r] = rhyme(word1[1],word2[1])
            
            if word1[1] != word2[1]:
            
                if word1[0] not in sum(rhyme_scheme.values(),[]):
    
                    if R:
                        rhyme_scheme[keys[0].upper()] = [word1[0], word2[0]]
                        keys=keys[1:]                   
                        
                    elif r:
                        rhyme_scheme[keys[0]] = [word1[0], word2[0]]
                        keys=keys[1:]

    return rhyme_scheme