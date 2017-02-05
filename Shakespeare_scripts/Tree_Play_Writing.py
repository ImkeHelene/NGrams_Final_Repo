# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 16:22:19 2017

@author: imke
"""

import os

import random
import pickle
import csv
import copy

import numpy as np
import math

class bigram_tree_node:
    
    def __init__(self, parent, first, node_index):
        self.first = first
        self.index = node_index
        self.probabilities = []
        self.parent = parent       
        #private
        self.children = []
        

    def add_child(self, index):
        
        # Do not add children to sentence end node.
        if index == sentence_end_node.index:
            raise ValueError('Adding child to sentence end node')
            
        self.children.append(index)
        # Once a child is added, it appeared as successor of the parent
        # one time
        self.probabilities.append(1)
        
    def get_child(self, child_first):
        """
        Returns the index in self.children of the child with name child_first
        if child_first is not a child of self, it returns -100
        """
        count = 0
        for i in self.children:
            # If child_first is found in children list, it is a child
            # return the corresponding node
            if first_list[i] == child_first:
                return count
            count += 1
        # If not returned in the for loop, there is no child with first 
        # child_first -> return None
        return None
            
        
    def get_node(self, first):
        """
        Return the index of the node with first first.
        Returns -100 if the first is not found in first_list
        """

        if first in first_list:
            return first_list.index(first)
        else:
            return None
            
        
filename = '/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Shakespeare/shake_bigrams.csv'

### Establish the tree

# The root node will be the beginning of sentence dummy
root_node = bigram_tree_node(None, None, 0) 
# The end of sentence node will only have the root_node as a child
sentence_end_node = bigram_tree_node(None, '.', -1)  

first_list = ['ROOOOOOT']
node_list = [root_node]

  
print('Creating the tree')  
with open(filename, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', dialect='excel')
    
    # Initialize auxilary nodes for the loop
    index = 1
    row_count = 0
    parent = first_list[0]
    for row in reader:
        # Skip first row -> description of columns
        if row_count == 0:
            row_count += 1
            continue
        else:

            if row[1] not in first_list:
                print('adding Node ' + row[1])
                first_list.append(row[1])
                node_list.append(bigram_tree_node(first_list.index(parent), row[1], index))
                node_list[first_list.index(parent)].add_child(index)               
                index +=1
                
            else:
                # If row[1] is already a key in the tree, we need to increase the
                # probability count.
                local_child_index = node_list[first_list.index(parent)].get_child(row[1])#
                if local_child_index  == None:
                    node_list[first_list.index(parent)].add_child(first_list.index(row[1]))
                else: 
                    print(parent)
                    node_list[first_list.index(parent)].probabilities[local_child_index] += 1
                    
                
            
            # For the next bigram the parent will either be the beginning of 
            # sentence dummy or the current node.
            if row[2] == '.':
                # Add . to first_list the first time it appears.
                if row[2] not in first_list:
                    first_list.append(row[2])
                    node_list.append(bigram_tree_node(len(first_list)-1, row[2], index))
                    node_list[-2].add_child(index)
                    index += 1
                    
                node_list[first_list.index(row[1])].add_child(first_list.index('.'))
                parent = first_list[0]
            else:
                parent = first_list[-1]

print('Done creating the tree')      
#%%

### Parse tree to write play

avg_num_speakers_per_play = 26
var_range_num_speakers = range(-17, 26)

avg_num_scenes_per_play = 21
var_range_num_scenes_per_play = range(-11, 23)

avg_num_words_per_speaker = 868
var_range_num_words_per_speaker = range(-867, 13289)

avg_num_sentences_per_speech = 1
var_range_num_sentences_per_speech = range(0, 2)

avg_num_speeches_per_speaker = 112
var_range_num_speeches_per_speaker = range(-111, 1700)

avg_num_speakers_per_scene = 2
var_range_num_speakers_per_scene = range(0, 11)

avg_num_speeches_per_scene = 15
var_range_num_speeches_per_scene = range(-10, 36)

avg_num_words_per_sentence = 13
var_range_num_words_per_sentence = range(-11, 20)

roman_numbers = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII',
                 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'IXX', 'XX', 'XXI']

speakers = ['KING HENRY IV', 'WESTMORELAND', 'FALSTAFF', 'PRINCE HENRY', 'POINS', 'EARL OF WORCESTER', 'NORTHUMBERLAND', 'HOTSPUR', 'SIR WALTER BLUNT', 'First Carrier', 'Ostler', 'Second Carrier', 'GADSHILL', 'Chamberlain', 'BARDOLPH', 'PETO', 'First Traveller', 'Thieves', 'Travellers', 'LADY PERCY', 'Servant', 'FRANCIS', 'Vintner', 'Hostess', 'Sheriff', 'Carrier', 'MORTIMER', 'GLENDOWER', 'EARL OF DOUGLAS', 'Messenger', 'VERNON', 'WORCESTER', 'ARCHBISHOP OF YORK', 'SIR MICHAEL', 'LANCASTER', 'BEDFORD', 'GLOUCESTER', 'EXETER', 'OF WINCHESTER', 'CHARLES', 'ALENCON', 'REIGNIER', 'BASTARD OF ORLEANS', 'JOAN LA PUCELLE', 'First Warder', 'Second Warder', 'WOODVILE', 'Mayor', 'Officer', 'Boy', 'SALISBURY', 'TALBOT', 'GARGRAVE', 'GLANSDALE', 'Sergeant', 'First Sentinel', 'BURGUNDY', 'Sentinels', 'Soldier', 'Captain', 'OF AUVERGNE', 'Porter', 'PLANTAGENET', 'SUFFOLK', 'SOMERSET', 'WARWICK', 'Lawyer', 'First Gaoler', 'KING HENRY VI', 'ALL', 'First Soldier', 'Watch', 'FASTOLFE', 'BASSET', 'YORK', 'General', 'LUCY', 'JOHN TALBOT', 'Legate', 'Scout', 'MARGARET', 'SU FFOLK', 'Shepherd', 'QUEEN MARGARET', 'CARDINAL', 'BUCKINGHAM', 'DUCHESS', 'HUME', 'First Petitioner', 'Second Petitioner', 'PETER', 'HORNER', 'BOLINGBROKE', 'Spirit', 'MARGARET JOURDAIN', 'Townsman', 'SIMPCOX', 'Wife', 'Beadle', 'BOTH', 'First Neighbour', 'Second Neighbour', 'Third Neighbour', 'Servants', 'Herald', 'STANLEY', 'Post', 'First Murderer', 'Second Murderer', 'First Murder', 'Commons', 'VAUX', 'First Gentleman', 'Master', 'Second Gentleman', 'WHITMORE', 'BEVIS', 'HOLLAND', 'CADE', 'DICK', 'SMITH', 'Clerk', 'CLERK', 'MICHAEL', 'SIR HUMPHREY', 'WILLIAM STAFFORD', 'SAY', 'SCALES', 'First Citizen', 'CLIFFORD', 'IDEN', 'EDWARD', 'RICHARD', 'YOUNG CLIFFORD', 'MONTAGUE', 'NORFOLK', 'PRINCE EDWARD', 'JOHN MORTIMER', 'RUTLAND', 'Tutor', 'PRINCE', 'GEORGE', 'Son', 'Father', 'First Keeper', 'Second Keeper', 'KING EDWARD IV', 'CLARENCE', 'LADY GREY', 'Nobleman', 'KING LEWIS XI', 'OXFORD', 'BONA', 'HASTINGS', 'QUEEN ELIZABETH', 'First Watchman', 'Second Watchman', 'Third Watchman', 'RIVERS', 'Huntsman', 'Lieutenant', 'All', 'First Messenger', 'Second Messenger', 'COUNTESS', 'BERTRAM', 'LAFEU', 'HELENA', 'PAROLLES', 'Page', 'KING', 'First Lord', 'Second Lord', 'Steward', 'Clown', 'Both', 'Fourth Lord', 'DUKE', 'Widow', 'DIANA', 'MARIANA', 'Second Soldier', 'Gentleman', 'ORLANDO', 'ADAM', 'OLIVER', 'DENNIS', 'CELIA', 'ROSALIND', 'TOUCHSTONE', 'LE BEAU', 'DUKE FREDERICK', 'DUKE SENIOR', 'AMIENS', 'CORIN', 'SILVIUS', 'JAQUES', 'AUDREY', 'SIR OLIVER MARTEXT', 'PHEBE', 'A Lord', 'Forester', 'WILLIAM', 'First Page', 'Second Page', 'HYMEN', 'JAQUES DE BOYS', 'PHILO', 'CLEOPATRA', 'MARK ANTONY', 'Attendant', 'DEMETRIUS', 'CHARMIAN', 'ALEXAS', 'Soothsayer', 'DOMITIUS ENOBARBUS', 'IRAS', 'First Attendant', 'Second Attendant', 'OCTAVIUS CAESAR', 'LEPIDUS', 'MARDIAN', 'POMPEY', 'MENECRATES', 'MENAS', 'VARRIUS', 'MECAENAS', 'AGRIPPA', 'OCTAVIA', 'Attendants', 'First Servant', 'Second Servant', 'VENTIDIUS', 'SILIUS', 'EROS', 'CANIDIUS', 'TAURUS', 'SCARUS', 'DOLABELLA', 'EUPHRONIUS', 'THYREUS', 'Third Soldier', 'Fourth Soldier', 'First Guard', 'Second Guard', 'Third Guard', 'DERCETAS', 'DIOMEDES', 'Egyptian', 'PROCULEIUS', 'GALLUS', 'SELEUCUS', 'Guard', 'AEGEON', 'DUKE SOLINUS', 'Gaoler', 'First Merchant', 'OF SYRACUSE', 'DROMIO OF SYRACUSE', 'DROMIO OF EPHESUS', 'ADRIANA', 'LUCIANA', 'OF EPHESUS', 'BALTHAZAR', 'LUCE', 'ANTIPHOLUS', 'ANGELO', 'Second Merchant', 'Courtezan', 'PINCH', 'AEMELIA', 'Second Citizen', 'MENENIUS', 'MARCIUS', 'First Senator', 'COMINIUS', 'TITUS', 'SICINIUS', 'BRUTUS', 'AUFIDIUS', 'Second Senator', 'VOLUMNIA', 'VIRGILIA', 'Gentlewoman', 'VALERIA', 'LARTIUS', 'First Roman', 'Second Roman', 'Third Roman', 'CORIOLANUS', 'First Officer', 'Second Officer', 'Senators', 'Third Citizen', 'Fourth Citizen', 'Fifth Citizen', 'Both Citizens', 'Sixth Citizen', 'Seventh Citizen', 'All Citizens', 'Citizens', 'AEdile', 'A Patrician', 'Second Patrician', 'Both Tribunes', 'Roman', 'Volsce', 'Citizen', 'First Servingman', 'Second Servingman', 'Third Servingman', 'Young MARCIUS', 'First Conspirator', 'Second Conspirator', 'Third Conspirator', 'All The Lords', 'Lords', 'All Conspirators', 'All The People', 'Third Lord', 'QUEEN', 'POSTHUMUS LEONATUS', 'IMOGEN', 'CYMBELINE', 'PISANIO', 'CLOTEN', 'Lady', 'IACHIMO', 'PHILARIO', 'Frenchman', 'First Lady', 'CORNELIUS', '', 'CAIUS LUCIUS', 'BELARIUS', 'GUIDERIUS', 'ARVIRAGUS', 'First Tribune', 'Lord', 'First Captain', 'Second Captain', 'Second Gaoler', 'Sicilius Leonatus', 'Mother', 'First Brother', 'Second Brother', 'Jupiter', 'Posthumus Leonatus', 'BERNARDO', 'FRANCISCO', 'HORATIO', 'MARCELLUS', 'KING CLAUDIUS', 'VOLTIMAND', 'LAERTES', 'LORD POLONIUS', 'HAMLET', 'QUEEN GERTRUDE', 'OPHELIA', 'Ghost', 'REYNALDO', 'ROSENCRANTZ', 'GUILDENSTERN', 'First Player', 'Prologue', 'Player King', 'Player Queen', 'LUCIANUS', 'PRINCE FORTINBRAS', 'Danes', 'First Sailor', 'First Clown', 'Second Clown', 'First Priest', 'OSRIC', 'First Ambassador', 'Chorus', 'CANTERBURY', 'ELY', 'KING HENRY V', 'NYM', 'PISTOL', 'SCROOP', 'CAMBRIDGE', 'GREY', 'KING OF FRANCE', 'DAUPHIN', 'Constable', 'FLUELLEN', 'GOWER', 'JAMY', 'MACMORRIS', 'GOVERNOR', 'KATHARINE', 'ALICE', 'BOURBON', 'MONTJOY', 'ORLEANS', 'RAMBURES', 'ERPINGHAM', 'COURT', 'BATES', 'WILLIAMS', 'GRANDPRE', 'French Soldier', 'QUEEN ISABEL', 'FRENCH KING', 'ABERGAVENNY', 'CARDINAL WOLSEY', 'First Secretary', 'BRANDON', 'KING HENRY VIII', 'QUEEN KATHARINE', 'Surveyor', 'SANDS', 'LOVELL', 'GUILDFORD', 'ANNE', 'CARDINAL CAMPEIUS', 'GARDINER', 'Old Lady', 'Scribe', 'Crier', 'GRIFFITH', 'LINCOLN', 'SURREY', 'CROMWELL', 'Third Gentleman', 'PATIENCE', 'CAPUCIUS', 'DENNY', 'CRANMER', 'Keeper', 'DOCTOR BUTTS', 'Chancellor', 'Man', 'Garter', 'KING JOHN', 'CHATILLON', 'QUEEN ELINOR', 'ESSEX', 'BASTARD', 'ROBERT', 'LADY FAULCONBRIDGE', 'GURNEY', 'LEWIS', 'ARTHUR', 'AUSTRIA', 'CONSTANCE', 'KING PHILIP', 'BLANCH', 'French Herald', 'English Herald', 'CARDINAL PANDULPH', 'ELINOR', 'HUBERT', 'First Executioner', 'PEMBROKE', 'BIGOT', 'MELUN', 'FLAVIUS', 'First Commoner', 'MARULLUS', 'Second Commoner', 'CAESAR', 'CASCA', 'CALPURNIA', 'ANTONY', 'CASSIUS', 'CICERO', 'CINNA', 'LUCIUS', 'DECIUS BRUTUS', 'METELLUS CIMBER', 'TREBONIUS', 'PORTIA', 'LIGARIUS', 'PUBLIUS', 'ARTEMIDORUS', 'POPILIUS', 'Several Citizens', 'CINNA THE POET', 'OCTAVIUS', 'LUCILIUS', 'PINDARUS', 'Poet', 'MESSALA', 'VARRO', 'GHOST', 'CLAUDIUS', 'TITINIUS', 'CATO', 'CLITUS', 'DARDANIUS', 'VOLUMNIUS', 'STRATO', 'KENT', 'EDMUND', 'KING LEAR', 'GONERIL', 'CORDELIA', 'LEAR', 'REGAN', 'CORNWALL', 'EDGAR', 'OSWALD', 'Knight', 'Fool', 'ALBANY', 'CURAN', 'Third Servant', 'Old Man', 'Doctor', 'FERDINAND', 'LONGAVILLE', 'DUMAIN', 'BIRON', 'DULL', 'COSTARD', 'ADRIANO DE ARMADO', 'MOTH', 'ARMADO', 'JAQUENETTA', 'BOYET', 'PRINCESS', 'MARIA', 'ROSALINE', 'SIR NATHANIEL', 'HOLOFERNES', 'MERCADE', 'First Witch', 'Second Witch', 'Third Witch', 'DUNCAN', 'MALCOLM', 'LENNOX', 'ROSS', 'MACBETH', 'BANQUO', 'ANGUS', 'LADY MACBETH', 'FLEANCE', 'MACDUFF', 'DONALBAIN', 'ATTENDANT', 'Both Murderers', 'Third Murderer', 'HECATE', 'First Apparition', 'Second Apparition', 'Third Apparition', 'LADY MACDUFF', 'MENTEITH', 'CAITHNESS', 'SEYTON', 'SIWARD', 'Soldiers', 'YOUNG SIWARD', 'DUKE VINCENTIO', 'ESCALUS', 'LUCIO', 'MISTRESS OVERDONE', 'CLAUDIO', 'Provost', 'FRIAR THOMAS', 'ISABELLA', 'FRANCISCA', 'ELBOW', 'FROTH', 'POMPHEY', 'Justice', 'JULIET', 'ABHORSON', 'BARNARDINE', 'FRIAR PETER', 'ANTONIO', 'SALARINO', 'SALANIO', 'BASSANIO', 'LORENZO', 'GRATIANO', 'NERISSA', 'SHYLOCK', 'MOROCCO', 'LAUNCELOT', 'GOBBO', 'LEONARDO', 'JESSICA', 'ARRAGON', 'TUBAL', 'SALERIO', 'BALTHASAR', 'STEPHANO', 'SHALLOW', 'SLENDER', 'SIR HUGH EVANS', 'PAGE', 'SIMPLE', 'ANNE PAGE', 'Host', 'MISTRESS QUICKLY', 'RUGBY', 'DOCTOR CAIUS', 'FENTON', 'MISTRESS PAGE', 'MISTRESS FORD', 'FORD', 'ROBIN', 'WILLIAM PAGE', 'THESEUS', 'HIPPOLYTA', 'EGEUS', 'HERMIA', 'LYSANDER', 'QUINCE', 'BOTTOM', 'FLUTE', 'STARVELING', 'SNOUT', 'SNUG', 'PUCK', 'Fairy', 'OBERON', 'TITANIA', 'PEASEBLOSSOM', 'COBWEB', 'MUSTARDSEED', 'HERNIA', 'PHILOSTRATE', 'Wall', 'Pyramus', 'Thisbe', 'Lion', 'Moonshine', 'LEONATO', 'BEATRICE', 'HERO', 'DON PEDRO', 'BENEDICK', 'DON JOHN', 'CONRADE', 'BORACHIO', 'URSULA', 'DOGBERRY', 'VERGES', 'Watchman', 'FRIAR FRANCIS', 'Sexton', 'RODERIGO', 'IAGO', 'BRABANTIO', 'OTHELLO', 'CASSIO', 'DUKE OF VENICE', 'Sailor', 'Senator', 'DESDEMONA', 'MONTANO', 'Fourth Gentleman', 'Second Gentlemen', 'EMILIA', 'First Musician', 'BIANCA', 'LODOVICO', 'ANTIOCHUS', 'PERICLES', 'Daughter', 'THALIARD', 'HELICANUS', 'CLEON', 'DIONYZA', 'First Fisherman', 'Second Fisherman', 'Third Fisherman', 'SIMONIDES', 'THAISA', 'KNIGHTS', 'Marshal', 'First Knight', 'Knights', 'ESCANES', 'Second Knight', 'Third Knight', 'LYCHORIDA', 'Second Sailor', 'CERIMON', 'PHILEMON', 'LEONINE', 'MARINA', 'First Pirate', 'Second Pirate', 'Third Pirate', 'Pandar', 'BOULT', 'Bawd', 'LYSIMACHUS', 'Tyrian Sailor', 'KING RICHARD II', 'JOHN OF GAUNT', 'HENRY BOLINGBROKE', 'THOMAS MOWBRAY', 'Lord Marshal', 'DUKE OF AUMERLE', 'First Herald', 'Second Herald', 'GREEN', 'BUSHY', 'DUKE OF YORK', 'LORD ROSS', 'LORD WILLOUGHBY', 'BAGOT', 'HENRY PERCY', 'LORD BERKELEY', 'EARL OF SALISBURY', 'BISHOP OF CARLISLE', 'SIR STEPHEN SCROOP', 'Gardener', 'GARDENER', 'LORD FITZWATER', 'DUKE OF SURREY', 'Abbot', 'DUCHESS OF YORK', 'EXTON', 'Groom', 'BRAKENBURY', 'LADY ANNE', 'GENTLEMEN', 'DERBY', 'DORSET', 'CATESBY', 'Second murderer', 'Girl', 'Children', 'Lord Mayor', 'LORD STANLEY', 'Pursuivant', 'Priest', 'RATCLIFF', 'VAUGHAN', 'BISHOP OF ELY', 'LOVEL', 'Scrivener', 'ANOTHER', 'KING RICHARD III', 'TYRREL', 'Third Messenger', 'Fourth Messenger', 'CHRISTOPHER', 'RICHMOND', 'HERBERT', 'BLUNT', 'of Prince Edward', 'of King Henry VI', 'Ghost of CLARENCE', 'Ghost of RIVERS', 'Ghost of GREY', 'Ghost of VAUGHAN', 'Ghost of HASTINGS', 'of young Princes', 'Ghost of LADY ANNE', 'of BUCKINGHAM', 'LORDS', 'SAMPSON', 'GREGORY', 'ABRAHAM', 'BENVOLIO', 'TYBALT', 'CAPULET', 'LADY CAPULET', 'LADY MONTAGUE', 'ROMEO', 'PARIS', 'Nurse', 'MERCUTIO', 'Second Capulet', 'FRIAR LAURENCE', 'NURSE', 'LADY  CAPULET', 'Second Musician', 'Musician', 'Third Musician', 'Apothecary', 'FRIAR JOHN', 'SLY', 'First Huntsman', 'Second Huntsman', 'Players', 'A Player', 'LUCENTIO', 'TRANIO', 'BAPTISTA', 'GREMIO', 'KATHARINA', 'HORTENSIO', 'HORTENSIA', 'BIONDELLO', 'PETRUCHIO', 'GRUMIO', 'KATARINA', 'CURTIS', 'NATHANIEL', 'PHILIP', 'JOSEPH', 'NICHOLAS', 'Pedant', 'Haberdasher', 'Tailor', 'VINCENTIO', 'Boatswain', 'ALONSO', 'GONZALO', 'SEBASTIAN', 'Mariners', 'MIRANDA', 'PROSPERO', 'ARIEL', 'CALIBAN', 'ADRIAN', 'TRINCULO', 'IRIS', 'CERES', 'JUNO', 'Painter', 'Merchant', 'Jeweller', 'TIMON', 'Old Athenian', 'APEMANTUS', 'ALCIBIADES', 'Cupid', 'All Ladies', 'All Lords', 'CAPHIS', 'All Servants', 'FLAMINIUS', 'LUCULLUS', 'First Stranger', 'Second Stranger', 'SERVILIUS', 'Third Stranger', 'SEMPRONIUS', 'HORTENSIUS', 'PHILOTUS', 'Third Senator', 'Some Speak', 'Some Others', 'PHRYNIA', 'TIMANDRA', 'First Bandit', 'Second Bandit', 'Third Bandit', 'Banditti', 'SATURNINUS', 'BASSIANUS', 'MARCUS ANDRONICUS', 'TITUS ANDRONICUS', 'TAMORA', 'CHIRON', 'LAVINIA', 'Tribunes', 'MUTIUS', 'MARTIUS', 'QUINTUS', 'AARON', 'MARCUS', 'Young LUCIUS', 'AEMILIUS', 'First Goth', 'All the Goths', 'Second Goth', 'Third Goth', 'TROILUS', 'PANDARUS', 'AENEAS', 'CRESSIDA', 'ALEXANDER', 'AGAMEMNON', 'NESTOR', 'ULYSSES', 'MENELAUS', 'AJAX', 'THERSITES', 'ACHILLES', 'PATROCLUS', 'PRIAM', 'HECTOR', 'HELENUS', 'CASSANDRA', 'HELEN', 'CALCHAS', 'DEIPHOBUS', 'ANDROMACHE', 'MARGARELON', 'MYRMIDONS', 'DUKE ORSINO', 'CURIO', 'VALENTINE', 'VIOLA', 'SIR TOBY BELCH', 'SIR ANDREW', 'OLIVIA', 'MALVOLIO', 'FABIAN', 'PROTEUS', 'SPEED', 'JULIA', 'LUCETTA', 'PANTHINO', 'SILVIA', 'LAUNCE', 'THURIO', 'First Outlaw', 'Second Outlaw', 'Third Outlaw', 'EGLAMOUR', 'Outlaws', 'ARCHIDAMUS', 'CAMILLO', 'POLIXENES', 'LEONTES', 'HERMIONE', 'MAMILLIUS', 'Second Lady', 'ANTIGONUS', 'PAULINA', 'CLEOMENES', 'DION', 'Mariner', 'Time', 'AUTOLYCUS', 'FLORIZEL', 'PERDITA', 'DORCAS', 'MOPSA', 'Shepard']


print('Pick speakers for the play')
# Pick speakers for the new play
newplay_speakers = []
while len(newplay_speakers) < avg_num_speakers_per_play:
    newplay_speakers.append(random.choice(speakers))


# Create the scenes
with open('/home/imke/Dokumente/Studium/MA_CSE/Semester_3/DataMining/Shakespeare/newPlay.csv', 'wb') as writefile:
    writer = csv.writer(writefile, delimiter = '\t')
    row = []
    scene_count = 0
    
    while scene_count < avg_num_scenes_per_play:
        print('Writing scene ' + roman_numbers[scene_count])
        row = ['', ''.join('SCENE ' + roman_numbers[scene_count] + '\n')]
        print(row)
        writer.writerow(row)
        #Pick the speakers for the new scene
        num_speakers_this_scene = avg_num_speakers_per_scene + random.choice(var_range_num_speakers_per_scene)
        scene_speakers = []
        while len(scene_speakers) <= num_speakers_this_scene:
            scene_speakers.append(random.choice(newplay_speakers))
        
        # Write speeches of the scene
        num_speeches_this_scene = avg_num_speeches_per_scene + random.choice(var_range_num_speeches_per_scene)
        scene_speech_count = 0
        while scene_speech_count <= num_speeches_this_scene:
             
            #pick a speaker for this speech
            current_speaker = random.choice(scene_speakers)
            
            # Write speech        
            num_sentences_this_speech = avg_num_sentences_per_speech + random.choice(var_range_num_sentences_per_speech)        
            text = []
            speech_sentence_count = 0
            while speech_sentence_count <= num_sentences_this_speech:
                word = first_list[0]
                
                before_indx = -100000
                num_words_sentence = avg_num_words_per_sentence + random.choice(var_range_num_words_per_sentence)
                words_in_sentence = 0
                while  word is not '.' and node_list[first_list.index(word)].children:
                    if words_in_sentence == num_words_sentence:
                        word_indx = first_list.index('.')
                        words_in_sentence = 0
                    else:
                        
                        if word == first_list[0]:
                            word_indx = random.choice(range(1,len(first_list))) 
                        else:    
                            child_max_prob = np.argmax(node_list[first_list.index(word)].probabilities)
                            word_indx = node_list[first_list.index(word)].children[child_max_prob]
                            
                        
                        # To prevent infinite loops take the second largest probability
                        # if the children has the parent as child or if the word
                        # is already in the text
                        if word_indx == before_indx or first_list[word_indx] in text:
                            # if there is more than one child, take the one with 
                            # second highes probability
                            if len(node_list[first_list.index(word)].children)>1:
                                tmp = node_list[first_list.index(word)].children
                                tmp_probabilities = node_list[first_list.index(word)].probabilities
                                
                                max_el_indx = np.argmax(tmp_probabilities)
                                max_child = tmp[max_el_indx]
                                
                                tmp.remove(max_child)
                                tmp_probabilities.remove(max(tmp_probabilities))
                                
                                child_max_prob = np.argmax(tmp_probabilities)
                                word_indx = tmp[child_max_prob]
                            # if there is only on child, pick a random word
                            else:
                                word_indx = random.choice(range(1,len(first_list)))
                        words_in_sentence += 1    
                        
                        
                    word = first_list[word_indx]
                    before_indx = word_indx                  
                    text.append(word)
                    
                        
                
                #text.append('\n')
                speech_sentence_count += 1
            
            #print('Writing Speech of ' + current_speaker + ': ' + ''.join(text))
            row = [current_speaker, ' '.join(text)]
            print(row)
            writer.writerow(row)
                        
                        
            scene_speech_count += 1
            
        scene_count += 1
            
            