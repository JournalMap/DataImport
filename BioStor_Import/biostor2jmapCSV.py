# json2jmap.py
# Script for converting BioStor's json files to JournalMap csv import format
# 29 Aug 2013
# Jason Karl

import json, csv, requests, unicodecsv
from time import sleep

## 0. setup pathways and constants

urlbase = 'http://biostor.org/reference/'
pathbase = '/Users/jason/Dropbox/JournalMap/scripts/Biostor_import/'
saveJSON = 'FALSE'
JSONfromWeb = 'FALSE'

## 1. Fetch list of BioStor articles
biostorlist = [4,8,10,13,15,45,53,62,74,76,78,80,154,171,178,183,189,194,198,200,210,211,212,215,217,219,220,221,222,223,230,231,288,301,307,310,315,328,358,363,394,470,472,513,524,4057,11914,12706,13027,13052,20792,20843,40481,49862,49896,49897,52382,55117,55278,57096,62089,62348,63875,64602,64674,67469,74616,75201,95381,95413,97419,97424,99070,110264,110559,111685,112345,112365,113518,113617,113931,113932,115598,133692,135239,137036,137146,137612,140515,61,3227,95401,97273,99385,103506,103993,113849,116480,133074]

## works list [4,8,10,13,15,45,53,62,74,76,78,80,154,171,178,183,189,194,198,200,210,211,212,215,217,219,220,221,222,223,230,231,288,301,307,310,315,328,358,363,394,470,472,513,524,4057,11914,12706,13027,13052,20792,20843,40481,49862,49896,49897,52382,55117,55278,57096,62089,62348,63875,64602,64674,67469,74616,75201,95381,95413,97419,97424,99070,110264,110559,111685,112345,112365,113518,113617,113931,113932,115598,133692,135239,137036,137146,137612,140515,61,3227,95401,97273,99385,103506,103993,113849,116480,133074]

## fail list - authors blank []

## 2. Set up output CSV files
with open(pathbase+'articles.csv','wb') as articlesCSV:
    with open(pathbase+'locations.csv','wb') as locationsCSV:
        articlewriter = unicodecsv.writer(articlesCSV,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
        locationwriter = unicodecsv.writer(locationsCSV,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
        
        articlelines = [['doi','publisher_name','publisher_abbreviation','citation','title','publish_year','first_author','authors_list','volume_issue_pages','volume','issue','start_page','end_page','keywords_list','no_keywords_list','abstract','no_abstract','url']]
        locationlines = [['doi','title','longitude','latitude','place','no_recorded_place','coordinates','coordinate_type','no_recorded_coordinate','location_type','location_scale','location_reliability','location_conformance','error_type','error_description']]
        
        ## 3. Set up iterator over article list
        for biostorID in biostorlist:
        
            ## 3.1. Fetch json file from BioStor
            if JSONfromWeb=='TRUE':
                sleep(1)
                request = requests.get(urlbase+str(biostorID)+'.json')
                json_data = request.json()
                if saveJSON=='TRUE':
                    with open(pathbase+'json/'+str(biostorID)+'.json','wb') as jsonFile:
                        json.dump(json_data, jsonFile)            
            else:  ## read JSON from files
                with open(pathbase+'json/'+str(biostorID)+'.json','rb') as jsonFile:
                    json_data=json.load(jsonFile)
            print "Processing BioStor article "+str(biostorID)            
            
            
            ## 3.3. Grab citation info and write to articles array
            doi = json_data["identifiers"].get("doi")
            biostor = json_data['identifiers']['biostor']
            url = 'http://biostor.org/reference/'+str(biostor)
            year = json_data['year']
            title = json_data['title']
            journal = json_data['publication_outlet']
            vol = json_data['volume']
            pages = json_data['pages']
            alist = json_data['authors']
            if alist:
                first_author = alist[0]['surname']+', '+alist[0]['forename']
                            
                ## Iterate over all authors to construct authors list
                authors = ''
                for a in alist:
                    authors = authors+', '+a['surname']+', '+a['forename']
                authors = authors[2:] ## Strip off the leading comma and space
            else:
                first_author = '<no_listed_authors>'
                authors = '<no_listed_authors>'
                    
            ## 3.4. Write articles line to the CSV
            citation = authors+". "+year+". "+title+". "+journal+" "+vol+":"+pages+"."
            spage = pages[0:pages.find('-')]
            epage = pages[pages.find('-')+1:]
            volisspg = vol+":"+pages
            articlelines.append([doi,journal,'',citation,title,year,first_author,authors,volisspg,vol,'',spage,epage,'','TRUE','','TRUE',url])
            
            ## 3.5.  Grab the location info and write to locations array
            locations = json_data['geometry'].get('coordinates')
            featuretype = json_data['geometry'].get('type')
            if locations and featuretype=='MultiPoint':  ## Dealing only with points for now (I think that's all BioStor has to date)
                for location in locations:
                    lat, lon = location[0], location[1]
                    locationlines.append([doi,title,lon,lat,'','TRUE',str(location).strip('[]'),'Geographic Coordinate System (GCS)','FALSE','point','site','1','3','',''])
            
        ## 4. Write arrays to the CSV files and clean up
        locationwriter.writerows(locationlines)
    articlewriter.writerows(articlelines)