import requests, json, re, datetime
import mysql.connector
from time import sleep
from datetime import datetime, date


keywords = 'agriculture'

r = requests.get('http://api.crossref.org/works?query='+keywords+'&rows=0&filter=has-license:true,has-full-text:true')
count = json.loads(r.text)['message']['total-results']

items = []
for i in range (0,count,1000):
    urls = requests.get('http://api.crossref.org/works?query='+keywords+'&rows=1000&offset='+str(i)+'&filter=has-license:true,has-full-text:true')
    print 'http://api.crossref.org/works?query='+keywords+'&rows=1000&offset='+str(i)+'&filter=has-license:true,has-full-text:true'
    text = json.loads(urls.text)
    items = items + text['message']['items']    
    sleep(1)

print "Total Records Fetched: "+str(len(items))


cnx = mysql.connector.connect(user='jmap', password='M0untainBiking!', host='128.123.177.250', database='jmapContent')    
cursor = cnx.cursor()
add_record = ("INSERT INTO raw_content "
              "(DOI, type, license, raw, URL, source, publisher, date_added)"
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    
cc_re = re.compile('creativecommons')
cc_count = 0
other_count = 0
for item in items:

    iscc = cc_re.search(item['license'][0]['URL'])
    try:
        if iscc.start(): 
            cc_count += 1
            doi = item['DOI']
            source = item['source']
            publisher = item['publisher']
            license = item['license'][0]['URL']
            date_added = datetime.now().date()
            for link in item['link']:
                contentURL = link['URL']
                contentType = link['content-type']
                if contentType == "application/xml" or contentType == "text/xml":
                    contentType = "xml"
                    rawContent = requests.get(contentURL).text 
                    break
                elif contentType == "text/plain":
                    contentType = "text"
                    rawContent = requests.get(contentURL).text 
                    break
                else:
                    contentType == "unspecified"
                    rawContent = ""
            data_record = (doi,contentType,license,rawContent,contentURL,source,publisher,date_added)
            cursor.execute(add_record, data_record)
            cnx.commit()  
            print "finished article " + doi
            sleep(1)
    except AttributeError:
        other_count += 1


cursor.close()
cnx.close()
print "finished"


""" Item:
{u'publisher': u'Elsevier BV', u'DOI': u'10.1016/s1754-5048(14)00154-8', u'subtitle': [], u'member': u'http://id.crossref.org/member/78', u'license': [{u'delay-in-days': 0, u'start': {u'timestamp': 1422748800000, u'date-parts': [[2015, 2, 1]]}, u'content-version': u'tdm', u'URL': u'http://www.elsevier.com/tdm/userlicense/1.0/'}], u'title': [u'Editorial board'], u'URL': u'http://dx.doi.org/10.1016/s1754-5048(14)00154-8', u'issued': {u'date-parts': [[2015, 2]]}, u'reference-count': 0, u'ISSN': [u'1754-5048'], u'volume': u'13', u'source': u'CrossRef', u'prefix': u'http://id.crossref.org/prefix/10.1016', u'score': 2.960265, u'link': [{u'intended-application': u'text-mining', u'URL': u'http://api.elsevier.com/content/article/PII:S1754504814001548?httpAccept=text/xml', u'content-version': u'vor', u'content-type': u'text/xml'}, {u'intended-application': u'text-mining', u'URL': u'http://api.elsevier.com/content/article/PII:S1754504814001548?httpAccept=text/plain', u'content-version': u'vor', u'content-type': u'text/plain'}], u'container-title': [u'Fungal Ecology'], u'indexed': {u'timestamp': 1423685119450, u'date-parts': [[2015, 2, 11]]}, u'deposited': {u'timestamp': 1417564800000, u'date-parts': [[2014, 12, 3]]}, u'type': u'journal-article', u'page': u'IFC', u'subject': [u'Ecology, Evolution, Behavior and Systematics', u'Plant Science', u'Ecological Modelling', u'Ecology']}
"""

"http://api.elsevier.com/content/article/DOI:10.1016/j.ibusrev.2010.09.002?APIKey=165c49e4574db9b5ba8e82e544089ef8"

