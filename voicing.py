#%%
import random
#Extract m11, m9, m6 and add maj in the dataset, 
# change 7 by dom_7, change 7sus by sus7
natures = ['maj','7sus', 'm', 'm11', 'm6', 'm7', 'm9', 'dom_7', 'maj7', 'o7', 'sus', 'sus2', 'ø7']

structural_elements = ['.', '|', ':|', '/', '|:']

all_notes = {
    'C': 48, 'C#': 49, 'Db': 49, 'D': 50, 'D#': 51, 'Eb': 51, 'E': 52, 'F': 53, 'F#': 54, 'Gb': 42, 'G': 43, 'G#': 44, 'Ab':44, 'A': 45, 'A#': 46, 'Bb': 46, 'B': 47, 
    'A##': 47, 'Abb': 43, 'Abbb': 42, 'B#': 48, 'B##': 49, 'Bbb': 45, 'Bbbb': 44, 
    'C#': 49, 'C##': 50, 'C###': 51, 'Cb': 59, 'Cbb': 58, 'D##': 52, 'Dbb': 48, 'Dbbb': 47, 'E##': 54, 'Ebb': 50, 'Ebbb': 49, 
    'F##': 55, 'F###': 56, 'Fb': 52, 'Fbb': 51, 'G##': 45, 'Gb': 42, 'Gbb': 41
    }

#define voicing for natures
maj = {'v_0':[0, 12, 16, 19], 'v_1':[0, 7, 12, 16], 'v_2':[0, 4, 7, 12], 'v_3':[0, 7, 16, 19]}
maj7 = {'v_0':[0, 12, 16, 19, 23], 'v_1':[0, 11, 16, 19], 'v_2':[0, 11, 14, 16], 'v_3':[0, 11, 14, 16, 19]}
m = {'v_0':[0, 12, 15, 19], 'v_1':[0, 15, 19, 24], 'v_2':[0, 19, 24, 27], 'v_3':[0, 12, 19, 24, 27]}



m7 = {'v_0':[0, 12, 15, 19, 22], 'v_1':[0, 10, 15, 19], 'v_2':[0, 10, 14, 15], 'v_3':[0, 10, 14, 15, 19]}



dom_7 = {'v_0':[0, 12, 16, 19, 22], 'v_1':[0, 10, 16, 19], 'v_2':[0, 10, 14, 16], 'v_3':[0, 10, 14, 16, 19]}
ø7 =  {'v_0':[0, 12, 15, 18, 22], 'v_1':[0, 10, 15, 18], 'v_2':[0, 15, 18, 22, 24], 'v_3':[0, 6, 10, 15, 18]}
o7 = {'v_0':[0, 12, 15, 18, 21], 'v_1':[0, 15, 18, 21, 24], 'v_2':[0, 18, 21, 24, 27], 'v_3':[0, 12, 15, 18, 21]}
sus = {'v_0':[0, 12, 17, 19], 'v_1':[0, 17, 19, 24], 'v_2':[0, 19, 24, 29], 'v_3':[0, 12, 19, 24, 29]} 
sus7 = {'v_0':[0, 12, 17, 19, 22], 'v_1':[0, 10, 17, 19], 'v_2':[0, 10, 14, 17], 'v_3':[0, 10, 14, 17, 19]}
sus2 = {'v_0':[0, 12, 14, 19], 'v_1':[0, 14, 19, 24], 'v_2':[0, 19, 24, 26], 'v_3':[0, 12, 19, 24, 26]}
# Define the voicing dictionaries
chord_voicings = {'maj': maj, 'maj7': maj7, 'm': m, 'm7': m7, 'dom_7': dom_7, 'ø7': ø7, 'o7': o7, 'sus': sus, 'sus7': sus7, 'sus2': sus2}

voicing = ['v_0', 'v_1', 'v_2', 'v_3']

samba = ['<start>', '<style>', 'Samba', '|:', '.', 'A#', '6', 'add 9', 'alter b5', '.', 'C#', '7', 'add 9', 'alter #5', '|', 
       '.', 'A#', '6', 'add 9', 'alter b5', '.', 'C#', '7', 'add 9', 'alter #5', '|', 
       '.', 'A#', '6', 'add 9', 'alter b5', '.', 'C#', '7', 'add 9', 'alter #5', '|', 'Repeat_1', 
       '.', 'A#', '6', 'add 9', 'alter b5', '.', 'C#', '7', 'add 9', 'alter #5', '|', 'Repeat_2', '.', 'A#', 'add 9', 'add 6', 
       '.', 'F#', '7', '.', 'A-', '7', '|', '.', 'E-', 'm7', '.', 'G#', '|', '.', 'A-', 'm7', 'alter b5', '.', 'E-', '7', '|', 
       '.', 'B-', '9', '.', 'C#', '7', '|', '.', 'A#', '6', 'add 9', 'alter b5', '.', 'A-', '7', 'add 9', 'alter #5', '|', 
       '.', 'E-', 'm7', '.', 'G#', '|', '.', 'A-', 'm7', 'alter b5', '|', '.', 'A-', 'm7', 'alter b5', '|', '.', 'E-', '7', '|', 
       '.', 'B-', '9', '.', 'C#', '7', '|', '.', 'G#', '6', '/', 'B', '.', 'F#', 'm6', '|', '.', 'G#', '6', '/', 'B', '.', 'F#', 'm6', '|', 
       '.', 'C#', 'm6', '.', 'A#', '9', '|', '.', 'F#', 'maj7', '.', 'A-', '7', 'alter #5', '|', '.', 'E-', '7sus', 'add b9', 
       '.', 'E-', '7', '|', '.', 'B-', '9', '.', 'C#', '7', '|', '.', 'A#', 'add 9', 'add 6', '.', 'C#', '13', '|:', 
       '.', 'A#', 'add 9', 'add 6', '.', 'B', '|', 'Form_B', '.', 'A#', 'add 9', 'add 6', '|', '.', 'A#', 'add 9', 'add 6', 
       '.', 'C', '|', '.', 'B-', 'm7', '|', '.', 'C#', '7', '|', '.', 'B-', 'm7', '|', '.', 'C#', '7', '|', 
       '.', 'D-', 'm7', 'alter b5', '.', 'A-', '7', '|', '.', 'E-', '7', '|', '.', 'E-', '7', '|', '.', 'E-', '7', '.', 'D#', '|', 
       '.', 'C##', 'm7', '/', 'G#', '|', '.', 'E#', 'm6', '/', 'G#', '|', '.', 'E-', '7', '|', '.', 'B-', '9', 
       '.', 'C#', '7', '|', 'Repeat_1', '.', 'A#', '6', 'add 9', 'alter b5', '.', 'A-', '7', 'add 9', 'alter #5', '|', 'Repeat_3', 
       '.', 'A#', '6', 'add 9', 'alter b5', '.', 'C#', '7', 'add 9', 'alter #5', '<end>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', 
       '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>']

