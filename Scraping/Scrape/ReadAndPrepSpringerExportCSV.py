import pandas as pd

import RemoveDuplicates
import CleanUpDatabase
import RemoveNewOldArticles
import ScrapeHelper

_path = "F:\\OneDrive - Technische Universität Ilmenau\\Documents\\2022_Paper-AvatarSurvey_Data\\FW\\Springer\\"
_input = "2022-09-05_SearchResults.csv"

df = pd.read_csv(_path+_input, sep=",", quoting=2)
print(df.head())
print(df.columns)


# title	authors	year	publicationtitle	citationcount	doi	abstract	keywords	population	intervention	comparison	outcomes	context	checklater	include	justadevice	nicebutvr
#     col_list = ["Title", "Authors", "Year", "Source", "Cites", "DOI", "Abstract", "Type"]


df_new = df [["Item Title", "Authors", "Publication Year", "Publication Title", "Item DOI"]]
df_new.rename(columns={"Item Title": "title", "Authors":"authors", "Publication Year": "year", "Item DOI":"doi", "Publication Title": "publicationtitle"}, inplace=True)
df_new["citationcount"] = "0"
df_new["abstract"] = ""
#df_new["Type"] = "Article"


df_new = CleanUpDatabase.fill_doi(df_new)
df_new = CleanUpDatabase.make_to_int(df_new)
RemoveDuplicates.create_keywords(df_new)
df_new = CleanUpDatabase.add_final_columns_for_toolkit(df_new)



df_new.to_csv(_path + _input + "-converted.csv", sep=";", index=None)



#print(df_new_concat.head())
#print(df_new_concat.columns)
# df_new_concat.to_csv(_path + ScrapeHelper.GetNowString() + "-Snowballers-survey-scraping.csv", sep=";", index=None)


