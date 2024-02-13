from utils import *
from formats import *
import xml.etree.ElementTree as ET

def repleaceTheseChords(mySequence, verbose = False):
    sequence = []
    correct_this = {
        "9sus4 add 4 subtract 3 add b9 add 4 subtract 3 add b9 alter #5": "sus add b2 add 8",
        "7 add 4 subtract 3 add b9 add 4 subtract 3 add b9 alter #5": "sus add b2 add 8",
        "7 add b9 add 4 subtract 3 add b9 add 4 subtract 3": "sus add b2 add 8",
        "13sus4 add 4 subtract 3 add b9 add 4 subtract 3": "sus add b2 add 8 add 6",
        "9sus4 add 4 subtract 3 add b9 add 4 subtract 3": "sus add b2 add 8",
        "7 add 4 subtract 3 add b9 add 4 subtract 3": "sus add b2 add 8",
        "13sus4 add 4 subtract 3 add 4 subtract 3": "sus add b2 add 6 add 8",
        "9sus4 add 4 subtract 3 add 4 subtract 3": "sus add 9",
        "9sus4 add 4 subtract 3 add #9 alter #5": "sus add b2 add 8",
        "9sus4 add 4 subtract 3 add b9 alter #5": "7 sus add b9",
        "9sus4 alter #5 add b9 add 4 subtract 3": "7 sus add 9",
        "7sus4 add 7 add b9 add 4 subtract 3": "7 sus",
        "13sus4 add 4 subtract 3 alter #11": "7 sus add 6",
        "13sus4 add 4 subtract 3 alter b9": "7 sus add 6",
        "13sus4 add 4 subtract 3 alter #5": "7 sus add 6",
        "9sus4 add 4 subtract 3 alter #5": "7 sus add 6 add 9",
        "13sus4 add 4 subtract 3 add #11": "7 sus add 6",
        "9sus4 alter b5 add 4 subtract 3": "7 sus add 6",
        "13sus4 add #11 add 4 subtract 3": "7 sus add 6",
        "13sus4 add 4 subtract 3 add b13": "7 sus add 6",
        "9sus4 alter #5 add 4 subtract 3": "7 sus add 9",
        "9sus4 add 4 subtract 3 alter b5": "7 sus add 9",
        "13sus4 add 4 subtract 3 add #9": "7 sus add 6 add 9",
        "9sus4 add 4 subtract 3 add #11": "7 sus add 9",
        "13sus4 add 4 subtract 3 add b9": "7 sus add b2 add 8 add 6",
        "9sus4 add 4 subtract 3 add b9": "7 sus add b2 add 8",
        "13sus4 add 4 subtract 3 add 7": "7 sus add 6",
        "9sus4 add 4 subtract 3 add 9": "7 sus add 9",
        "7sus4 add 4 subtract 3 add 7": "7 sus",
        "m69 add 4 subtract 3 add 9": "7 sus add 6 add 9",
        "7 add #11 add b9 alter #11": "7 add #11 add b9",
        "13sus4 add 4 subtract 3": "7 sus add 6",
        "m69 add 9 add #7 add 9": "m7 add 9 alter #7",
        "9sus4 add 4 subtract 3": "7 sus add 9",
        "alter #5 add b9 sus": "7 sus alter #5 add b9",
        "add b9 sus add b9": "7 sus add b9",
        "add 4 subtract 3": "sus",
        "m69 add 9 add 9 add 9": "m7 add 6 add 9",
        "7alt alter b5 add #9": "7 alter b5 add #9",
        "7sus4 add 7 alter b9": "sus add b2 add 8",
        "m7 alter b5 alter b9": "m7 alter b5 add b9",
        "7 alter b9 alter #5": "7 alter b5 add b9",
        "maj9 add #11 add b9": "maj7 add 9 add #11",
        "m69 add 9 alter #5": "m6 add 9",
        "maj9 add #11 add 7": "maj7 add 9 add #11",
        "m69 add 9 alter b5": "m6 add 9",
        "7 alter b9 add b13": "7 add b9 add b13",
        "7 alter #11 add b9": "7 add b9 add #11",
        "69 add 9 alter b5": "6 add 9 alter b5",
        "69 alter b5 add 9": "6 add 9 alter b5",
        "69 add 9 alter #5": "6 add 9 alter b5",
        "maj9 add #11": "maj7 add 9 add #11",
        "7sus4 add 9 add 7": "7 sus add 9",
        "7sus4 add #11 add 7": "7 sus add #11",
        "7sus4 alter #5 add 7": "7 sus alter #5",
        "sus4 alter b5 add 7": "sus alter b5",
        "7sus4 add b13 add 7": "7 sus add b13",
        "add #11 add #9 add #11 add #9": "add #9 add #11",
        "add #11 add #11" : "add #11",
        "77 sus add 9": "7 sus add 9",
        "7sus4 add 7 add 7": "7 sus",
        "7sus4 add 7": '7 sus',
        "7susadd3": '7 sus',
        "9 sus alter #5": "7 sus",
        "add b9 add b9 add 9": "add b9",
        "7 sus add 7": '7 sus',
        "7 sus alter b5": "7 sus",
        "7 7 sus add b13": "7 add b13",
        "maj7 7 sus alter #5": "maj7",
        "maj7 sus add #11": "maj7 add #11",
        "*..........*": "",
        "13 sus alter #11": "sus add #11",
        "13 sus alter b9": "sus add b9",
        "9 7 sus add #11": "7 sus add #11",
        "alter b5 add b9 alter #5": "alter b5 add b9 add b13",
        "alter b5 alter b5 alter b5": "alter b5",
        "alter b5 add #9 alter #5": "alter b5 add #9 add b13",
        "dim(maj7)": "m7 alter #7",
        "add 9 add 9 add 9": "add 9",
        "add b9 add b9 add b9": "add b9",
        "add b9 add b9 alter #5": "add b9 alter #5",
        "add b9 add b9": "add b9",
        "add 9 add 9": "add 9",
        "alter b5 alter b5": "alter b5",
        "add #7 add #7": "add #7",
        "add #9 add #9": "add #9",
        "add b9 sus add b9 alter #5": "sus add b9 alter #5",
        "add b9 sus add b9": "sus add b9",
        "alter b5 sus": "sus alter b5",
        "add 7 add b9 sus": "7 sus add b9",
        "add b9 add 9": "add b9",
        "m69 add 9": "m6 add 9",
        " m(add9)": "m add 9",
        " *-add9*": "m add 9",
        "*7b5#5*": "7 alter b5",
        "alter #5 alter #5": "alter #5",
        "alter #5 alter b5": "alter b5",
        "alter b5 alter #5": "alter b5",
        "alter #5 sus": "7 sus alter #5",
        "alter #5 add b9 sus": "7 sus add b9 alter #5",
        "alter b5 add #9 add b9": "alter b5 add b9",
        "*sus4*": "7 sus",
        "maj13": "maj7 add 13",
        "*6#9*": "6 add #9",
        "*ø11*": "m7 alter b5",
        "*dim*": "dim7",
        "*mb9*": "m add b9",
        "*-add9*": "m add 9",
        "*mM7*": "m7 alter #7",
        "*-b5*": "m7 alter b5",
        "*6b5*": "6 add 9 alter b5",
        "7alt": "7 add #11 add b9",
        "7#5#9": "7 add #5 add #9",
        "m(add9)": "m add 9",
        "add b13 sus": "7 sus add b13",
        "add #11 sus": "7 sus add #11",
        "add b9 sus": "sus add b9",
        "add b9 sus add #9 alter #5": "sus add b9 alter #5",
        "7 7 sus add b9": "7 sus add b9",
        "*7+*": "maj7",
        "*m7*": "m7",
        "*-3*": "m",
        "maj9": "maj7 add 9",
        "-N3": "m",
        "*m*": "m",
        "*O*": "dim7",
        "-7s": "m7",
        "77": "7",
        "m7 sus": "m7",
        "**": "",
        "N.C.": ""
    }
    
    #for key, value in correct_this.items():
    #    print('translating', key, 'to', value)
    #    mySequence = np.vectorize(lambda x: x.replace(key, value))(mySequence)
    
    #keys = list(correct_this.keys())
    #values = list(correct_this.values())

    for song in tqdm(mySequence):
        tmp = []  
        for element in song:            
            for key, value in correct_this.items():
                if key in element:
                    if (verbose):
                        print(element, '-->', value)
                    element = element.replace(key, value)
                    break
            tmp.append(element)
        sequence.append(tmp)
    sequence = np.array(sequence, dtype=object) 
    
    x = 0
    for song in sequence:
        y = 0
        for chord in song:
            s = chord.split(' ')
            if len(s) >= 5:
                #print(x)
                if s[1]+s[2] == s[3]+s[4]:
                    #print(x, y, chord)
                    sequence[x][y]=s[0]+' '+s[1]+' '+s[2]
                    #print(sequence[x][y])
            y+=1
        x+=1
             
    return sequence

