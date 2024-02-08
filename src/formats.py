#import music21 as m21
import numpy as np
import librosa as lib
from tqdm.auto import tqdm

# some by default declarations
def getNotes():
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'B-', 'E-', 'A-', 'D-', 'G-', 'C-']
    return notes

def getFormat():
    format = ['.', '<start>', '<end>', '<pad>']
    return format

def listToIgnore():
    ignore_list = {'<start>', '<end>', '<pad>', '.', '|', 'Repeat_0', 'Repeat_1', 'Repeat_2', 'Repeat_3', 
                   'Form_A', 'Form_B', 'Form_C', 'Form_D', 
                    'Form_verse', 'Form_intro', 'Form_Coda', 'Form_Segno', '|:', ':|'}
    return ignore_list

#----------------------------------------------------------------------
def splitChordTokens(chord):
    '''This function splits the chord tokens into a list of tokens
    input is a string of the chord
    output is a list of tokens
    '''
    list = []
    section = chord.split(' ')
    base = section[0][:1]
    nature = section[0][1:]
    
    #fix the bpedal error
    #if nature == 'bpedal':
    #    nature = nature.replace('bpedal', '-pedal')
                    
    #fix the shifted error when sharp and flat appears   
         
    if '###' in nature or '---' in nature:
        base = section[0][:4]
        nature = section[0][4:]
    
    elif '##' in nature or '--' in nature:
        base = section[0][:3]
        nature = section[0][3:]
    
    elif '#' in nature or '-' in nature:
        base = section[0][:2]
        nature = section[0][2:]
        
    #fix the base error when is b intead of -
    #if base[1:] == 'b':
    #    base = base.replace('b', '-')
        
    ext = ''
    for i in range(1, len(section)):
        ext += section[i]+ ' '
    ext = ext[:-1]
    
    list.append(base)
    list.append(nature)
    
    #add = ext.count('add')
    #subtract = ext.count('subtract')
    #alter = ext.count('alter')
    #print(add, subtract, alter)
    
    #check if the chord has extensions
    subSection = ext.split(' ')
  
    if (len(subSection) >  0):
        #print(subSection)
        line = ''
        for i in range(len(subSection)):
            line += subSection[i] + ' '
            #print(line)
        if line[-1] == ' ':
            line = line.rstrip()
        list.append(line)
    
    discart = ''
    while discart in list: list.remove(discart)
    return list

#------------------------------------------------------------------------------
def splitSlashChords(chord):
    '''This function splits the slash chords into a list of tokens
    input is a string of the chord
    output is a list of tokens
    '''
    list = []
    section = chord.split('/')
    list = splitChordTokens(section[0]) + ['/'] + splitChordTokens(section[1])
    return list

#Split the chords --------------------------------------------
def splitTheChords(chords):
    ignore_list = listToIgnore()
    chord_list = []
    
    for chord in chords:
        if chord in ignore_list:
            chord_list.append(chord)
            continue
        
        chord_list.append('.')
        
        if '/' in chord:
            result = splitSlashChords(chord)
        else :
            result = splitChordTokens(chord)
            
        chord_list.extend(result)
        
    return chord_list


#get all chords from file -----------------------------------------------------
def get_all_chords_from_file(path):
    """
    Iterate over the files in a directory and extract the chords
    """
    chord_list = []
    xml_song = m21.converter.parse(path)

    m = xml_song.parts[0].getElementsByClass(m21.stream.Measure)
    for x in range(len(m)):
        #durations = []
        chords = m[x].getElementsByClass(m21.harmony.ChordSymbol)
        #duration = m[x].getElementsByClass(m21.note.Note)    
        for chord_type in chords:
            #first clean the data not related to the chord
            chord = chord_type.figure
            if chord == "Chord Symbol Cannot Be Identified" or chord == "N.C.":
                break

            if '/' in chord:
                result = splitSlashChords(chord)
            else :
                result = splitChordTokens(chord)
            chord_list = chord_list + result
    # to remove duplicated from list
    result = set(chord_list)
    return result

