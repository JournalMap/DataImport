## Format BibTex files as a JournalMap articles.csv file

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
import csv, urllib2, unicodecsv

def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = convert_to_unicode(record)
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    
    return record

infile = '/Users/jason/Dropbox/JournalMap/SampleMarsPapers/bibtex-records_first100MarsExamples.txt'  #Dropbox/JournalMap/scripts/bibtex_parser/bibtex_test_set.txt'
outfile = '/Users/jason/Dropbox/JournalMap/SampleMarsPapers/articles100.csv'  #JournalMap/scripts/bibtex_parser/test.csv'


## open BibTex file
with open(infile, 'r') as bibfile:
    bibtex = bibfile.read()
    
## collapse keyword fields
out = ''
articles = bibtex.split('\n\n')
for article in articles:
    kws=''
    lines = article.split('\n')
    for line in lines:
        parts = line.split('=')
        if parts[0]=="optkeywords":
            kws = kws+parts[1]
        elif parts[0]=='}':
            break
        else:
            out=out+line+'\n'
    if kws=='':
        out=out+'"\n}\n'
    else:
        out=out+',\noptkeywords="'+kws.replace('"','')+'"\n}\n'


    
## Parse the BibTex
bp = BibTexParser(out, customization=customizations)

## Set up the output file and write the first line
with open(outfile, 'wb') as outcsv:
    csvwriter = unicodecsv.writer(outcsv)
    csvlines = [['doi','publisher_name','publisher_abbreviation','citation','title','publish_year','first_author','authors_list','volume_issue_pages','volume','issue','start_page','end_page','keywords_list','no_keywords_list','abstract','no_abstract','url']]

    article_list = bp.get_entry_list()
    for article in article_list:    
        #typ = article['type']
        typ = 'article'
        if typ=='article':
            if 'author' in article.keys():
                authors = ', '.join(article['author'])
                first_author = article['author'][0]
            else:
                authors = ''
                first_author = ''
            title = article['title'] if 'title' in article.keys() else ''
            kw = article['optkeywords'] if 'optkeywords' in article.keys() else ''
            no_kw = 'true' if kw == '' else 'false'
            journal = article['journal']['name'] if 'journal' in article.keys() else ''
            issue = article['number'] if 'number' in article.keys() else ''
            abstract = article['abstract'] if 'abstract' in article.keys() else ''
            no_ab = 'true' if abstract == '' else 'false'
            volume = article['volume'] if 'volume' in article.keys() else ''
            year = article['year'] if 'year' in article.keys() else ''
            doi = article['doi'].replace('"','') if 'doi' in article.keys() else ''
            pages = article['pages'] if 'pages' in article.keys() else ''
            if pages != '':
                s_page = pages.split('--')[0] 
                e_page = pages.split('--')[1] if len(pages.split('--'))>1 else ''
            else:
                s_page = ''
                e_page = ''
            volisspg = volume+'('+issue+'):'+s_page+'-'+e_page
            url = article['opturl'] if 'opturl' in article.keys() else ''

            ## do article DOI lookup if no DOI

        
            csvlines.append([doi,journal,'','',title,year,first_author,authors,volisspg,volume,issue,s_page,e_page,kw,no_kw,abstract,no_ab,url])
    
    csvwriter.writerows(csvlines)
    
        
        
                  