def parse_info_from_XML(path, BLOCK_SIZE):
    '''
    Populate a chord sequence and an offset sequence from a XML file
    '''
    chord_sequence_list = []
    offset_sequence_list = []
    meta_info_list = []
    
    for file in tqdm(os.listdir(path)):
    
        if (file == '.DS_Store'):
            continue
            
        song_path = path+'/'+file
        
        tree = ET.parse(song_path)
        root = tree.getroot()

        #possible_types = ['segno', 'rehearsal', 'coda', 'words']

        bar = '|'
        song_form = ''
        tone = ''
        coda = ''
        chord = ''
        nature = ''
        extension = ''
        slash = ''
        offset = 0
        the_chord_sequence = []
        the_offset_sequence = []

        #Division is the number of ticks per quarter note
        division = int(root.find('part').find('measure').find('attributes').find('divisions').text)

        meta_info = get_metadata(song_path)
        meta_info_list.append(meta_info)

        #define the Style
        style_token = '<style>'
        the_chord_sequence.append(style_token)
        the_offset_sequence.append(offset)
        the_chord_sequence.append(meta_info['style'])
        the_offset_sequence.append(offset)

        for measure in root.iter('measure'):
            
            #get the offset reference
            measure_number = int(measure.attrib.get('number'))
            #print(measure_number, '->', offset)
        
            #get the bars
            bar = '|'
            barline = measure.find('barline')
            if barline != None:
                repeat = barline.find('repeat')
                if repeat != None:
                    direction = repeat.attrib.get('direction')
                    if direction == 'forward':
                        bar = '|:'
                    
            #print(bar)
            the_chord_sequence.append(bar)
            the_offset_sequence.append(offset)
            #get the Form
            direction = measure.find('direction')
            if direction != None:
                direction_type = direction.find('direction-type')
                
                segno = direction_type.find('segno')
                if segno != None:
                    song_form = 'Form_Segno'
                    #print(song_form)
                    the_chord_sequence.append(song_form)
                    the_offset_sequence.append(offset)
                
                coda = direction_type.find('coda')
                if coda != None:
                    song_form = 'Form_Coda'
                    #print(song_form)
                    the_chord_sequence.append(song_form)
                    the_offset_sequence.append(offset)
                    
                form = direction_type.find('rehearsal')
                if form != None:
                    song_form = 'Form_'+form.text
                    #print(song_form)
                    the_chord_sequence.append(song_form)
                    the_offset_sequence.append(offset)
                    
            #get barline
            barline = measure.find('barline')
            if barline != None:
                ending = barline.find('ending')
                if ending != None:
                    number = ending.attrib.get('number')
                    if number != None:
                        bar = 'Repeat_'+ str(number) #this section defines the bar to be repeated
                        #print(bar)
                        the_chord_sequence.append(bar)
                        the_offset_sequence.append(offset)
                        
            
                
            #get the chords
            for harmony in measure.iter('harmony'):
                root = harmony.find('root')
                note = root.find('root-step')
                sharp = root.find('root-alter')
                if sharp != None:
                    sharp = sharp.text
                    if sharp == '-1': #Remember to check double sharp and double flat
                        tone = 'b'
                    elif sharp == '1':
                        tone = '#'
                    elif sharp == '0':
                        tone = ''
                
                note = note.text+tone
                kind = harmony.find('kind')
                nature = kind.attrib.get('text')
                
                #get nature of the chord
                if nature == None:
                    nature = ''
                
                #get the extension
                degree = harmony.find('degree')
                extension = ''
                if degree != None:
                    for degree in measure.iter('degree'):
                        
                        degree_type = degree.find('degree-type').text
                        relatedNote = degree.find('degree-value').text
                        degree_sharp = degree.find('degree-alter').text
                        if degree_sharp == '-1':
                            relatedNote = 'b'+relatedNote
                        elif degree_sharp == '-2':
                            relatedNote = 'bb'+relatedNote
                        elif degree_sharp == '1':
                            relatedNote = '#'+relatedNote
                        elif degree_sharp == '2':
                            relatedNote = '##'+relatedNote
                            
                        extension += ' ' + degree_type + ' ' +relatedNote
                else:
                    extension = ''
                
                #get slash chord
                bass = harmony.find('bass')
                if bass != None:
                    bass_step = bass.find('bass-step')
                    slash = '/'+bass_step.text
                else :
                    slash = ''
                    
                chord = note + str(nature) + extension + str(slash)
                #print(chord)
                the_chord_sequence.append(chord)
            
            #get durations offset
            for note_element in measure.iter('note'):
                duration = int(note_element.find('duration').text) / division
                the_offset_sequence.append(offset)
                offset += duration
                #print(offset)
                
            #this second bar is relevat to close the section
            if barline != None:
                repeat = barline.find('repeat')
                if repeat != None:
                    direction = repeat.attrib.get('direction')
                    if direction == 'backward':
                        bar = ':|'
                        #print(bar)
                        the_chord_sequence.append(bar)
                        the_offset_sequence.append(offset)
        
        
        the_chord_sequence = np.array(the_chord_sequence, dtype=object)
        the_offset_sequence = np.array(the_offset_sequence, dtype=float)
        '''
        #divide the chords into sections base, nature, extension, slash
        #the first two elements are the style 
        the_sequence = the_chord_sequence[2:]
        the_offset = the_offset_sequence[2:]

        format = the_chord_sequence[0:2].tolist()

        offset_format = the_offset_sequence[0:2].tolist()

        the_sequence, the_offset = getArrayOfElementsInChord(the_sequence, the_offset)
        the_offset = offset_format + the_offset
        the_sequence = format + the_sequence
        
        #the final format of the sequence is:
        the_sequence = format_start_end(the_sequence)
        the_sequence = padding(the_sequence, BLOCK_SIZE)
        
        the_offset = format_start_end(the_offset)
        the_offset = padding(the_offset, BLOCK_SIZE)
        chord_sequence_list.append(the_sequence)
        offset_sequence_list.append(the_offset)
        
        '''
        chord_sequence_list.append(the_chord_sequence)
        offset_sequence_list.append(the_offset_sequence)
    
    chord_sequence_list = np.array(chord_sequence_list, dtype=object)
    offset_sequence_list = np.array(offset_sequence_list, dtype=object)
    meta_info_list = np.array(meta_info_list, dtype=object)
    
    print(chord_sequence_list.shape, offset_sequence_list.shape)
    return chord_sequence_list, offset_sequence_list, meta_info_list