stella = ['<start>', '<style>', 'Jazz', '|', 'Form_A', '.', 'E', 'm7', 
'alter b5', '|', '.', 'A', '7', 'add b9', '|', '.', 
'C', 'm7', '|', '.', 'F', '7', '|', '.', 
'F', 'm7', '|', '.', 'B-', '7', '|', '.', 
'E-', 'maj7', '|', '.', 'A-', '7', '|', '.', 
'B-', 'maj7', '|', '.', 'E', 'm7', 'alter b5', 'add b9', 
'.', 'A', '7', 'alter b5', 'add b9', '|', '.', 'D', 
'm7', '|', '.', 'B-', 'm7', '.', 'E-', '7', 
'|', '.', 'F', 'maj7', '|', '.', 'E', 'm7', 
'alter b5', '|', '.', 'E-', 'maj7', 'add #11', '|', '.', 
'D', '7', 'add b9', '|', 'Form_B', '.', 'G', '7', 
'add b13', '|', '.', 'G', '7', 'add b13', '|', '.', 
'C', 'm7', '|', '.', 'C', 'm7', '|', '.', 
'A-', '7', 'add #11', '|', '.', 'A-', '7', 'add #11', 
'|', '.', 'B-', 'maj7', '|', '.', 'B-', 'maj7', 
'|', 'Form_C', '.', 'E', 'm7', 'alter b5', '|', '.', 
'A', '7', 'add b9', '|', '.', 'D', 'm7', 'alter b5', 
'|', '.', 'G', '7', 'add b9', '|', '.', 'C', 
'm7', 'alter b5', '|', '.', 'F', '7', 'add b9', '|', 
'.', 'B-', 'maj7', '|', '.', 'B-', 'maj7', '<end>', 
'<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>', '<pad>',]

seq = stella
# Replace all char'-' by 'b'4
seq = [x.replace('-', 'b') for x in seq]

# Delete all '<pad>' in the sequence
seq = [x for x in seq if x != '<pad>']

for i in range(len(seq) - 1):
    if seq[i] == '7' and seq[i + 1] != 'add 7':
        seq[i] = 'dom_7'
    
print(len(seq))

#add major chord token to the sequence
new_sequence = []
for i in range(len(seq)):
    new_sequence.append(seq[i])
    if seq[i] in all_notes and (i == len(seq) - 1 or seq[i + 1] in structural_elements or seq[i + 1].startswith('Form_')):
        new_sequence.append('maj')

c = 0    
for element in new_sequence:
    if c%10 == 0:
        print('\n')
    print("'"+element+"'", end=', ')
    c += 1
#%%
#run over the sequence, detect if there is a dot and define the base root with the information provided by all_notes, 
# then create the sequence of MIDI notes based on the nature


midi_sequence = []
root = 0
midi = []
durations = []
num_chords = 0

for i in range(len(new_sequence)):
    #print(new_sequence[i])
    element = new_sequence[i]
    if element in ['|', '|:', ':|']:
        num_chords = 0
    if element == '.':
        #print('.')
        num_chords += 1
        durations.append(num_chords)
        print(num_chords)
    if element in all_notes:
        root = all_notes[element]
        print(root)
    if element in natures:
        midi = [x + root for x in chord_voicings[element][voicing[random.randint(0, 3)]]]
        print(midi)
        midi_sequence.append(midi)
        
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
for m, d in zip(midi_sequence, durations):
    print(m, d)

#add the additions and alteration into the midi array

#----------------------------------------------------------
# %%
from midiutil import MIDIFile

track    = 0
channel  = 0
time     = 0    # In beats
tempo    = 120   # In BPM
volume   = 80  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
MyMIDI.addTempo(track, time, tempo)

time = 0
for m, d in zip(midi_sequence, durations):
    l = d * 4
    for i, pitch in enumerate(m):
        MyMIDI.addNote(track, channel, pitch, time, l, volume)
    time += d*4
    print(time)
    
with open("mySong.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
# %%
