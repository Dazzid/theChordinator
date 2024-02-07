#%%

from utils import get_metadata, getArrayOfElementsInChord
import xml.etree.ElementTree as ET

#song_path = "../data/iRealXML/Message To A Friend.xml"
song_path = "../data/Penny Lane.musicxml"

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
print(division)

meta_info = get_metadata(song_path)

print(meta_info)

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

print(the_chord_sequence.shape, the_offset_sequence.shape)

#divide the chords into sections base, nature, extension, slash
#the first two elements are the style 
the_sequence = the_chord_sequence[2:]
the_offset = the_offset_sequence[2:]

format = the_chord_sequence[0:2].tolist()

offset_format = the_offset_sequence[0:2].tolist()

the_sequence, the_offset = getArrayOfElementsInChord(the_sequence, the_offset)
the_offset = offset_format + the_offset
the_sequence = format + the_sequence
print(the_sequence)

#adjust the offset sequence
the_sequence = np.array(the_sequence, dtype=object)
the_offset = np.array(the_offset, dtype=float)

print(the_sequence.shape, the_offset.shape)

for i in range (len(the_sequence)):
    d = i%1
    if (d == 0):
        print('\n')
    print("'"+the_sequence[i]+"'" + ' -> '+ str(the_offset[i]), end=' ')
# %%
