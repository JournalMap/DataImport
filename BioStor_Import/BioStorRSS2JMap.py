## BioStorRSS2JMap.py
## Importer to return ID numbers of recent BioStor articles that have geotagged locations
## Recent is defined as occurring since the last time this script was run (previous date is cached in a file)


import feedparser, json, requests
import time

# Setup 
paramsfile = 'UpdateHistory.json'
urlbase = 'http://biostor.org/reference/'
outpath = '/Users/jason/Dropbox/JournalMap/Journal_Map_Data/BioStor/'
outfilebase = 'BioStorUpdateList'
updatelist = []

# 1. Grab the BioStor RSS feed and find the most recent article ID number
feed = feedparser.parse('http://biostor.org/rss')
recentID = feed['entries'][0]['id'].strip('http://biostor.org/reference/')


# 2. Fetch the last parsed BioStor ID number
with open(paramsfile,'rb') as pFile:
    param_json = json.load(pFile)
numUpdates = len(param_json['updates'])
lastID=param_json['updates'][numUpdates-1]['lastbiostorID']

# 3. Iterate over the biostor ID range

try:      # Execute until/unless error encountered (most likely timeout with fetching JSON)
    if int(lastID) < int(recentID):
        biostorRange = range(int(lastID)+1,int(recentID))
        for biostorID in biostorRange:         
            
            # 3.1 Grab the json file for the ID
            time.sleep(1)
            print "Checking BioStor article "+str(biostorID)+"."
            request = requests.get(urlbase+str(biostorID)+'.json')
            json_data = request.json()
            if json_data.get('error'): raise
    
            # 3.2 Check the json for coordinates
            if json_data.get('geometry'):
    
                # 3.3 If coordinates, save json to local file and add ID number to list            
                with open(outpath+'json/'+str(biostorID)+'.json','wb') as jsonFile:
                    json.dump(json_data, jsonFile)            
                updatelist.append(biostorID)
    else:
        biostorID = recentID
except:    # Write out the update list and the last record checked even if an error occurred
    print 'Error encountered with BioStorID '+str(biostorID)
    print 'Saving output so far...'
    
# 4. Write the ID list to a date-coded text file
with open(outpath+outfilebase+str(time.strftime("%Y%m%d"))+".txt","ab") as outFile:
    outFile.writelines(["%s\n" % item for item in updatelist])


# 5. write the last ID number checked (recentID) and current date to the params file
update = {'date':time.strftime("%Y%m%d"),'lastbiostorID':biostorID-1}
param_json['updates'].append(update)
    
with open(paramsfile,'wb') as pFile:
    json.dump(param_json, pFile)

print "Finished!"