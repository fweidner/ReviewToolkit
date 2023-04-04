import pandas as pd
from datetime import date
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import ScrapeHelper as Helper
########################################################pythonimpo
#### Helpers                                         ###
########################################################

def identify_tokens(row):
    tokens = nltk.word_tokenize(row)
    # taken only words (not punctuation)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words


def remove_stops(row, thestops):
    my_list = row
    meaningful_words = [w for w in my_list if not w in thestops]
    return (meaningful_words)

def rejoin_words(row):
    joined_words = ( " ".join(row))
    return joined_words

def create_keywords(_df, _source_key = "title", _key = "keywords"):
    _df[_key] = _df[_source_key].str.lower()

    # tokenize and exclude non-alphanumeric in title
    stemming = PorterStemmer()
    _df[_key] = _df[_key].apply(identify_tokens, stemming)

    # remove stopwords in title
    stops = set(stopwords.words("english"))    
    _df[_key] = _df[_key].apply(remove_stops, thestops = stops)
    
    #remove duplicate entries based on title and year
    _df[_key] = _df[_key].apply(rejoin_words)


########################################################
#### Core functions                                  ###
########################################################

def RemoveDuplicateEntriesFromDataframeBasedOnTitleAndYear(_df, _key = "title", _key2 = "year"):

    len_before = len(_df)

    _df[_key] = _df[_key].str.lower()

    # tokenize and exclude non-alphanumeric in title
    stemming = PorterStemmer()
    _df[_key] = _df[_key].apply(identify_tokens, stemming)

    # remove stopwords in title
    stops = set(stopwords.words("english"))    
    _df[_key] = _df[_key].apply(remove_stops, thestops = stops)
    
    #remove duplicate entries based on title and year
    _df[_key] = _df[_key].apply(rejoin_words)
    _df = _df.drop_duplicates(subset=[_key, _key2])

    #drop empty lines if title, year or author is NA; we allow empty fields in other columns
    _df = _df.dropna(subset=[_key, _key2, "authors"])

    len_after = len(_df)

    print(_df)

    print("Removed " + str(len_before-len_after) + " elements. New length: " + str(len(_df)))

    return _df

def RemoveDuplicateEntriesFromDataframeBasedOnDOI(_df):
    
    len_before = len(_df)
 
    _df = _df.drop_duplicates(subset=['doi'])

    len_after = len(_df)
    
    print("Removed " + str(len_before-len_after) + " elements. New length: " + str(len(_df)))

    return _df

def GetNoDuplicateCSV(_df, _filename, _filepath):
    _df['keywords'] = _df['title']
    dfNoDuplicateEntries = RemoveDuplicateEntriesFromDataframeBasedOnTitleAndYear(_df, "keywords")
    dfNoDuplicateEntries = RemoveDuplicateEntriesFromDataframeBasedOnDOI(dfNoDuplicateEntries)
    # Helper.SafeDataFrameToCSV(dfNoDuplicateEntries, _filename, _filepath)

    dfNoDuplicateEntries.to_csv(_filepath + Helper.GetNowString() + _filename, sep=";", index=None)

########################################################
#### Program start                                   ###
########################################################

# # inputFile = r'../Results/Review/2022-06-15_13-47_AllSurveys.csv' #surveys
# inputFile = r'../Results/Paper/2022-08-18_11-42_AllPapers_second-pass.csv' #surveys

# GetNoDuplicateCSV(pd.read_csv(inputFile, sep=";"), _filename = "-AllPapers_second-pass-unique.csv", _filepath = r'../Results/Paper/')


