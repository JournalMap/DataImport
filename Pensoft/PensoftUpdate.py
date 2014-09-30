### PensoftUpdate.py
### Script for downloading and saving Pensoft content XML files from their API for a given date to present.


import requests, time, json, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

## Set up constants

configfile = "PensoftUpdate.config"
paramsfile = 'PensoftHistory.json'

with open(configfile, 'rb') as pFile:
    config_json = json.load(pFile)
journallist = config_json['journallist']
urlbase = config_json['urlbase']
outpath = config_json['outpath']
user = config_json['user']
pw = config_json['pw']
fromaddr = config_json['fromaddr']
toaddr = config_json['toaddr']

#journallist = ['zookeys','phytokeys','biorisk','neobiota','jhr','ijm','compcytogen','subtbiol','natureconservation','mycokeys','zse','dez','nl','ab']
#urlbase = 'http://bdj.pensoft.net/lib/journal_archive.php?journal='
#outpath = '/Users/jason/Downloads/'
#user = 'jakal14@gmail.com'
#pw = 'asgyuckadibjqymu'
#fromaddr = 'jakal14@gmail.com'
#toaddr = 'jkarl@nmsu.edu'
#toaddr = ['jkarl@nmsu.edu', 'jgillan@nmsu.edu']

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
day = time.strftime('%d').lstrip('0')
month = time.strftime('%m').lstrip('0')
year = time.strftime('%Y')
newdate = day+'-'+month+'-'+year
update = {'date':newdate}
param_json['updates'].append(update)    
with open(paramsfile,'wb') as pFile:
    json.dump(param_json, pFile)


## Send notification email
msg = MIMEMultipart()
msg['From'] = 'JournalMap <'+fromaddr+'>'
msg['To'] = ', '.join(toaddr)
msg['Subject'] = 'Auto Notification: New Pensoft content ready for JournalMap import'
body = "New Pensoft articles have been downloaded to the XML Storage drive and are ready to be imported to JournalMap. \n\n This message was created automatically by SkyNet on behalf of JournalMap. You can't hide. There is no hope. JournalMap is taking over the world..."
msg.attach(MIMEText(body,'plain'))
text = msg.as_string()

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(user,pw)
server.sendmail(fromaddr,toaddr,text)
server.quit()