def formatChordsVocabulary(theChordsSequence, theOffetsSequence, blockSize):
    chord_sequence_list = []
    offset_sequence_list = []
    i = 0
    for theChords, theOffets in zip(theChordsSequence, theOffetsSequence):
        theChords = np.array(theChords, dtype=object)
        theOffets = np.array(theOffets, dtype=float)
        
        #divide the chords into sections base, nature, extension, slash
        #the first two elements are the style 
        the_sequence = theChords[2:]
        the_offset = theOffets[2:]

        format = theChords[0:2].tolist()
        offset_format = theOffets[0:2].tolist()

        the_sequence, the_offset = getArrayOfElementsInChord(the_sequence, the_offset)
        the_offset = offset_format + the_offset
        the_sequence = format + the_sequence

        #the final format of the sequence is:
        the_sequence = format_start_end(the_sequence)
        the_offset = format_start_end(the_offset)
        
        #if (the_sequence.shape[0] > 768):
        #    print(i, the_sequence.shape[0], the_offset.shape[0], format)
        
        the_sequence = padding(the_sequence, blockSize)
        the_offset = padding(the_offset, blockSize)
        
        chord_sequence_list.append(the_sequence)
        offset_sequence_list.append(the_offset)
        i+=1
            
    chord_sequence_list = np.array(chord_sequence_list, dtype=object)
    offset_sequence_list = np.array(offset_sequence_list, dtype=object)
    print(chord_sequence_list.shape, offset_sequence_list.shape)
    return chord_sequence_list, offset_sequence_list


