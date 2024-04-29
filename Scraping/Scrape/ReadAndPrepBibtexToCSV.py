import bibtexparser
import os
import csv
import unicodedata
import pandas as pd
import time

import CleanUpDatabase
import RemoveDuplicates

# for all files
    # for each file
        # for each entry
            # get title authors abstract year doi
i = 0
finalList = []

def iterateOverFiles(_rootDirectory):
    for root, dirs, files in os.walk(_rootDirectory):
        for file in files:
            if (file.endswith('bib')):
                iterateOverFile(root, file)
    return

def iterateOverFile(_root, _file):
    print(_root+_file)
    with open(_root+_file, encoding='utf-8') as file:
        bibfile =  bibtexparser.load(file)
        for entry in bibfile.entries:
            iterateOverEntry(entry)
    return

def iterateOverEntry(_entry):
    # print(_entry)        

    author = checkAndParseKey(_entry, "author", "NoValue")       
    year = checkAndParseKey(_entry, "year", "0000")       
    title = checkAndParseKey(_entry, "title", "NoValue")       
    doi = checkAndParseKey(_entry, "doi", "0000")       
    abstract = checkAndParseKey(_entry, "abstract", "NoValue")       
    publicationTitle = getPublicationTitle(_entry)
    citationcount = 0   

    doi = doi.replace('https://doi.org/', '')
    # print (doi)
    
    global finalList

    finalList.append([title, author, year, publicationTitle, 
                        citationcount, doi, abstract])
    
    return

def getPublicationTitle(_entry):
    res ="NeverAssigned"
    if _entry.get('ENTRYTYPE') == 'article':
        res = checkAndParseKey(_entry, "journal", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'inproceedings':
        res = checkAndParseKey(_entry, "booktitle", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'inbook':
        res = checkAndParseKey(_entry, "booktitle", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'proceedings':
        res = checkAndParseKey(_entry, "title", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'book':
        res = checkAndParseKey(_entry, "title", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'conference':
        res = checkAndParseKey(_entry, "title", "NoValue")
    elif _entry.get('ENTRYTYPE') == 'incollection':
        res = checkAndParseKey(_entry, "booktitle", "NoValue")

    else:
        print (_entry.get('ENTRYTYPE'))
        print (_entry)
        print()
    


    return res
def checkAndParseKey(_entry, _key, _default):
    val = _entry.get(_key, _default)
    # print(val)        

    return transform_confusables(val)


def writeFinalFile(_targetDir):
    global finalList
    with open(_targetDir, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter = ";")
        writer.writerows(finalList)

    print("Data has been written to", _targetDir)
    return

# LLM
def transform_confusables(text):
    normalized_text = unicodedata.normalize('NFC', text)
    
    transformed_text = ''
    for char in normalized_text:
        try: #HACK some weird char rasies a value error during name lookkup
            char_name = unicodedata.name(char)
            transformed_text += unicodedata.lookup(char_name)
        except ValueError:
            # If ValueError occurs, simply append the original character
            transformed_text += char
    
    return transformed_text

##########

finalList.append(['title', 'authors', 'year', 'publicationtitle', 'citationcount', 'doi', 'abstract'])

rootDir = "./Input/"
iterateOverFiles(rootDir)

targetDir = "./Results/"
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "Results.csv"
# writeFinalFile(targetDir+timestr+"-"+filename)

# convert to pandas
finalDf = pd.DataFrame(finalList)
# make first row header
new_header = finalDf.iloc[0] #grab the first row for the header
finalDf = finalDf[1:] #take the data less the header row
finalDf.columns = new_header #set the header row as the df header

# cleaning
finalDf = CleanUpDatabase.make_to_int(finalDf)
finalDf = CleanUpDatabase.add_final_columns_for_toolkit(finalDf)
finalDf = RemoveDuplicates.RemoveDuplicateEntriesFromDataframeBasedOnDOI(finalDf)

finalDf["other"] = "0"
finalDf["backtracking"] = "0"

print(len(finalDf))
finalDf.to_csv(targetDir + timestr + "-" + filename + "-converted.csv", sep=";")
# finalDf.to_csv(targetDir + "-" + filename + "-converted.csv", sep=";", encoding='utf-8')