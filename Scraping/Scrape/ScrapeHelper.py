import datetime
import csv
import re                       #regex
import os               
import glob
import pandas as pd

sQuoteChar = "%22"
sSpaceChar = "+"
sConnectChar = "&"
sAllField = "AllField="
sBaseString = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl" # only acm full-text 
sBaseString = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced" #acm guide to computing lib
sBaseString = 'https://dl.acm.org/action/doSearch?AllField='
sEndString = '&expand=dl"' #dl is digital lib; all ' computing lib

## this is for acm
AfterStartMonth = "AfterMonth=" + str(1)
AfterStartYear = "AfterYear=" + str(2023)
ResearchArticleOnly = 'ContentItemType=research-article'
Expand = 'expand=dl'

notTerm = ""



############# RANDOM ##############

def WriteFile(_text, _filename):
    with open(_filename, 'w', encoding="utf-8") as f:
        f.write(_text)
    print('Written to', _filename)
    f.close()

def GetNowString():
    now = datetime.datetime.now()
    format = "%Y-%m-%d_%H-%M"
    #format datetime using strftime() 
    return  now.strftime(format)

def getwd():
    return os.getcwd() 

def WriteDBToCSV(_DB, _filename):
    with open(_filename, 'w', newline='', encoding='UTF-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        
        spamwriter.writerow(['title', 'authors', 'year', 'publicationtitle', 'citationcount', 'doi', 'abstract'])

        for row in _DB:
            spamwriter.writerow(row)

    print ('Final number of records: ' + str(len(_DB)))

def GetMostRecentFile(directory, fileextension):
    # IEEE__Reviews__2021-05-04_17-21_data

    path = getwd() + '/' + directory
    print (path)
    listOfFiles = glob.glob(path + '*.' + fileextension) # * means all if need specific format then *.csv
    latestFile = max(listOfFiles, key=os.path.getctime)
    return latestFile

def clean_year(_time):
    #print(_time)

    #regex = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Apr(?:il)?|Mar(?:ch)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) (?:19[7-9]\d|2\d{3})(?=\D|$)'
    try:
        year = _time
        year = year.replace(",", "")
        year = year.replace(" ", "")
        year = year[-4:]
    except Exception as e:
        print(year)
        print(e)
        year = ""  
    print (year)

    not_term = notTerm
############# SEARCH QUERIES ##############

def CleanMaxResultForACMURL(_numResults):
    d = re.sub('\D', '', _numResults)
    d = int(d)
    return d

def ACM_AddMiddlePartForSearchURL(_searchurl, _operator, _tmplist, _bUseOnlyTitle):
    res = _searchurl

    # https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&AfterMonth=1&AfterYear=2015&AllField=Title%3A%28%28%27Augmented+Reality%27+OR+%27Mixed+Reality%27%29+AND+%28%27survey%27+or+%27review%27%29%29
    # https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&AfterMonth=1&AfterYear=2015&AllField=%28%27Augmented+Reality%27+OR+%27Mixed+Reality%27%29+AND+%28%27survey%27+or+%27review%27%29
    # https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&AfterMonth=1&AfterYear=2015&ContentItemType=research-article&AllField=AllField=Title%3A%28%22augmented+reality%22+OR+%22mixed+reality%22%29+AND+AllField=Title%3A%28%22review%22+OR+%22survey%22%29


    for item in _tmplist[:-1]:
        res += sQuoteChar + item.replace(" ", "+") + sQuoteChar
        if len(_tmplist) > 1:
            res += _operator
    res += sQuoteChar + _tmplist[-1].replace(" ", "+") + sQuoteChar
    res += ")" #)
    return res
    
def ACM_BuildReviewURL(_filename, _bUseOnlyTitle):
    print()
    searchurl = sBaseString + sConnectChar 

    if _bUseOnlyTitle:
        searchurl += "AllField=Title%3A("
    else:
        searchurl += "AllField=(" # ([
    with open(_filename) as csv_file:
        df = csv.reader(csv_file, delimiter=',')
        df = list(df)
        for row in df:
            #print(row)
            #print ("Adding... " + str(row))
            searchurl += "("
            searchurl = ACM_AddMiddlePartForSearchURL(searchurl, "+OR+", row, _bUseOnlyTitle)
            
            searchurl += "+AND+"        

        searchurl = searchurl[:len(searchurl)-5]
        #print (searchurl)
        #print (len(searchurl))

        searchurl += ")" #)

        print ("Final short page URL: " + searchurl)  
    return searchurl

def ACM_QueryTermBuilder(_filename, _bIsReview, _bUseOnlyTitle = False):

    print ("Constructing single page URL...")

    if _bIsReview:
        return ACM_BuildReviewURL(_filename, _bUseOnlyTitle)

    useYear = True
    if useYear:
        searchurl = sBaseString + sConnectChar + AfterStartMonth + sConnectChar + AfterStartYear + sConnectChar + ResearchArticleOnly + sConnectChar  
    else: 
        searchurl = sBaseString + sConnectChar + ResearchArticleOnly + sConnectChar + Expand + sConnectChar
        
    if _bUseOnlyTitle:
        searchurl += "AllField=Title%3A("
    else:
        searchurl += "AllField=(" # ([

    with open(_filename) as csv_file:
        df = csv.reader(csv_file, delimiter=',')
        df = list(df)
        for row in df:
            #print(row)
            #print ("Adding... " + str(row))
            searchurl += "("
            searchurl = ACM_AddMiddlePartForSearchURL(searchurl, "+OR+", row, _bUseOnlyTitle)
            
            searchurl += "+AND+"        

        searchurl = searchurl[:len(searchurl)-5]
        #print (searchurl)
        #print (len(searchurl))

        searchurl += ")" #)

        print ("Final short page URL: " + searchurl)  
    return searchurl

def IEEE_QueryBuilderRow(_searchTerm, _row, isNotLast):
    _searchTerm += "("
    # add except last term in row to final term
    for term in _row[:-1]:
        _searchTerm += "\"" + term + "\"" + " OR "
        
    # add last term in row to final term
    _searchTerm += "\"" + _row[-1] + "\""

    #close current row
    _searchTerm += ")"

    #do only if next is true
    if isNotLast:
        _searchTerm += " AND "

    return _searchTerm

def IEEE_QueryTermBuilder(_filename):
    searchTerm = ""

    with open(_filename) as csv_file:
        df = csv.reader(csv_file, delimiter=',')
        df = list(df)
        dfiter = iter(df)

        for row in df[:-2]:
            #print(row)              
            searchTerm = IEEE_QueryBuilderRow(searchTerm, row, True)

        searchTerm = IEEE_QueryBuilderRow(searchTerm, df[-1], False)
        searchTerm += ""   

        #print (searchTerm)
    return searchTerm   

def QuoteWord(_word):
    quoteChar = "\""
    return quoteChar + _word + quoteChar

def GoogleScholar_QueryTermBuilder(_filename, _bIsReview):
    searchTerm = "("

    with open('SearchTerms.csv') as csv_file:
        df = csv.reader(csv_file, delimiter=',')
        df = list(df)
        dfiter = iter(df)

        for term in df[:-1]:
            #searchTerm += "\"" + term + "\"" + " OR "
            #print (term)

            searchTerm += "("
    
            for word in term[:-1]:
                searchTerm += QuoteWord(word)
                searchTerm += " OR "
                #print (word)

            searchTerm += QuoteWord(term[len(term)-1])

            searchTerm += ") AND "

        searchTerm += "("
        lastTerm = df[-1]
        for word in lastTerm[:-1]:
                searchTerm +=  QuoteWord(word)
                searchTerm += " OR "
                #print (word)
        searchTerm += QuoteWord(lastTerm[len(term)]) 
        searchTerm += ")"
    searchTerm += ")"

    print (searchTerm)
    return searchTerm

def GetQueryTerm(_provider, _filename, _bIsReview = False, _bUseOnlyTitle = False):
    if _provider == "ACM":
        return ACM_QueryTermBuilder(_filename, _bIsReview, _bUseOnlyTitle)
    elif _provider == "IEEE":
        return IEEE_QueryTermBuilder(_filename)
    elif _provider == "GoogleScholar":
        return GoogleScholar_QueryTermBuilder(_filename)
    else:
        print("Unknown provider. Sry my frien'!")

def SimplyGetACMIDontCareAnymore(_searchTerm):
    res = ""

    res += sBaseString
    res += _searchTerm




    res += sEndString

    return res

#################################################################


