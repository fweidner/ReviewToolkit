import requests                 #getting the search html page
from bs4 import BeautifulSoup   #html parsing
import re                       #regex
import pprint
import glob                     #get list of filenames

import ScrapeHelper



def GetHMTLDoc(_url):
    response = requests.get(_url)
    if response.ok:
        text = response.text
        print("Got file from ACM.")
        return text
    else:
        return "404"

def ScrapeSoup(_soup):

    regex = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Apr(?:il)?|Mar(?:ch)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) (?:19[7-9]\d|2\d{3})(?=\D|$)'

    resDB = []
    skippedItems = 0

    allSearchItems = _soup.find_all('li',{'class':'search__item issue-item-container'})
    print ("Items in soup: " + str(len(allSearchItems)))
    for item in allSearchItems:
    
        #print (item.text)

        #TypeOfWork
        typeOfWork = item.find('div',{'class':'issue-heading'}).text
        #print (typeOfWork)
        # if typeOfWork == "proceeding" or typeOfWork == "book":
            # skippedItems += 1
            # continue 
    
        
        #Title
        title = item.find('h5',{'class':'issue-item__title'}).text
        title = re.sub('\s+',' ', title) #delete a bunch of spaces
        #print(title)
        
        #DOI
        # not all items (even research-articles) have a DOI
        try:
            doi = item.find('a',{'class':'issue-item__doi'}).text
        except Exception as e:
            #print(e)
            doi = ""  
        #doi = doi.replace("https://doi.org/", "")
        #print(doi)

        itemDetail = item.find('div',{'class':'issue-item__detail'})
        if itemDetail is not None:
            itemSubDetail = itemDetail.find('span', {'class':'dot-separator'})
        else:
            itemSubDetail = item.find('span', {'class':'simple-tooltip__block--b'})

        try:
            year = itemSubDetail.find('span', text=re.compile(regex)).text
            year = year.replace(",", "")
            year = year.replace(" ", "")
            year = year[-4:]
        except Exception as e:
            print(itemSubDetail)
            print(e)
            year = ""  
        #print (year)
        
        #venue/publication
        if itemDetail is not None:
            publicationtitle = itemDetail.find('span', {'class':'epub-section__title'}).text
        else: 
            publicationtitle = ""
        #print(publicationtitle)

        #citation count
        citationcount = item.find('div',{'class':'citation'}).text
        citationcount = re.sub('[^0-9]','', citationcount)
        #print(citationcount)

        #authors
        #authors = item.find('ul', {'class':'rlist--inline loa truncate-list'}).text
        try:
            authors = item.find('ul', {'class':'rlist--inline loa truncate-list'}).text
            authors = re.sub('\s+',' ', authors) #delete a bunch of spaces
            authors = list(authors.split(","))
        except Exception as e:
            print(e)
            print(item)
            authors = ""
            pass
        
        #print(authors)

        #TODO get abstract
        abstract = ""


        finalRecord = [title, authors, year, publicationtitle, citationcount, doi, abstract]
        #
        # pprint.pprint(finalRecord)
        resDB.append(finalRecord)

        #print("")
        #break
    return resDB

def GetAndScrapeHTMLDocsInBulk_test(_shorturl, _numSearchResults, _magicNumber, _prefix1, _prefix2):

        timeString = ScrapeHelper.GetNowString() 
        startPage = 0
        pageSize = _magicNumber
        DB = []
        
        while _numSearchResults > (pageSize*startPage):

            # construct new one page url
            startPageString = "&startPage=" + str(startPage)
            pageSizeString = "&pageSize=" + str(pageSize)
            longurl = _shorturl + startPageString + pageSizeString
            print ("Final long page URL for page " + str(startPage) + " (page size: " + str(pageSize) + ")" + ": " + longurl)  

            # get long single page html
            text = GetHMTLDoc(longurl)

            #create final soup
            soup = BeautifulSoup(text, "html.parser") #https://stackoverflow.com/questions/11804148/parsing-html-to-get-text-inside-an-element
            DBtmp = ScrapeSoup(soup)

            #concat DBs
            DB += DBtmp
            print(len(DB))

            #save HMTl so we don't get banned from ACM
            filepath = ScrapeHelper.getwd() + "/" + _prefix1 

            print (filepath)
            
            ScrapeHelper.WriteFile(text, filepath + "/ACM__" + _prefix2 +  timeString + "_" + str(pageSize*(1+startPage)) + ".html")

            startPage+=1

        return DB