#Convert the separated chords into one unify chord -----------------------------
def convertChordsFromOutput(sequence):
    chord = []
    chordArray = []
    ignore = listToIgnore()
    ignore.remove('.') #we need the dot to identify the chord
    ignore.remove('|')
    ignore.remove(':|')
    ignore.remove('<end>')
    #if sequence[len(sequence)-1] != '.':
    #    sequence.append('.')
    for i in range (3, len(sequence)): #first two elementes are style context
        element = sequence[i]
        
        if element not in ignore:
            #check if the chord starts
            if element != '.' and element != '|' and element != ':|' and element != '<end>':
                #print(i, duration)
                #collect the elements of the chord
                if element.find('add') >= 0 or element.find('subtract') >= 0 or element.find('alter') >= 0:
                    chord.append(' ')
                chord.append(element)
                #print(i, chord)
            if len(chord) > 0:
                if  element == '.' or element == '|' or element == ':|' or element == '<end>':
                    #print(i, element)listToIgnore
                    #join the sections into a formatted chord
                    c = ''.join(chord) 
                    chordArray.append(c)
                    chord = []
               
    return chordArray


#Get the array of elements per chord and also configure the offsets --------------------------------------------
def getArrayOfElementsInChord(chords, offsets):
    ignore_list = listToIgnore()
    chord_list = []
    offset_list= []
    #print(type(chords))
          
    for chord, offset in zip(chords, offsets):
        if chord in ignore_list:
            chord_list.append(chord)
            offset_list.append(offset)
            continue
        
        chord_list.append('.')
        offset_list.append(offset)
        
        if '/' in chord:
            result = splitSlashChords(chord)
        else :
            result = splitChordTokens(chord)
            
        chord_list.extend(result)
        offset_list.extend([offset] * len(result))
    
    return chord_list, offset_list


#-------------------------------------------------------------------------
def extendDatasetToAllNotes(data):
    '''
    Get all the songs by default and it extend to all posible keys 
    input: chord progressions with '<start>', '<end>' and '<pad>' tokens
    output: same chord progressions transposed to all posible keys
    it means each song is in 18 keys, it needs to be shuffled 
    '''
    ignore_list = listToIgnore()
    
    x_data = []
    erros_found=[]
    notes = getNotes()
    file = 0
    print(data.shape)
    for songs in tqdm(data):
        #let's pass the starting and style elements
        for i in range(len(notes)):
            transposed_song = []
            style_format = songs[:3]
            chord_sequence = songs[3:]
            for element in chord_sequence:
                if element not in ignore_list:
                    
                    if element.find('b') > 0 and element[1:2] == 'b':
                        element = element[0:1] + '-' + element[2:]
                    try:
                        tmp = m21.harmony.ChordSymbol(element)
                    except:
                        print('error in file:', file, 'element:', element)
                        erros_found.append(element)
                    #Here we transpose the song to all possible keys
                    
                    loc = notes.index(tmp.bass().name) 
                    ref = (loc + i) % len(notes) #calculate the distance to the reference
                    interval = m21.interval.Interval(tmp.bass(), m21.pitch.Pitch(notes[ref]))
                    tmp2 = tmp.transpose(interval).figure
                    #print(i, 'origin:', tmp.figure, 'transposed:', tmp2, 'interval:', interval.name)
                    transposed_song.append(tmp2)
                else:
                    transposed_song.append(element)
            transposed_song = style_format + transposed_song
            x_data.append(transposed_song)
            
        file += 1    
    x_data = np.array(x_data, dtype=object)
    return x_data, erros_found

#Correct the format of the chords
#-------------------------------------------------------------------------
def correctBackTheFormat(reference, toBeCorrected):
    '''
    This function will correct the format of the chords
    '''
    new_dataset = []
    for origin, to_correct in zip(reference, toBeCorrected):
        #to_correct = transposed_data[0]
        to_correct = [s.replace('-', 'b') for s in to_correct]       
        to_correct = splitTheChords(to_correct)

        chord_id = 0
        fixed = []
        local_format = origin[:3]

        for i in range(3, len(origin)):
            element = origin[i]
            check = listToIgnore()
            check.remove('.') #dot is part of the chord
            
            if element in check: #this is asking if it is a chord
                fixed.append(element)
            else:
                try:
                    newChord = to_correct[chord_id]
            
                    #print(element, chord_id, newChord)
                    fixed.append(newChord)
                    chord_id += 1
                except:
                    print('error', i, '--->', element, chord_id, newChord)
                    break
                
        #add the format back
        fixed = list(local_format) + fixed
        new_dataset.append(fixed)
    
    new_dataset = np.array(new_dataset, dtype=object)
    return new_dataset

#Check the chord is handdleled by music21
def checkChordFormat(element):
    tmp = m21.harmony.ChordSymbol(element)
    return [str(p) for p in tmp.pitches]

