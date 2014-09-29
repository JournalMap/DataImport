### PensoftUpdate.py
### Script for downloading and saving Pensoft content from a given date to present.


import requests, StringIO, time


journallist = ['zookeys','phytokeys','biorisk','neobiota','jhr','ijm','compcytogen','subtbiol','natureconservation','mycokeys','zse','dez','nl','ab']
urldate = time.strftime("%d-%m-%Y").replace('-','%2F')
urlbase = 'http://bdj.pensoft.net/lib/journal_archive.php?journal='

for journal in journallist:
    r = requests.get(urlbase+journal+'&date='+urldate)
    output = open('/Users/jason/Downloads/test.zip', 'w')
    output.write(r.content)
    output.close()

