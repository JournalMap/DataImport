### PensoftUpdate.py
### Script for downloading and saving Pensoft content XML files from their API for a given date to present.


import requests, time, json


## Set up constants
journallist = ['zookeys','phytokeys','biorisk','neobiota','jhr','ijm','compcytogen','subtbiol','natureconservation','mycokeys','zse','dez','nl','ab']
urlbase = 'http://bdj.pensoft.net/lib/journal_archive.php?journal='
outpath = '/Users/jason/Downloads/'
paramsfile = 'PensoftHistory.json'

## Fetch the last date the script was run
with open(paramsfile,'rb') as pFile:
    param_json = json.load(pFile)
numUpdates = len(param_json['updates'])
lastDate=param_json['updates'][numUpdates-1]['date']

urldate = lastDate.replace('-','%2F')

## Grab any new content from Pensoft
for journal in journallist:
    r = requests.get(urlbase+journal+'&date='+urldate)
    output = open(outpath+journal+'-'+lastDate+'.zip', 'w')
    output.write(r.content)
    output.close()


## Update the params file with the new date
day = time.strftime('%d').strip('0')
month = time.strftime('%m').strip('0')
year = time.strftime('%Y')
newdate = day+'-'+month+'-'+year
update = {'date':newdate}
param_json['updates'].append(update)    
with open(paramsfile,'wb') as pFile:
    json.dump(param_json, pFile)
