import os, glob

dir = '/Users/jason/Dropbox/JournalMap/scripts/DataImport/museum_collections/'

pdfList = glob.glob(dir+"*.pdf")
print(pdfList)

for pdf in pdfList:
    base = pdf.split(".")[0]
    print("/usr/local/bin/pdf2txt.py -o "+base+".txt "+pdf)
    os.system("/usr/local/bin/pdf2txt.py -o "+base+".txt "+pdf)