def correctDuplicatedExtensions(dataset, offset):
    corrected_datset = []
    corrected_offset = []
    #i = 0
    for song, off in zip(dataset, offset):
        cleaned_list = []
        cleanned_offset = []
        for chord, ofNum in zip(song, off):
            new = []
            s = chord.split(' ')
            if len(s) >= 2 and len(s) % 2 == 0:
                tmp = s[0] + ' ' + s[1]
                new.append(tmp)
                for i in range(2, len(s), 2):
                    r = s[i]+ ' ' + s[i+1]
                    if tmp != r:
                        new.append(r)
                        
            else:
                new.append(chord)
            
            new = ' '.join(new)
            cleaned_list.append(new)
            cleanned_offset.append(ofNum)
        #i+=1
        corrected_datset.append(cleaned_list)
        corrected_offset.append(cleanned_offset)
    corrected_datset = np.array(corrected_datset, dtype=object)
    corrected_offset = np.array(corrected_offset, dtype=object)
    print(corrected_datset.shape, corrected_offset.shape)
    return corrected_datset, corrected_offset

#----------------------------------------------------------------------------
#Chel for all chords that can not be read by music21
def checkIncompatibleChords(data):
    #save all chords not compatible with music21
    incompatible_chords = []
    s_id = 0
    for songs in tqdm(data):
        #let's pass the starting and style elements
        for i in range(len(songs)):
            element = songs[i]
            if element.find('b') > 0 and element[1:2] == 'b':
                element = element[0:1] + '-' + element[2:]
            try:
                tmp = m21.harmony.ChordSymbol(element)
            except:
                #erase the first character
                print(s_id, element)
                if element[1:2] == '-' or element[1:2] == '#':
                    element = element[2:]
                else:
                    element = element[1:]
                if element.find('/'):
                    s = element.split('/')
                    element = s[0]
                incompatible_chords.append(element)
        s_id += 1

    incompatible_chords = list(set(incompatible_chords))
    print(incompatible_chords)
    return incompatible_chords