def ProcessOfflineHTMLDocsInBulk(_basefilename):
    DB =[]
    print (_basefilename)
    filenamesList = glob.glob(_basefilename)
    print (str(filenamesList))
    for filename in filenamesList:
        print (filename)
        text = open(filename, "r", encoding="utf-8")
        soup = BeautifulSoup(text, "html.parser") #https://stackoverflow.com/questions/11804148/parsing-html-to-get-text-inside-an-element
        DB += ScrapeSoup(soup)

    print (len(DB))
    return DB

def GetDB(_useOnline, _searchTerm, _prefix1, _prefix2, _bIsReview = False, _bUseOnlyTitle = False, _useTextTerm = False):

    magicNumber = 100 #that is the single page layout we use that does not lead to a timeout.

    if _useOnline:

        #get the one-page default ACM URL for your search terms
        
        if (_useTextTerm):
            shortQueryURL = ScrapeHelper.SimplyGetACMIDontCareAnymore(_searchTerm)
        else:
            shortQueryURL = ScrapeHelper.GetQueryTerm("ACM", _searchTerm, _bIsReview, _bUseOnlyTitle)


        print (shortQueryURL)
        # get init default html page - it's a short one!
        text = GetHMTLDoc(shortQueryURL)

        #get num results
        soup = BeautifulSoup(text, "html.parser") #https://stackoverflow.com/questions/11804148/parsing-html-to-get-text-inside-an-element
        numSearchResults = soup.find('span',{'class':'result__count'}).text
        print(numSearchResults)

        # convert to int
        numSearchResults = ScrapeHelper.CleanMaxResultForACMURL(numSearchResults)

        #get the DB, if we need multiple requests, we do that.
        DB = GetAndScrapeHTMLDocsInBulk_test(shortQueryURL, numSearchResults, magicNumber, _prefix1, _prefix2)
      
    else:   
        offlinepath = ScrapeHelper.getwd() + "/" + _prefix1  + "/*"        
        DB = ProcessOfflineHTMLDocsInBulk(offlinepath)

    return DB

def GetPapers(_useOnline = False, _useTextTerm = False):

    useOnline = _useOnline
    input("Do we query ACM and risk to get banned? " + ("Yes!" if useOnline else "No") + "\n Proceed with caution. Press Enter to continue...")

    bIsReview = False   
    bUseOnlyTitle = False

    prefix1 = '.\Results\ACM'
    prefix2 = 'Paper__'

    if _useTextTerm:
        # searchTerms = '("Binocular Parallax" OR "Eye Dominance" OR "Dominant Eye" OR "Ocular Dominance" OR "Sighting Dominance") NOT animals NOT rats NOT monkeys NOT surgery NOT myopia NOT cortex NOT strabismus'  
        searchTerms = '("Binocular Parallax" OR "Eye Dominance" OR "Dominant Eye" OR "Ocular Dominance" OR "Sighting Dominance")' 
    else:
        searchTerms = '.\Scrape\SearchTerms.csv'

    DB = GetDB(useOnline, searchTerms, prefix1, prefix2, bIsReview,bUseOnlyTitle, _useTextTerm)

    if useOnline:
        ScrapeHelper.WriteDBToCSV(DB, prefix1 + "/ACM__" + prefix2 + ScrapeHelper.GetNowString() + "_DB.csv") 

############################################################################
############################################################################
############################################################################

#HACK year is defined in ScrapeHelper.py
_useOnline = True
_useTextTerm = True
GetPapers(_useOnline, _useTextTerm)
