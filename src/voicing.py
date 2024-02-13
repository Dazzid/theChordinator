#%%
import random
# Change m11, m9, and add maj in the dataset, 
# change 7 by dom_7, change 7sus by sus7

# natures = ['maj','7sus', 'm', 'm11', 'm6', 'm7', 'm9', 'dom_7', 'maj7', 'o7', 'sus', 'sus2', 'ø7']

# alter = ['add #11', 'add #5', 'add #7', 'add #9', 'add 13', 'add 2', 'add 5', 'add 6',
#  'add 7', 'add 8', 'add 9', 'add b13', 'add b2', 'add b6', 'add b9', 'alter #11',
#  'alter #5', 'alter #7', 'alter #9', 'alter b5', 'alter b9']

# structural_elements = ['.', '|', ':|', '/', '|:']

natures = {'maj', '7sus', 'm', 'm11', 'm6', 'm7', 'm9', 'dom_7', 'maj7', 'o7', 'sus', 'sus2', 'ø7'}
alter = {'add #11', 'add #5', 'add #7', 'add #9', 'add 13', 'add 2', 'add 5', 'add 6', 'add 7', 'add 8', 'add 9', 'add b13', 'add b2', 'add b6', 'add b9', 'alter #11', 'alter #5', 'alter #7', 'alter #9', 'alter b5', 'alter b9'}

structural_elements = {'.', '|', ':|', '|:', '/', 'N.C.', 'maj'} #to add the maj token 

voicing = ['v_0', 'v_1', 'v_2', 'v_3']

all_notes = {
    'C': 48, 'C#': 49, 'Db': 49, 'D': 50, 'D#': 51, 'Eb': 51, 'E': 52, 'F': 53, 'F#': 54, 'Gb': 42, 'G': 43, 'G#': 44, 'Ab':44, 'A': 45, 'A#': 46, 'Bb': 46, 'B': 47, 
    'A##': 47, 'Abb': 43, 'Abbb': 42, 'B#': 48, 'B##': 49, 'Bbb': 45, 'Bbbb': 44, 
    'C#': 49, 'C##': 50, 'C###': 51, 'Cb': 59, 'Cbb': 58, 'D##': 52, 'Dbb': 48, 'Dbbb': 47, 'E##': 54, 'Ebb': 50, 'Ebbb': 49, 
    'F##': 55, 'F###': 56, 'Fb': 52, 'Fbb': 51, 'G##': 45, 'Gb': 42, 'Gbb': 41
    }

#define voicing for natures
maj = {'v_0':[0, 7, 12, 16], 'v_1':[0, 7, 16, 19], 'v_2':[0, 4, 7, 12], 'v_3':[0, 7, 16, 19]}
maj7 = {'v_0':[0, 11, 14, 16, 19], 'v_1':[0, 11, 16, 19], 'v_2':[0, 11, 14, 16], 'v_3':[0, 11, 14, 16, 19]}
m = {'v_0':[0, 12, 15, 19], 'v_1':[0, 15, 19, 24], 'v_2':[0, 19, 24, 27], 'v_3':[0, 12, 19, 24, 27]}

m7 = {'v_0':[0, 10, 15, 19], 'v_1':[0, 7, 10, 15], 'v_2':[0, 10, 14, 15], 'v_3':[0, 10, 14, 15]}

dom_7 = {'v_0':[0, 7, 10, 16, 19], 'v_1':[0, 10, 16, 19], 'v_2':[0, 10, 14, 16], 'v_3':[0, 10, 14, 16, 19]}

ø7 =  {'v_0':[0, 15, 18, 22], 'v_1':[0, 10, 15, 18], 'v_2':[0, 15, 18, 22, 24], 'v_3':[0, 6, 10, 15, 18]}
o7 = {'v_0':[0, 15, 18, 21], 'v_1':[0, 15, 18, 21, 24], 'v_2':[0, 18, 21, 24, 27], 'v_3':[0, 12, 15, 18, 21]}
sus = {'v_0':[0, 12, 17, 19], 'v_1':[0, 17, 19, 24], 'v_2':[0, 19, 24, 29], 'v_3':[0, 12, 19, 24, 29]} 
sus7 = {'v_0':[0, 10, 17, 19], 'v_1':[0, 10, 14, 17, 19], 'v_2':[0, 10, 14, 17], 'v_3':[0, 10, 14, 17, 19]}
sus2 = {'v_0':[0, 14, 19, 24], 'v_1':[0, 12, 19, 24, 26], 'v_2':[0, 19, 24, 26], 'v_3':[0, 12, 19, 24, 26]}
# Define the voicing dictionaries
chord_voicing = {'maj': maj, 'maj7': maj7, 'm': m, 'm7': m7, 'dom_7': dom_7, 'ø7': ø7, 'o7': o7, 'sus': sus, 'sus7': sus7, 'sus2': sus2}

seq = []

# Replace all char'-' by 'b'4
seq = [x.replace('-', 'b') for x in seq]

# Delete all '<pad>' in the sequence
seq = [x for x in seq if x != '<pad>']

#Fix '7' to 'dom_7' and '7sus' to 'sus7'
for i in range(len(seq) - 1):
    if seq[i] == '7' and seq[i + 1] != 'add 7':
        seq[i] = 'dom_7'
    if seq[i] == '7sus':
        seq[i] = 'sus7'
 
