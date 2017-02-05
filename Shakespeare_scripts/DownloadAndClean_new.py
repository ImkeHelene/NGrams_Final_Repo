# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 21:48:30 2016

@author: imke
"""
import gzip
import os
import sys
import glob
import shutil
import subprocess
import collections
#import zlib
import zipfile
from collections import OrderedDict
from itertools import islice, product, chain, groupby
from nltk.corpus import stopwords

from opster import Dispatcher
from py.path import local
from google_ngram_downloader import readline_google_store
import _Cleaning
import csv

import requests
                
# Download unigrams and clean data.
                
                
def unzipGZ(compressedFile, outFilePath):
#    import gzip
#    import glob
#    import os.path
#    import shutil

#    source_dir = "./dumps/server1"
#    dest_dir = "./dedupmount"
#    tmpfile = "/tmp/delete.me"
        
#        decompressedFile = gzip.GzipFile(fileobj = compressedFile, mode='rb')
#        with open(outFilePath, 'w') as outfile:
#            outfile.write(decompressedFile.read())
    iNF = gzip.GzipFile(compressedFile, 'rb')
    s = iNF.read()
    iNF.close()
    
    outF = open(outFilePath, 'wb')
    outF.write(s)
    outF.close()


def download(ngram_len, stpwds):
    """Download The Google Books Ngram Viewer dataset version 20120701."""
    output = os.getcwd() + '{ngram_len}'
    #set ngram len in the output file
    output = local(output.format(ngram_len=ngram_len))
    #Create the output directory if it doesn't exist yet
    output.ensure_dir()
    verbose = False
    lang = 'eng-gb'
    Cleaned_out = []
    #numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    download = ['lo', 'ma', 'sh', 'wo', 'go', 'en']
                    
    for fname, url, request in readline_google_store(ngram_len, 
                                                     verbose=verbose, 
                                                     lang=lang):
                                                         
            if (fname[len(fname)-5:len(fname)-4] not in numbers): continue
            else:

                print("downloading " + fname)
                session = requests.Session()
                request = session.get(url, stream=True)
                assert request.status_code == 200        
                with output.join(fname).open('wb') as f:
                    for num, chunk in enumerate(request.iter_content(1024)):
                        if verbose and not divmod(num, 1024)[1]:
                            sys.stderr.write('.')
                            sys.stderr.flush()
                        f.write(chunk)
                        
                        
                #print [file for file in os.getcwd() + '1' + '/*.gz']
                #os.chdir(os.getcwd() + '/1')
                if not os.path.isfile(f.name[:-3]):
                    os.mknod(f.name[:-3])
                
                unzipGZ(f.name, f.name[:-3])      
                
                print f.name
                #os.remove(f.name)
            
                #cleaned_out = clean(f.name[:-3], stpwds)
            
                #Cleaned_out.append(cleaned_out)
    return Cleaned_out
            
def find_max_count(reader):
    max_count = 0
    for row in reader:
        print row[2]
        if row[2] > max_count:
            max_count = row[2]
            
    return float(max_count)
            
            
def clean(fname, stpwds):
    print "Cleaning " + fname
    with open(fname, 'rb') as csvfile:
            row_count = len(csvfile.readlines())
            print row_count
            reader = csv.reader(csvfile, delimiter='\t', dialect='excel')
           
            max_count = 0
            for row in reader:
                print row[0]
                print row[1]
                if float(row[2]) > max_count:
                    max_count = row[2]
            
            max_count = float(max_count)
            print max_count
            
            with open(fname + '_Cleaned' ,'wb') as writefile:
                writer = csv.writer(writefile, delimiter= '\t', dialect='excel')
                Cleaner = _Cleaning.Clean_NGrams(max_count, row_count)
                
                indx = -1
                for row in reader:
                    indx += 1
                    Cleaner.rough(indx, row)
                    if Cleaner.drop == 1:
                        continue
                    else:

                        Cleaner.types(indx, [row[0]]) 
                        Cleaner.row.append(row[1:len(row)])     
                        
                        writer.writerow(Cleaner.row)

                Cleaned_out = Cleaner.clean_count  
                
                    
    print "Done"
    return Cleaned_out
                
stpwds = stopwords.words('english')
_Cleaning.extendStopwords(stpwds)

Cleaned_out = download(2, stpwds)
#avg_cleaned = sum(Cleaned_out)/float(len(Cleaned_out))
#print("Cleaned total average of " + str(avg_cleaned))
