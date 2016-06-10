#####################################################################################
## jmapManifest.py
## Create a manifest of articles that a publisher (or source has contributed to
## be geotagged and included in JournalMap. This script just trolls through a
## parent directory structure looking for XML files and associated PDFs and builds
## a list of articles and article metadata. Output is a .csv file.
#####################################################################################

import os
import fnmatch
import unicodecsv, csv
from bs4 import BeautifulSoup

#startDir = '/Volumes/XML Storage/AOU'
startDir = '/Users/jason/Google Drive/JournalMap/GeoParser_Paper/TandF'
outfile = startDir + '/TandF_manfest.20160606.csv'

with open(outfile, 'wb') as csvFile:
    csvWriter = unicodecsv.writer(csvFile)
    csvWriter.writerow(['doi','title','journal','publisher','year','vol','issue','xmlfile','pdffile'])

    ## Traverse the start directory structure
    i = 0 # initialize article counter
    for root, dirs, files in os.walk(startDir):
        for name in fnmatch.filter(files, '*.xml'):
            ###############################
            ## Grab the article XML file ##
            ############################### 
            i += 1
            xmlFile = os.path.join(root,name)
            print("Processing " + xmlFile)
            
            ###############################
            ## Grab the article metadata ##
            ###############################        
            tree = BeautifulSoup(open(xmlFile))
            try: doi = tree.find('article-id', {'pub-id-type':'doi'}).text 
            except: doi=''
            try: title = tree.find('article-title').text
            except: title=''
            try: journal = tree.find('journal-title').text
            except: journal=''            
            try: publisher = tree.find('publisher-name').text
            except: publisher = ''
            try: year = tree.find('pub-date').year.text
            except: year = ''
            try: vol = tree.find('volume').text
            except: vol=''
            try: issue = tree.find('issue').text
            except: issue = ''
    
            ###############################
            ## Check for a PDF file      ##
            ############################### 
            if os.path.isfile(os.path.join(root,name.split(".")[0]+".pdf")):
                pdfFile = os.path.join(root,name.split(".")[0]+".pdf")
            else:
                pdfFile = ''
                
            ###############################
            ## Write row to output file  ##
            ###############################
            csvWriter.writerow([doi,title,journal,publisher,year,vol,issue,xmlFile,pdfFile])
    
    print("")
    print("Finished traversing directory " + startDir)
    print("Processed " + str(i) + " XML files.")
    print("Article details written to manifest file: " + outfile)
    
    