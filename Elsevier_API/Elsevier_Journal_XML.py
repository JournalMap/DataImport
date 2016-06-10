import requests, json, time
import os, sys, re, StringIO
import fnmatch
import unicodecsv, csv

from decimal import Decimal, setcontext, ExtendedContext
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.append('/Users/Jason/Dropbox/JournalMap/scripts/GeoParsers')

#### Set Options ####
saveXML = True
saveDir = '/Users/jason/Google Drive/JournalMap/Elsevier/Geoderma'
apiKey = '7cc75ee7eb87607977e73916ec347c7d'
issn = '00167061'
#####################


## Get the list of DOIs from Elsevier and build the DOI iterator
r = requests.get('http://api.elsevier.com/content/search/scidir?query=issn('+issn+')&APIKey='+apiKey+'&httpAccept=application/json&field=doi&count=200')
ElsvContent = json.loads(r.text)
total = ElsvContent['search-results']['opensearch:totalResults']

dois = []
start = datetime.now()
#for i in range (1,int(total),200):
for i in range (401,2000,200):
    page = requests.get('http://api.elsevier.com/content/search/scidir?query=issn('+issn+')&APIKey='+apiKey+'&httpAccept=application/json&field=doi&count=200&start='+str(i))
    pageResults = json.loads(page.text)
    doiList = pageResults['search-results']['entry']
    #print doiList
    for doi in doiList:  # Iterate over the DOIs and write them to a master list of DOIs
        #print doi['prism:doi']
        dois.append(doi['prism:doi'])
    time.sleep(2)
end = datetime.now()
delta = end-start
print "Total Records Fetched: "+str(len(dois))
print "Elapsed processing time: " + str(delta)

## Iterate over the DOI list
start = datetime.now()
# dois = dois[0:25]
for doi in dois:
    # Keep us out of trouble by not battering their server
    time.sleep(2)
        
    ## Fetch the XML for the DOI
    xmlRequest = requests.get('http://api.elsevier.com/content/article/doi/'+doi+'?APIKey='+apiKey+'&httpAccept=text/xml&view=full')
    xml = xmlRequest.text
    #print len(xml)
    
    ## Option to save the XML
    if saveXML:
        f = open(saveDir+'/'+doi.replace('/','.')+'.xml', 'w')
        f.write(xml.encode('utf-8'))
        f.close()

    print "Finished processing XML for " + doi

    ## Parse the XML for the JournalMap stuff...
    #articleDOI = tree.coredata.find('dc:identifier').text
end = datetime.now()
delta = end-start
print "Finished processing download of " + str(len(dois)) + " XML files."
print "Time to complete download: " + str(delta)
