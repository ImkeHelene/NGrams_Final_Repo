# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:24:08 2016

@author: imke
"""
#Append pwd to sys.path
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))


import pandas as pd
from nltk.corpus import stopwords
import math
import csv
import numpy as np
count_per_volume = []
lower_count=[]
lower_volumecount=[]
upper_count=[]
upper_volumecount=[]
mixed_count=[]
mixed_volumecount=[]        
known_grams = []
indices = []

def extendStopwords(stpwds):
        # Append Names of speakers to stopword list
    with open(os.getcwd() + '/will_play_text.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', dialect='excel')
             
        for row in reader:
            if row[4].lower() not in stpwds:
                if (row[4].lower().find('all') == -1 and row[4].lower().find('first') == -1 
                and row[4].lower().find('second')==-1 and row[4].lower().find('third') == -1
                and row[4].lower().find('fourth')== -1 and row[4].lower().find('fifth')== -1
                and row[4].lower().find('some') == -1):
                    #print row[4]
                    stpwds.append(row[4].lower())  

class Clean_NGrams:

    #Constructor
    def __init__(self, max_count,row_count, words = None): #stopwords):
        #self.filename = filename
        #self.dataframe = pd.read_csv(filename, delim_whitespace=True, header = None)
        self.dictionary = pd.read_csv('words3.txt', delimiter = "\n")
        self.clean_count = 0
        if words == None:
            self.stpwds = stopwords.words('english')
        else:
            self.stpwds = words

        
        #self.threshold = row_count / max_count
        self.threshold = 500
	print("Threshold is " + str(self.threshold))
        self.drop = 0
        self.row = []
        
        
    def rough(self, indx, row, gram): 
        #Stopword list as input???
        # Do rough cleaning of the dataset in csv_file
        # Clean out words without vowls:
        self.drop = 0
        # Clean out words from stopwordlist <- member or input??:
        if (row[len(gram) + 1] in self.stpwds 
            or float(row[len(gram)+1]) > self.threshold 
            or row[len(gram) + 1] not in self.dictionary):
            self.drop = 1
            self.clean_count += 1
        else:
            self.drop = 0
        
    def types(self, indx, gram):
        # split types from the gram and add in a new column.
        # expects gram to be a list of length 1 or 2

        # Access to rows and columns: self.csv_frame.iloc[rows, columns]
        self.row = []
        
        for i in range(0,len(gram)):
            if gram[i].find('_') > 0:
                self.row.append(gram[i][0:gram[i].find('_')])
                self.row.append(gram[i][gram[i].find('_'):len(gram[i])])
                self._append_row()
            else: 
                self.row.append(gram[i])
                self.row.append('')
                self._append_row()
      
            
    def _append_row(self): 
        
        if (self.drop == 0):    
            self.row.append(row[1])
            self.row.append(float(row[2]) / float(row[3]) )
    
            
    

    def finalize(self):
        #self.csv_frame.save
        self.clean_count = 100.0 * (self.clean_count / row_count)
    	print("cleaned out " + str(100.0 * (self.clean_count)))
        #self.dataframe.to_csv(['/Cleaned_' + self.filename] , sep = '\t')
        

# These tables match the interesting words picked.
# Downloading all bigrams / unigrams takes quite a long time.

#frame = pd.read_csv(, delim_whitespace=True, header=None)
file_list = ['/googlebooks-eng-gb-all-2gram-20120701-sh', '/googlebooks-eng-gb-all-2gram-20120701-lo',
             '/googlebooks-eng-gb-all-2gram-20120701-ma', '/googlebooks-eng-gb-all-2gram-20120701-wo',
             '/googlebooks-eng-gb-all-2gram-20120701-go', '/googlebooks-eng-gb-all-2gram-20120701-en']
Cleaned_out = []
for fname in file_list:

    fname = os.getcwd() + fname
    print('Reading file ' + fname)
    #pd_df = pd.read_csv(fname, delimiter='\t', header=None)
    #pd_df.to_csv(fname + '_CSV.csv' , sep = '\t')
    
    with open(fname, 'rb') as csvfile:
        row_count = len(csvfile.readlines())
    
    print('It has in total ' + str(row_count) + ' rows')
        
    with open(fname, 'rb') as csvfile:
        
        reader = csv.reader(csvfile, delimiter='\t', dialect='excel')
       
        max_count = 0
        indx = -1
        progress0 = -1
        print("Finding Max count")
        for row in reader:
            indx += 1
            progress = np.floor(100.0 * float(indx) / float(row_count))
            #print("GOING THROUGH FILE")
            #print row
            if float(row[2]) / float(row[3]) > max_count:
                max_count = float(row[2]) / float(row[3])
                
            if ( progress in [0.0,25.0,50.0,75.0,100.0]) and progress <> progress0:
                print('At ' + str(np.floor(100.0 * (float(indx) / float(row_count)))) + ' percent')
                progress0 = progress
            
       
    #max_count = 5592.5            
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', dialect='excel')
    #    
       # max_count = float(max_count)
        #max_count = 5509611.0
        #max_count = 1000000.0
        print ("Max Count is " + str(max_count) )
        
        print("Start the cleaning process")
        
        with open(fname + '_Cleaned' ,'wb') as writefile:
            writer = csv.writer(writefile, delimiter= '\t', dialect='excel')
            Cleaner = Clean_NGrams(max_count, row_count)
            indx = -1
            progress0 = -1
            for row in reader:
                indx += 1
                progress = np.floor(100.0 * float(indx) / float(row_count))
                if ( progress in range(0,100,10) and progress <> progress0):
                    print('Looking at row ' + str(indx )+ str(np.floor(100.0 * float(indx) / float(row_count))) + 'percent done')
                    progress0 = progress
                    
                Cleaner.rough(indx, row, [row[0], row[1]])
                if Cleaner.drop == 1:
                    continue
                else:
                    Cleaner.types(indx, [row[0], row[1]])  
                    print(Cleaner.row)                     
                    writer.writerow(Cleaner.row)
        
            Cleaned_out.append(Cleaner.clean_count) 
    
            
        print ("Done! Cleaned out " + str((float(Cleaner.clean_count)/float(row_count)) * 100.0))
        
print('Totally done! In average ' + np.mean(Cleaned_out) + 'Percent of lines were cleaned out!')
