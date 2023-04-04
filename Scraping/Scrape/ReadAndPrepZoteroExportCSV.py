import pandas as pd

import RemoveDuplicates
import CleanUpDatabase
import RemoveNewOldArticles
import ScrapeHelper

_path = "../Results/Paper/"
_input = "2022-09-01_13-10_Snowballers.csv"

df = pd.read_csv(_path+_input, sep=",", quoting=2)
print(df.head())
print(df.columns)


# title	authors	year	publicationtitle	citationcount	doi	abstract	keywords	population	intervention	comparison	outcomes	context	checklater	include	justadevice	nicebutvr
#     col_list = ["Title", "Authors", "Year", "Source", "Cites", "DOI", "Abstract", "Type"]


df_new = df [["Title", "Author", "Publication Year", "Publication Title", "DOI", "Abstract Note"]]
df_new.rename(columns={"Title": "title", "Author":"authors", "Publication Year": "year", "DOI":"doi", "Publication Title": "publicationtitle", "Abstract Note": "abstract"}, inplace=True)
df_new["citationcount"] = "0"
#df_new["Type"] = "Article"


df_new = CleanUpDatabase.fill_doi(df_new)
df_new = CleanUpDatabase.make_to_int(df_new)
RemoveDuplicates.create_keywords(df_new)
df_new = CleanUpDatabase.add_final_columns_for_toolkit(df_new)



df_new.to_csv(_path +ScrapeHelper.GetNowString() + "-Snowballers-converted.csv", sep=";", index=None)




original_file = r'../Results/Papers-from-Survey/2022-08-23_13-16-with-survey-converted-with-doi-and-concat.csv'
original_file_df = pd.read_csv(original_file, sep=";")

df_new_concat = RemoveNewOldArticles.GetNoDuplicateCSV(original_file_df, df_new)

print(df_new_concat.head())
print(df_new_concat.columns)
df_new_concat.to_csv(_path + ScrapeHelper.GetNowString() + "-Snowballers-survey-scraping.csv", sep=";", index=None)


