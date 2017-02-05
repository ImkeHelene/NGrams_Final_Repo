# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 17:31:39 2017

@author: imke

This script collects some statistics about the Shakespeare plays in order 
to use them to automatically write a play

"""

import csv
import re
import numpy as np
import matplotlib.pyplot as plt


def plot_statistics(k, values, names, y_label, title, avg, filename):
    plt.figure(k)
    y_pos = np.arange(len(names))
    plt.bar(y_pos, values, align='center')
    plt.xticks(y_pos, names, rotation='vertical')
    plt.ylabel(y_label)
    plt.title(title)

    plt.plot(y_pos, np.zeros(len(names)) + avg, '-r', markersize=50)    
    
    plt.legend(['Average'])
    
    plt.savefig(filename + '.pdf')
    

filename = '/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Final_Scripts/will_play_text.csv'


# Parse a list of speakers from all plays
shakespeare_file = '/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Final_Scripts/will_play_text.csv'

speakers=[]
num_words_speakers=[]
num_words_sentence=[0]
num_sentences_speech=[]
speech_count=[]
scene_speakers_count = []

plays = []
scene_count = []
speaker_count = []
speeches_scene_count = []


with open(shakespeare_file, 'rb') as shake_file:
    reader = csv.reader(shake_file, delimiter=';', dialect='excel')
    
    before_speaker = ''
    speech_indx = -1
    for row in reader:
        
        currentPlay = row[1]
        currentSpeaker = row[4]
        currentDiag = row[5] 
        
        
            
                 
        wordList = re.sub("[^\w]", " ",  currentDiag).split()
        
        
        
        # Extract play and scene info
        if currentPlay not in plays:
            plays.append(currentPlay)
            scene_count.append(1)
            speaker_count.append(0)        
        elif currentPlay in plays and 'SCENE' in wordList:
            scene_count[plays.index(currentPlay)] += 1
            scene_speakers_count.append(0)
            speeches_scene_count.append(0)
            
         
        play_indx = plays.index(currentPlay)
        
        if row[3] is not '':
            if currentDiag.find('.') > 0:
                num_words_sentence.append( len( re.sub( "[^\w]", " ",  currentDiag[0:currentDiag.index('.')] ) .split()) )
                num_words_sentence.append(len( re.sub( "[^\w]", " ",  currentDiag[currentDiag.index('.') + 1 : len(currentDiag)] ) .split()))
            else:
                num_words_sentence[-1] += len(wordList)
            # Extract speaker info        
            if currentSpeaker not in speakers:
                speakers.append(row[4])
                #Since each play has different speakers we only increase the count
                # if a new speaker is added
                speaker_count[play_indx] += 1
                num_words_speakers.append(0)
                num_sentences_speech.append(0)
                scene_speakers_count[-1] += 1
                
                if before_speaker is not currentSpeaker:
                    speech_indx += 1
                    num_sentences_speech.append(0)
                    speech_count.append(1)
                    speeches_scene_count[-1] += 1
                    
            else:            
                if before_speaker is not currentSpeaker:
                    speech_indx += 1
                    num_sentences_speech.append(0)
                    speech_count[speakers.index(currentSpeaker)] += 1
                    speeches_scene_count[-1] += 1
             
            # Extract information of speech               
            speaker_indx = speakers.index(currentSpeaker)
            num_words_speakers[speaker_indx] += len(wordList)
            
            # Increase count of sentences by counting the '.'
            if '.' in currentDiag:
                    num_sentences_speech[speech_indx] += 1
                    
                    
        before_speaker = currentSpeaker
        
    
#%%       
avg_num_speakers_per_play = np.mean(speaker_count)
var_num_speakers = speaker_count - avg_num_speakers_per_play
var_range_num_speakers = [np.min(var_num_speakers), np.max(var_num_speakers)]

plot_statistics(1, speaker_count, plays, 'number of speakers', 
                'Speakers in Shakespeare Plays', avg_num_speakers_per_play,
                'SpeakerCount')

print(avg_num_speakers_per_play)
print(var_range_num_speakers)

avg_num_scenes_per_play = np.mean(scene_count)
var_num_scenes_per_play = scene_count - avg_num_scenes_per_play
var_range_num_scenes_per_play = [np.min(var_num_scenes_per_play), np.max(var_num_scenes_per_play)]

plot_statistics(2, scene_count, plays, 'number of scenes', 
                'Number of scenes in Shakespeare Plays', 
                avg_num_scenes_per_play, 'ScenesPlay')

print(avg_num_scenes_per_play)
print(var_range_num_scenes_per_play )

avg_num_words_per_speaker = np.mean(num_words_speakers)
var_num_words_per_speaker = num_words_speakers - avg_num_words_per_speaker
var_range_num_words_per_speaker = [np.min(var_num_words_per_speaker), np.max(var_num_words_per_speaker)]

avg_PLAY_num_words_per_speaker = []
indx = 0
for i in range(0, len(plays)):
    speakers_current_play =[] 
    while len(speakers_current_play) < speaker_count[i]:
        speakers_current_play.append(num_words_speakers[indx])
        indx += 1
    avg_PLAY_num_words_per_speaker.append(np.mean(speakers_current_play))
 
avg_PLAY_avg_num_words_per_speaker = np.mean(avg_PLAY_num_words_per_speaker)   
plot_statistics(3, avg_PLAY_num_words_per_speaker, plays, 
                'average number of words per speaker', 
                'Average Number of Words Per Speaker per Shakespeare Play', 
                avg_PLAY_avg_num_words_per_speaker, 'AvgPLAYWordsPerSpeaker')
#plot_statistics(3, num_words_speakers, Speakers, y_label, title, filename)

print(avg_num_words_per_speaker)
print(var_range_num_words_per_speaker )

avg_num_sentences_per_speech = np.mean(num_sentences_speech)
var_num_sentences_per_speech = num_sentences_speech - avg_num_sentences_per_speech
var_range_num_sentences_per_speech = [np.min(var_num_sentences_per_speech), np.max(var_num_sentences_per_speech)]

print(avg_num_sentences_per_speech)
print(var_range_num_sentences_per_speech)

avg_num_speeches_per_speaker = np.mean(speech_count)
var_num_speeches_per_speaker = speech_count - avg_num_speeches_per_speaker
var_range_num_speeches_per_speaker = [np.min(var_num_speeches_per_speaker), np.max(var_num_speeches_per_speaker)]

avg_PLAY_num_speeches_per_speaker = []
indx = 0
for i in range(0, len(plays)):
    speakers_current_play =[] 
    while len(speakers_current_play) < speaker_count[i]:
        speakers_current_play.append(speech_count[indx])
        indx += 1
    avg_PLAY_num_speeches_per_speaker.append(np.mean(speakers_current_play))
 
avg_PLAY_avg_num_speeches_per_speaker = np.mean(avg_PLAY_num_speeches_per_speaker)   
plot_statistics(4, avg_PLAY_num_speeches_per_speaker, plays, 
                'average number of speeches per speaker', 
                'Average Number of Speeches per Speaker per Shakespeare Play', 
                avg_PLAY_avg_num_speeches_per_speaker, 'AvgPLAYSpeechesPerSpeaker')
    

print(avg_num_speeches_per_speaker)
print(var_range_num_speeches_per_speaker)

avg_num_speakers_per_scene = np.mean(scene_speakers_count)
var_num_speakers_per_scene = scene_speakers_count - avg_num_speakers_per_scene
var_range_speakers_per_scene = [np.min(var_num_speakers_per_scene), np.max(var_num_speakers_per_scene)]
#
#avg_PLAY_num_speakers_per_scene = []
#indx = 0
#for i in range(0, len(plays)):
#    scene_current_play = []
#    while len(scene_current_play) < scene_count[i]:
#        scene_current_play.append(scene_speakers_count[indx])
#        indx += 1
#    avg_PLAY_num_speakers_per_scene.append(np.mean(scene_speakers_count))
#    
#avg_PLAY_avg_num_speakers_per_scene = np.mean(avg_PLAY_num_speakers_per_scene)
#plt_statistics(5, avg_PLAY_num_speakers_per_scene, plays, 
#               'average number of speakers per scene', 
#               'Average Number of Speakers per Scene per Shakespeare Play', 
#               avg_PLAY_avg_num_speakers_per_scene, 'AvgPLAYSpeakersPerScene')
#
#print(avg_num_speakers_per_scene)
#print(var_range_speakers_per_scene)

avg_num_speeches_per_scene = np.mean(speeches_scene_count)
var_num_speeches_per_scene = speeches_scene_count - avg_num_speeches_per_scene
var_range_speeches_per_scene = [np.min(var_num_speeches_per_scene), np.max(var_num_speeches_per_scene)]

print(avg_num_speeches_per_scene)
print(var_range_speeches_per_scene)

avg_num_words_per_sentence = np.mean(num_words_sentence)
var_num_words_per_sentence = num_words_sentence - avg_num_words_per_sentence
var_range_words_per_sentence = [np.min(var_num_words_per_sentence), np.max(var_num_words_per_sentence)]

print(avg_num_words_per_sentence)
print(var_range_words_per_sentence)
            