#Correct style tokens by reference
def correctStyleTokensInMeta(data):
    #Get all the elements in meta and correct the style tokens
    for x in tqdm(range(len(data))):
        element = data[x]['style']
        if element == "Even 8th's" or element == "Even 8's":
            data[x]['style'] = 'Even 8ths'
        if (element.find('Swing') != -1):
            data[x]['style'] = 'Jazz'
        if (element.find('Blues') != -1):
            data[x]['style'] = 'Blues'
        if (element.find('Folk') != -1):
            data[x]['style'] = 'Folk'
        if (element.find('Fusion') != -1):
            data[x]['style'] = 'Jazz'
        if (element.find('Jazz') != -1):
            data[x]['style'] = 'Jazz'
        if (element.find('Bossa') != -1):
            data[x]['style'] = 'Bossa'
        if (element.find('Reggae') != -1):
            data[x]['style'] = 'Reggae'
        if (element.find('Folk') != -1):
            data[x]['style'] = 'Folk'
        if (element.find('Samba') != -1):
            data[x]['style'] = 'Samba'
        if (element.find('Funk') != -1):
            data[x]['style'] = 'Funk'
        if (element.find('Pop') != -1):
            data[x]['style'] = 'Pop'
        if (element.find('Son') != -1):
            data[x]['style'] = 'Son'
        if (element.find('Rock') != -1):
            data[x]['style'] = 'Rock'
        if (element.find('Soul') != -1):
            data[x]['style'] = 'Soul'
        if (element.find('Balad') != -1):
            data[x]['style'] = 'Balad'
        if element == "R'n'B":
            data[x]['style'] = "RnB"
        if element == 'Beatles': 
            data[x]['style'] = 'Rock'
        if element == 'Afoxe': 
            data[x]['style'] = 'Afoxé'
        if element == 'Worship': 
            data[x]['style'] = 'Gospel'
        if element == 'Traditional Gospel': 
            data[x]['style'] = 'Gospel'
    
#------------------------------------------------------------------------------
#Correct style tokens by reference in meta data
def correctStyleTokens(data):
    size_x, size_y = data.shape
    for x in tqdm(range(size_x)):
        for y in range(size_y):
            element = data[x][y]
            if element == "Even 8th's" or element == "Even 8's":
                data[x][y] = 'Even 8ths'
            if (element.find('Swing') != -1):
                data[x][y] = 'Jazz'
            if (element.find('Blues') != -1):
                data[x][y] = 'Blues'
            if (element.find('Folk') != -1):
                data[x][y] = 'Folk'
            if (element.find('Jazz') != -1):
                data[x][y] = 'Jazz'
            if (element.find('Fusion') != -1):
                data[x][y] = 'Jazz'
            if (element.find('Bossa') != -1):
                data[x][y] = 'Bossa'
            if (element.find('Reggae') != -1):
                data[x][y] = 'Reggae'
            if (element.find('Folk') != -1):
                data[x][y] = 'Folk'
            if (element.find('Samba') != -1):
                data[x][y] = 'Samba'
            if (element.find('Funk') != -1):
                data[x][y] = 'Funk'
            if (element.find('Pop') != -1):
                data[x][y] = 'Pop'
            if (element.find('Son') != -1):
                data[x][y] = 'Son'
            if (element.find('Rock') != -1):
                data[x][y] = 'Rock'
            if (element.find('Soul') != -1):
                data[x][y] = 'Soul'
            if (element.find('Balad') != -1):
                data[x][y] = 'Balad'
            if element == "R'n'B":
                data[x][y] = "RnB"
            if element == 'Beatles': 
                data[x][y] = 'Rock'
            if element == 'Afoxe': 
                data[x][y] = 'Afoxé'
            if element == 'Worship': 
                data[x][y] = 'Gospel'
            if element == 'Traditional Gospel': 
                data[x][y] = 'Gospel'
                
