# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 20:36:50 2016

@author: imke
"""

# append current working directory
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import csv
import re
from collections import namedtuple
import numpy as np
import pandas as pd
import argparse


# Parse command line parameters
#parser = argparse.ArgumentParser(description='Parse CSV file and extract unigrams')
#parser.add_argument('filename', default='will_play_text_TEST.csv')
#parser.add_argument('n', default=1)
#print parser.parse_args()


#args = parser.parse_args()
#filename = args.filename
#n = int(args.n)

filename = '/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Shakespeare/will_play_text.csv'
n = 2

# 1 row should look like
# unigram totalcount numberofplays history tragedy  comedy play1 play2...

print filename

comedies = ['The Tempest', 'Two Gentlemen of Verona', 
                'Merry Wives of Windsor', 'Measure for measure', 
                'A Comedy of Errors', 'Much Ado about nothing',
                'Loves Labours Lost', 'A Midsummer nights dream', 
                'Merchant of Venice', 'As you like it', 'Taming of the Shrew',
                'Alls well that ends well', 'Twelfth Night', 'A Winters Tale', 
                'Pericles']
                
tragedies = ['Troilus and Cressida', 'Coriolanus', 'Titus Andronicus', 
                 'Romeo and Juliet', 'Timon of Athens', 'Julius Caesar', 'macbeth',
                 'Hamlet', 'King Lear', 'Othello', 'Antony and Cleopatra',
                 'Cymbeline']
                 
histories = ['King John', 'Richard II', 'Henry IV', 'Henry V', 
                 'Henry VI Part 1', 'Henry VI Part 2', 'Henry VI Part 3',
                 'Richard III', 'Henry VIII' ]
                 
plays = comedies + tragedies + histories
                


def whichCategory(play):
    """
    Return in which category a play is
    """
                
    if (play in comedies):
        return 'Comedy'
    elif (play in tragedies):
        return 'Tragedy'
    elif (play in histories):
        return 'History'
    else:
        raise NameError(['Play not found', play])
# Unigram struct

class Gram:
    def __init__(self, gram):
        self.gram = gram
        self.totalcount = 1
        self.plays = np.zeros(len(plays))
        self.numberofplays = 1
        self.history = 0
        self.tragedy = 0
        self.comedy = 0
        
    def addPlay(self, play):
        if (play in self.plays):
             self.play[plays.index(play)] +=1  
             #self.numberofplays[self.plays.index(play)] += 1
        else:
            #print("~Gram.addPlay: %s is already in the List", %play)
            if whichCategory(currentPlay) == 'History':
                new_gram.history += 1
            elif whichCategory(currentPlay) == 'Tragedy':
                new_gram.tragedy += 1
            elif whichCategory(currentPlay) == 'Comedy':
                new_gram.comedy += 1
            self.numberofplays += 1
        
    def inPlayList(self, play):
        for exPlay in self.playcounts:
            if (play == exPlay):
                return 1
        return 0
        
def write2CSV(n, gram_list):
    print "Starting to write CSV File"
    if (n == 1):
        file = 'shake_unigrams.csv'
        print file
    elif (n == 2):
        file = 'shake_bigrams.csv'
        print file
    
    # Now write the unigrams in a new csv file          
    with open(file, 'wb') as csvfile2:                
        writer = csv.writer(csvfile2, delimiter = "\t") #, dialect='excel')
        print "starting for loop"
        for n_gram in gram_list:
            i = 0
            #writer.writerow([uni.unigram, uni.totalcount)
            if n == 1:
                PlayCount_column = [n_gram.gram, n_gram.totalcount, n_gram.numberofplays]
            elif n == 2:
                PlayCount_column = [n_gram.gram[0], n_gram.gram[1],
                                    n_gram.totalcount]
            #print PlayCount_column
            for play in n_gram.plays:
                PlayCount_column.append(n_gram.category[i])
                PlayCount_column.append(play)
                PlayCount_column.append(n_gram.playcounts[i])
                i += 1
            writer.writerow(PlayCount_column)	
            

# Open CSV file with plays 
#df = pd.read_csv(filename, delimiter=";")
with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', dialect='excel')
    
    
    csv_rows = np.empty([800000, len(plays)+5])
    words = []
    count = 0
    #for indx, row in df.iterrows():
    for row in reader:    
        print row
        if row[3] == '':
            continue
    
        else:
            currentPlay = row[1]
            currentDiag = row[5]
                    
            wordList = re.sub("[^\w]", " ",  currentDiag).split()
            
            #Add a dot to indicate the end of a sentence for bigrams
            if currentDiag.find('.') > 0 and n>1:
                wordList.append('.')
                
            
            if n == 1:
                for word in wordList:
                    
                    if wordList[i] not in words:
                        new_gram = Gram(word)
                        
                        if whichCategory(currentPlay) == 'History':
                            new_gram.history += 1
                        elif whichCategory(currentPlay) == 'Tragedy':
                            new_gram.tragedy += 1
                        elif whichCategory(currentPlay) == 'Comedy':
                            new_gram.comedy += 1
                        
                        new_gram.plays[plays.index(currentPlay)] += 1
                        
    
                        
                        words.append(new_gram.gram)
                        
                        csv_rows[count,0] = new_gram.totalcount
                        csv_rows[count,1] = new_gram.numberofplays
                        csv_rows[count,2] = new_gram.history
                        csv_rows[count,3] = new_gram.tragedy
                        csv_rows[count,4] = new_gram.comedy
                        csv_rows[count,5:csv_rows.shape[1]] = new_gram.plays
                        count += 1
                        
                    else:
                        for i in range(len(words)):
                            
                            if words[i] == word:
                                csv_rows[i,0] += 1
                                
                                if csv_rows[i,plays.index(currentPlay)+5] == 0:
                                    csv_rows[i][1] += 1
                                    
                                csv_rows[i,plays.index(currentPlay)+5] += 1
                                
                                if whichCategory(currentPlay) == 'History':
                                    csv_rows[i,2] += 1
                                elif whichCategory(currentPlay) == 'Tragedy':
                                    csv_rows[i,3] += 1
                                elif whichCategory(currentPlay) == 'Comedy':
                                    csv_rows[i,4] += 1
            else:
                
                for i in range(len(wordList)-1):
                    current_gram = [wordList[i], wordList[i+1]]
                    
                    if current_gram not in words:
                        new_gram = Gram(current_gram)
                        
                        if whichCategory(currentPlay) == 'History':
                            new_gram.history += 1
                        elif whichCategory(currentPlay) == 'Tragedy':
                            new_gram.tragedy += 1
                        elif whichCategory(currentPlay) == 'Comedy':
                            new_gram.comedy += 1
                            
                        new_gram.plays[plays.index(currentPlay)] += 1
                        
                        
                        
                        
                        words.append(new_gram.gram)
                        csv_rows[count,0] = new_gram.totalcount
                        csv_rows[count,1] = new_gram.numberofplays
                        csv_rows[count,2] = new_gram.history
                        csv_rows[count,3] = new_gram.tragedy
                        csv_rows[count,4] = new_gram.comedy
                        csv_rows[count,5:csv_rows.shape[1]] = new_gram.plays
                        count += 1
                                
                    else:
                        for i in range(len(words)):
                            
                            if words[i] == current_gram:
                                csv_rows[i,0] += 1
                                
                                if csv_rows[i,plays.index(currentPlay)+5] == 0:
                                    csv_rows[i][1] += 1
                                    
                                csv_rows[i,plays.index(currentPlay)+5] += 1
                                
                                if whichCategory(currentPlay) == 'History':
                                    csv_rows[i,2] += 1
                                elif whichCategory(currentPlay) == 'Tragedy':
                                    csv_rows[i,3] += 1
                                elif whichCategory(currentPlay) == 'Comedy':
                                    csv_rows[i,4] += 1
                                
                                
words = np.array(words)
data = np.array(csv_rows)

if n == 1:

    gram_df = pd.DataFrame(data=words, columns =["Unigram"])    
    
    gram_df["Totalcount"] = data[0:len(words), 0]
    gram_df["Number of Plays"] = data[0:len(words), 1]
    gram_df["History"] = data[0:len(words), 2]
    gram_df["Tragedy"] = data[0:len(words), 3]
    gram_df["Comedy"] = data[0:len(words), 4]
    for i in range(0,len(plays)):
        gram_df[plays[i]] = data[0:len(words),i+5]
    gram_df.to_csv('/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Shakespeare/shake_unigrams.csv', sep='\t')
else:
    
    gram_df = pd.DataFrame(data=words, columns =["Bigram1", "Bigram2"])    
    
    gram_df["Totalcount"] = data[0:len(words), 0]
    gram_df["Number of Plays"] = data[0:len(words), 1]
    gram_df["History"] = data[0:len(words), 2]
    gram_df["Tragedy"] = data[0:len(words), 3]
    gram_df["Comedy"] = data[0:len(words), 4]
    for i in range(0,len(plays)):
        gram_df[plays[i]] = data[0:len(words),i+5]
    gram_df.to_csv('/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Shakespeare/shake_bigrams.csv', sep='\t')


