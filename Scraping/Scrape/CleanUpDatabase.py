import pandas as pd
import numpy as np

import ScrapeHelper as Helper


def make_to_int(_df):
    _df['year'] = _df['year'].fillna(0)
    _df = _df.astype({'year':'int','citationcount':'int'})
    return _df


def add_final_columns_for_toolkit(_df):

    _df["population"] ="0"
    _df["intervention"] ="0"
    _df["comparison"] ="0"
    _df["outcomes"] ="0"
    _df["context"] ="0"
    _df["checklater"] ="0"
    _df["include"] ="0"

    return _df

##########################################################

# path = "./Results/"
# input_file = "2023-04-04_12-45_All" 
# input_file_ext = ".csv"

# df = pd.read_csv(path + input_file + input_file_ext, sep=";", quoting=2)
# df = make_to_int(df)
# df = add_final_columns_for_toolkit(df) #this one is extremely important!

# # print (df.head())

# new_input_file = input_file + "-Clean" + input_file_ext
# df.to_csv(path + new_input_file, sep=";", index=None)