# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 09:24:40 2017

@author: bibigul
"""

from appJar import gui
import csv

# create the GUI & set a title
app = gui("Next Word Predictor")

app.setGeom(700, 400)

def nextWords(word):
    #filename = 'exampleTree.csv'
    filename = 'shake_bigrams_successor.csv'
    next_words =['-none-']
    next_words_ind =[]
    this_words=[]
    probabilities=[]
    rows=[]
    i=0
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', dialect='excel') 
        for row in reader:
            rows.append(row)
        for column in range(0, len(rows[0])):
            this_words.append(rows[0][column])
            exec('next_words_ind.append('+rows[1][column]+')')
            exec('probabilities.append('+rows[2][column]+')')

    for i in range(0, len(rows[0])):
        next_words_ind[i] = [next_words_ind[i] for (probabilities[i],next_words_ind[i]) in sorted(zip(probabilities[i],next_words_ind[i]), reverse=True)]
        if len(next_words_ind[i])>3:
            next_words_ind[i] = next_words_ind[i][0:3]
        if this_words[i] == word:
            next_words = [this_words[ind] for ind in next_words_ind[i]]
    if not next_words:
        next_words = ['-Enter starting word-']
    return next_words

def get(btn):
    word =  app.getOptionBox("Options") 
    text =  app.getTextArea("Text") +" "+ word
    app.clearTextArea("Text")
    app.setTextArea("Text", text)
    app.changeOptionBox("Options", nextWords(word))
    app.setEntry("userEnt", word)

    # function to print out the name of the button pressed
# followed by the contents of the two entry boxes

def press(btnName):
    if btnName == "Cancel" or btnName == "End":
        app.stop()
    if app.getTextArea("Text")=="":
        text = app.getEntry("userEnt")
        app.setTextArea("Text", text)
        app.changeOptionBox("Options", nextWords(text))
    else:
        word =  app.getEntry("userEnt")
        text =  app.getTextArea("Text") +" "+ word
        app.clearTextArea("Text")
        app.setTextArea("Text", text)
        app.changeOptionBox("Options", nextWords(word))

# add labels & entries
# in the correct row & column
app.addLabel("userLab", "Type a word:", 0,0)
app.addEntry("userEnt", 0,1)
app.addButton("Submit", press, 0, 2)
app.addLabel("Next words","Possible next words:", 1, 0)
app.addOptionBox("Options", ["Word1", "Word2", "Word3"], 1, 1)
app.addButton("Select", get, 1, 2)
app.addTextArea("Text", 2, 0, 2)
app.addButton("End", press, 2, 2)

# start the GUI
app.go()
