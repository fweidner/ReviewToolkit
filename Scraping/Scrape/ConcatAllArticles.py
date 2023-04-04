import pandas as pd

import ScrapeHelper


def get_proper_file_from_PoP(_filepath):
    pop_file = _filepath

    col_list = ["Title", "Authors", "Year", "Source", "Cites", "DOI", "Abstract", "Type"]
    df = pd.read_csv(pop_file, usecols=col_list, sep=",")
    df = df[col_list]

    #HACK we drop reviews, notes, books, and so on here. we only use articles and conference papers
    before = len(df)
    df = df[(df.Type == "Article") | (df.Type == "Conference Paper")]
    df = df.drop(columns=['Type'])
    after = len(df)
    print ("Deleted " + str(before-after) + " items bc they were not conf papers or articles")

    
    col_list_new = ["title","authors","year","publicationtitle","citationcount","doi","abstract"]
    df.columns = col_list_new
    
    return df
    

def concatFiles(acm_file, ieee_file, pop_file, out_path):
    
    df_acm = pd.read_csv(acm_file, sep=';')
    df_ieee = pd.read_csv(ieee_file, sep=';') #here's a bug with the csv file
    df_pop = pop_file

    # res = pd.concat([df_acm, df_ieee, df_pop])
    res = pd.concat([df_acm, df_ieee])
    res.to_csv(out_path, index=None, sep=";")

def concatPapers():
    acm_file = "./Results/ACM/" + "Paper__2023-04-04_12-39_DB.csv"
    ieee_file = "./Results/IEEE/" + "IEEE__Papers__2023-04-04_12-43_DB.csv"
    # pop_file = get_proper_file_from_PoP( "../Results/Paper/" + "Scopus/" + "2022-08-18_PoPCites-Scopus.csv")
    pop_file = []

    out_path = ".//Results/" + ScrapeHelper.GetNowString() + "_All.csv"
    # concatFiles(acm_file, ieee_file, pop_file, out_path)
    concatFiles(acm_file, ieee_file, pop_file, out_path)


concatPapers()