#Fix m6, m9, m11
for i, e in enumerate(seq):
    if e == 'm6':
        seq[i] = 'm'
        seq.insert(i + 1, 'add 6')
    if e == 'm9':
        seq[i] = 'm'
        seq.insert(i + 1, 'add 9')
    if e == 'm11':
        seq[i] = 'm'
        seq.insert(i + 1, 'add 11')
         
    
print(len(seq))

#add major chord token to the sequence
new_sequence = []
for i in range(len(seq)):
    new_sequence.append(seq[i])
    if seq[i] in all_notes and (i == len(seq) - 1 or seq[i + 1] in structural_elements or seq[i + 1].startswith('Form_')):
        new_sequence.append('maj')

seq = new_sequence
#print the sequence
c = 0    
for element in seq:
    if c%10 == 0:
        print('')
    print("'"+element+"'", end=', ')
    c += 1
print('\n')



def convert_song_structure(arr):
    song_info_start = arr.index('<start>') + 1 # skip '<start>'
    song_info_end = arr.index('<end>') # to not include '<end>'
    
    between_repeats = False
    repeat_section = []
    completed_song = []
    
    for elem in arr[song_info_start:song_info_end]:
        if elem == '|:':
            # start of a repeat section
            between_repeats = True
            repeat_section = ['|']
        elif elem == ':|':
            # end of a repeat section
            between_repeats = False
            repeat_section.append('|')
            # repeat the section and append to completed song
            completed_song += repeat_section + repeat_section
            repeat_section = []
        elif between_repeats:
            # within a repeat section
            repeat_section.append(elem)
        else:
            # outside of a repeat section
            completed_song.append(elem)
        
    return completed_song

seq = convert_song_structure(seq)

print("---------------------")
print(len(seq))

#print the sequence
c = 0    
for element in seq:
    if c%10 == 0:
        print('')
    print("'"+element+"'", end=', ')
    c += 1
print('\n')
    
#----------------------------------------------------------
#%%
#run over the sequence, detect if there is a dot and define the base root with the information provided by all_notes, 
# then create the sequence of MIDI notes based on the nature

midi_sequence = []
root = 0
midi = []
durations = []
num_chords = 0
v = 0
pitch = ''
mod = 4

# Create a dictionary for the alter section
add_dict = {
    'add b9': 1 + 12,
    'add 9': 2 + 12,
    'add #9': 3 + 12,
    'add b13': 8 + 12,
    'add 13': 9 + 12,
    'add 6': 9,
    'add #11': 6 + 12,
    'add 2': 2 + 12,
    'add 5': 7,
    'add 7': 11,
    'add 8': 12,
    'add b2': 1,
    'add b6': 8 + 12
}
# Create a dictionary for the alter section
alter_dict = {
    'alter b9': 2,
    'alter #9': 2,
    'alter b5': 7,
    'alter #5': 7,
    'alter #7': 11,
    'alter #11': 11
}


for element in seq:
    if element in ['|', '|:', ':|']:
        num_chords = 0
    elif element == '.':
        num_chords += 1
        durations.append(num_chords)
    elif element in all_notes:
        root = all_notes[element]
        pitch = element
    elif element in natures:
        #random voicing int from 0 to 3
        #n = random.randint(0, 3)
        n = v % mod
        midi = [x + root for x in chord_voicing[element][voicing[n]]]
        print(pitch, element, n)
        midi_sequence.append(midi)
    elif element in add_dict:
        if element in add_dict:
            midi.append(root + add_dict[element])
        for i, n in enumerate(midi):
            diff = (n - root) % 12 
            if (n - root) % 12 == 2 and element.find('9') != -1:
                #delete the note from the midi array
                midi.remove(n)
                
    elif element in alter_dict:
        for i, n in enumerate(midi):
                diff = (n - root) % 12 
                if element.find('b') != -1 and diff == alter_dict[element]:
                    midi[i] = n - 1
                elif element.find('#') != -1 and diff == alter_dict[element]:
                    midi[i] = n + 1
    v += 1
        
#if duration has a 2 then this value and previous one of duration array has the value 0.5 each. If there is a 3 then 0.33 each, if there is a 4 then 0.25 each
for i in range(len(durations)):
    if durations[i] == 2:
        durations[i] = 0.5
        durations[i - 1] = 0.5
    if durations[i] == 3:
        durations[i] = 0.5
        durations[i - 1] = 0.25
        durations[i - 2] = 0.25
    if durations[i] == 4:
        durations[i] = 0.25
        durations[i - 1] = 0.25
        durations[i - 2] = 0.25
        durations[i - 3] = 0.25
        
#print(midi_sequence)
#for m, d in zip(midi_sequence, durations):
#    print(m, d)

#----------------------------------------------------------
from midiutil import MIDIFile

track    = 0
channel  = 0
time     = 0    # In beats
tempo    = 200   # In BPM
volume   = 80  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
MyMIDI.addTempo(track, time, tempo)

time = 0
for m, d in zip(midi_sequence, durations):
    l = d * 4
    for i, pitch in enumerate(m):
        volume = int(random.uniform(55, 85))
        MyMIDI.addNote(track, channel, pitch, time, l, volume)
    time += d*4

fileName = "myFile"
with open(fileName + '.mid', "wb") as output_file:
    MyMIDI.writeFile(output_file)

print(fileName + '.mid', "\nMIDI file created!", )

#play the midi file
   # %%
