from operator import concat
import pandas as pd
from datetime import date
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import ScrapeHelper as Helper

def GetNoDuplicateCSV(_first_pass_df, _second_pass_df):
    # _df['keywords'] = _df['title']

    print(len(_first_pass_df))
    print(len(_second_pass_df))
    concatRes = pd.concat([_first_pass_df, _second_pass_df]).drop_duplicates(subset=['doi'])
    print(len(_first_pass_df))
    print(len(_second_pass_df))
    
    diff = len(concatRes) - len(_first_pass_df)
    print ("Diff: " + str(diff))
    print(len(concatRes))

    return concatRes

def write_file(_df, _filepath, _filename):
    _df.to_csv(_filepath + Helper.GetNowString() + _filename, sep=";", index=None)
    
########################################################
#### Program start                                   ###
########################################################

# # inputFile = r'../Results/Review/2022-06-15_13-47_AllSurveys.csv' #surveys
# first_pass_filepath = r'../Results/Paper/2022-06-24_14-27-AllPapers-unique-clean.csv'
# second_pass_filepath = r'../Results/Paper/2022-08-18_11-44-AllPapers_second-pass-unique-clean.csv'
# first_pass_df = pd.read_csv(first_pass_filepath, sep=";")
# second_pass_df = pd.read_csv(second_pass_filepath, sep=";")



# res = GetNoDuplicateCSV(first_pass_df, second_pass_df)
# write_file(res, '../Results/Paper/', Helper.GetNowString() + '-NewIncludes.csv')

