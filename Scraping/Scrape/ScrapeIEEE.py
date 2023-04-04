import json
from os import read
from re import search
import xplore

import pprint as pp

import ScrapeHelper

def GetRecord(_item):
    title = _item['title']
    #print(title)
    
    authors = "" 
    #authors = _item['authors'] #TODO naive way, needs to be improved!
    for author in _item['authors']['authors']:
        #print (author['full_name'])
        authors += author['full_name'] + ','

    year = _item['publication_year']
    #print(_item['publication_date'])

    if 'doi' in _item:
        doi = "https://doi.org/"+_item['doi']
    else: 
        doi = ""
    #print(doi)

    citationcount = _item['citing_paper_count']
    #print(citationcount)

    publicationtitle = _item['publication_title']
    #print(publicationtitle)

    try:       
        abstract = _item['abstract']
    except Exception as e:
        print(_item)
        print(e)
        abstract =""
    #print(abstract)
    
    finalRecord = [title, authors, year, publicationtitle, citationcount, doi, abstract]
    #print (finalRecord)
    return finalRecord 

def GetQuery(_queryString):
        
    with open("./Scrape/IEEExploreAPIKey.txt", "r", encoding="utf-8") as f:
        apikey = f.readlines()
        f.close()
    #print (apikey[0])
    query = xplore.xploreapi.XPLORE(apikey[0])
    
    #queryString = "10.1109/ACCESS.2019.2906394"
    query.queryText(_queryString)

    return query

def GetResultsFromIEEExploreOnline(_yearFilter,  _searchtermFilename):

    print ("Building query string...")
    queryString = ScrapeHelper.GetQueryTerm('IEEE', _searchtermFilename)

    print ("Building final query...")
    query = GetQuery(queryString)

    if _yearFilter[2]:
        query.resultsFilter('start_year', _yearFilter[0])
        query.resultsFilter('end_year', _yearFilter[1])
        print ('Searching from year ' + _yearFilter[0] + ' to ' + _yearFilter[1])

    query.resultsFilter('content_type', "Conferences,Journals")
    query.maximumResults(200)

    print ("Doing an ONLINE search using \n\t" + queryString)
    data = query.callAPI()  
    
    return data

def GetResultsFromIEEExploreOffline(offlineFileFilename):

    print ("Doing and OFFLINE search using " + offlineFileFilename)
    with open(offlineFileFilename, "r", encoding="utf-8") as f:
        data = f.readline()
        f.close()   

    #data = data.replace("\'", "\"")

    return data

def clean_year(_item):
    #pp.pprint(_item)

    time = _item['publication_date']
    #print(_item['publication_date'])
    year = ScrapeHelper.clean_year(time)
    _item['publication_date'] = year
    return _item
    

def FillDBFromData(_IEEEJSONdata):
    DB = []
    count = 0
    print("Total records found: " + str(_IEEEJSONdata['total_records']))
    for item in _IEEEJSONdata['articles']:
        #pp.pprint(item)

        #item = clean_year(item)
        #print (str(count))

        #pp.pprint(item)
        count +=1
        DB.append(GetRecord(item))

    return DB

def GetDB(_useOnline, _yearFilter, _searchtermFilename, _prefix1, _prefix2):
    
    IEEEdata = ""
    tmpTotalRecords = 0
    tmpArticles = []

    if _useOnline:
        currYear = _yearFilter[0]      
        while currYear <= _yearFilter[1]:
            IEEEdata = GetResultsFromIEEExploreOnline([str(currYear), str(currYear), True], _searchtermFilename)
            IEEEdata = json.loads(IEEEdata) # convert response from byte to json          

            #print (len(IEEEdata))

            #print (IEEEdata)

            if len(IEEEdata) >2:
                tmpArticles += IEEEdata['articles']
            tmpTotalRecords += IEEEdata['total_records']
            print ('Found ' + str(len (tmpArticles)) + ' articles.')

            if (IEEEdata['total_records']) > 199:
                print ('Warning! To many results per query!')
            
            currYear += 1
            IEEEJSONdata = IEEEdata

        IEEEJSONdata['articles'] = tmpArticles
        IEEEJSONdata['total_records'] = tmpTotalRecords

        print("Writing backup files...")
        prefix = _prefix1 + _prefix2
        s = json.dumps(IEEEJSONdata)
        open(prefix + ScrapeHelper.GetNowString() + '_data.json','w').write(s)
        print("Done writing backup files!")

    else:
        print ("Retrieving latest json file...")
        filename = ScrapeHelper.GetMostRecentFile(_prefix1, 'json')
        print ('Latest file is ' + filename)

        print('Loading json...')
        IEEEJSONdata = json.loads(GetResultsFromIEEExploreOffline(filename))
        print('Got my json object...')

    print("Total records found: " + str(IEEEJSONdata['total_records']))

    DB = FillDBFromData(IEEEJSONdata)

    return DB

def GetPapers(_useOnline = False):  
    useOnline = _useOnline

    startYear = 2023
    stopYear = 2023
    useYearFilter = True
    yearFilter = [startYear, stopYear, useYearFilter]

    searchtermFilename = './Scrape/SearchTerms.csv'
    
    prefix1 =  "./Results/IEEE/" 
    prefix2 =  "IEEE__Papers__" 

    DB = GetDB(useOnline, yearFilter, searchtermFilename, prefix1, prefix2)

    if useOnline:
        ScrapeHelper.WriteDBToCSV(DB, prefix1 + prefix2 + ScrapeHelper.GetNowString() + "_DB.csv", ) 

###################################################################
###################################################################
###################################################################



GetPapers(_useOnline = True) 
#GetReviews(_useOnline = True)