#-------------------------------------------------------------------------                
#Get the midi notes from the chords
def get_the_midi_notes(chord_list):
    ''' 
    input: the chords in the format of the dataset
    output: the midi notes of the chords
    '''
    noChord = [0,0,0,0,0,0,0,0] #this part is for the no chord
    slashChord = [0,0,0,0,0,0,0,127] #this part is for the no chord
    starting = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    all_midiNotesChords = []
    ignore = listToIgnore()
    ignore.remove('.') #we need the dot to identify the chord
    ignore.remove('<end>')
    x = 0
    for song in tqdm(chord_list):
        songChordMidiNotes = []
        section = song[3:]
        for element in section:
            if element not in ignore:
                #print(element)
                if element == '.':
                    buildChord = ''
                    songChordMidiNotes.append(noChord)
                elif element != '<end>':
                    if element == '/':
                        songChordMidiNotes.append(slashChord)
                        buildChord+=element
                    else:
                        buildChord+=element
                        #print('chord', buildChord)
                        #Get the notes from the chord
                        try:
                            chords = m21.harmony.ChordSymbol(buildChord)
                        except:
                            print('Error parsing element:', x, buildChord)
                        #Define an octave for the notes
                        chords = chords.closedPosition(forceOctave=4, inPlace=False)
                        #Create the array of notes
                        theNotes = [str(p) for p in chords.pitches]
                        midiNotes = []
                        for n in theNotes:
                            change = n.find('-')
                            if change != -1:
                                n = n.replace('-', 'b')
                            #Translate the notes to midi notes
                            midi_key = lib.note_to_midi(n)
                            #Recollect the notes in an array-
                            midiNotes.append(midi_key)
                        if (len(midiNotes)) < 8:
                            for i in range(8-(len(midiNotes))):
                                midiNotes.append(0.0)
                        songChordMidiNotes.append(midiNotes)
                else:
                    songChordMidiNotes.append(noChord)
            else:
                songChordMidiNotes.append(noChord)  
        songChordMidiNotes = starting + songChordMidiNotes
        all_midiNotesChords.append(songChordMidiNotes)
        x+=1
    
    return all_midiNotesChords




#-------------------------------------------------------------------------                
#Get the midi notes from the chords
def get_the_midi_in_song(song):
    ''' 
    input: the chords in the format of the dataset
    output: the midi notes of the chords
    '''
    noChord = [0,0,0,0,0,0,0,0] #this part is for the no chord
    slashChord = [0,0,0,0,0,0,0,127] #this part is for the no chord
    starting = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

    ignore = listToIgnore()
    ignore.remove('.') #we need the dot to identify the chord
    ignore.remove('<end>')
    duration = 4.0
    songChordMidiNotes = []
    section = song[3:]
    x = 0
    status = True
    for element in section:
        #print (element)
        if element == '|':
            d = 0
        if element not in ignore:
            #print(element)
            if element == '.':
                buildChord = ''
                songChordMidiNotes.append(noChord)
            elif element != '<end>':
                if element == '/':
                    songChordMidiNotes.append(slashChord)
                    buildChord+=element
                else:
                    buildChord+=element
                    #print('chord', buildChord)
                    #Get the notes from the chord
                    try:
                        chords = m21.harmony.ChordSymbol(buildChord)
                    except:
                        print('Error parsing element:', buildChord, 'in position:', x)
                        status = False
                    #Define an octave for the notes
                    chords = chords.closedPosition(forceOctave=4, inPlace=False)
                    chords.duration = m21.duration.Duration(duration)
                    #Create the array of notes
                    theNotes = [str(p) for p in chords.pitches]
                    midiNotes = []
                    for n in theNotes:
                        change = n.find('-')
                        if change != -1:
                            n = n.replace('-', 'b')
                        #Translate the notes to midi notes
                        midi_key = lib.note_to_midi(n)
                        #Recollect the notes in an array-
                        midiNotes.append(midi_key)
                    if (len(midiNotes)) < 8:
                        for i in range(8-(len(midiNotes))):
                            midiNotes.append(0)
                    songChordMidiNotes.append(midiNotes)
            else:
                songChordMidiNotes.append(noChord)
        else:
            songChordMidiNotes.append(noChord)
        x+=1
    songChordMidiNotes = starting + songChordMidiNotes

    
    return songChordMidiNotes, status


#-------------------------------------------------------------------------                
#Correct the extensions of the chords
def correct_extensions(song, offset, block_size):
    i = 0
    for chord, off in zip(song, offset):
        if '<pad>' not in chord:
            if 'add' in chord or 'alter' in chord:
                toSplit = chord.split(' ')
                if len(toSplit) > 2:
                    #print('cleared ---->', song[i])
                    song = np.delete(song, i)
                    tmpOff = off
                    #print('cleared ---->', off)
                    offset = np.delete(offset, i)
                    i-=1
                    for x in range(0, len(toSplit), 2):
                        #print(toSplit[x], toSplit[x+1])
                        newElement = toSplit[x] + ' ' + toSplit[x+1]  
                        song = np.insert(song, i+1, newElement)
                        offset = np.insert(offset, i+1, tmpOff)
                        i+=1
                    
                #print(i, '------->', len(toSplit))
            i+=1

    #clear the length of the array
    for e in range(len(song)):
        if e >= block_size:
            song = np.delete(song, len(song)-1)
            offset = np.delete(offset, len(offset)-1)
    return song, offset