import csv
import json
import shutil
from datetime import datetime
import os

class DataHandler():

    def __init__(self):
        self.row_index = -1
        print ('init')

    def init(self, _file):

        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            key_abstract = json_data['keys']['abstract']
            key_title = json_data['keys']['title']
            key_year = json_data['keys']['year']

        print('creating data handler...')
        self.csv_file = open(_file, 'r', encoding='utf-8')
        csv_data = csv.DictReader(self.csv_file, delimiter=self.get_root_val_from_config(["delimiter"]))
        self.my_csv_data = csv_data
        print('opened file')

        self.convert_to_list()
        
        self.csv_file.close()

    def get_root_val_from_config(self, _keys):
        res = ""
        if len(_keys) == 1:
            with open('config.json', 'r') as json_file:
                json_data = json.load(json_file)
                res = json_data[_keys[0]]
        else: 
            print ("Key error in get_root_val_from_config")
        print("using " + res + " as delimiter.")
        return res;


    def convert_to_list(self):
        self.my_csv_data_list = []
        for row in self.my_csv_data:
            self.my_csv_data_list.append(row)
        #print (len(self.my_csv_data_list))

    def print_count(self, _print = False):
        count = len(self.my_csv_data_list)
        if _print:
            print (str(count))
        return count
        
    def get_row_index(self):
        return self.row_index
    
    def update_current_item_in_file(self, _abstract, _title, _review_elements_list, _tf_year):
        if self.row_index == -1: # we do this because it otherwise overwrites the log
            return

        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            key_abstract = json_data['keys']['abstract']
            key_title = json_data['keys']['title']
            key_year = json_data['keys']['year']

        self.my_csv_data_list[self.row_index][key_abstract] = _abstract.rstrip()
        self.my_csv_data_list[self.row_index][key_title] = _title.rstrip()
        self.my_csv_data_list[self.row_index][key_year] = _tf_year.rstrip()

        for list_element in _review_elements_list:
            #print ("\t" + str(list_element))
            #print ("\t" + str(list_element[1].get()))
            self.my_csv_data_list[self.row_index][list_element[0].replace(" ", "_").rstrip()] = list_element[1].get()
        
    def get_next_item(self):
        #print (str(self.row_index))
        self.row_index += 1
        if self.row_index >= len(self.my_csv_data_list):
            self.row_index = 0

        tmp = self.my_csv_data_list[self.row_index]
        #print (tmp)

        return tmp

    def get_prev_item(self):
        #print('prev')

        #print (str(self.row_index))
        self.row_index -= 1
        if self.row_index < 0:
            self.row_index = len(self.my_csv_data_list)-1

        tmp = self.my_csv_data_list[self.row_index]
        #print (tmp)

        return tmp

    def get_specific_item(self, _index):
        print( 'get specific')
        self.row_index = _index

        tmp = self.my_csv_data_list[self.row_index]

        return tmp

    def save_tmp_file(self):
        tmp_file = ""
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            tmp_file = json_data['tmp_file']

        with open(tmp_file, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = self.my_csv_data_list[0]

            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter= self.get_root_val_from_config(["delimiter"]))
            dict_writer.writeheader()
            for item in self.my_csv_data_list[0:]:
                #print (item)
                dict_writer.writerow(item)        
    
    def swap_save(self):
        tmp_file = ""
        input_file = ""

        #get file names
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            input_file = json_data['input_file']

        #create a backup of the old file
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d-%H-%M")
        src = input_file
        dst = "Backup/" + current_datetime +".csv"
        shutil.copyfile(src, dst)

        with open(input_file, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = self.my_csv_data_list[0]
            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter= self.get_root_val_from_config(["delimiter"]))
            dict_writer.writeheader()
            for item in self.my_csv_data_list[0:]:
                #print (item)
                dict_writer.writerow(item)        
        
    def get_header_of_input_file(self):
        # return self.my_csv_data_list[0]
        return self.my_csv_data.fieldnames
    
    def get_stats(self):

        count_include = 0
        count_check_later = 0
        count_mobile_ar = 0
        count_total = len(self.my_csv_data_list)
        tmp = 0
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            key_include = json_data['keys']['review_elements']['include']
            key_check_later = json_data['keys']['review_elements']['checklater'].replace(" ", "_")
            key_mobile_ar = json_data['keys']['review_elements']['population'].replace(" ", "_")


            for item in self.my_csv_data_list:
                tmp += 1
                print (tmp)

                do_include = item[key_include]
                if do_include != "":
                    if int(float(do_include)) == 1:
                        count_include +=1

                do_checklater = item[key_check_later]
                if do_checklater != "":
                    if int(float(do_checklater)) == 1:
                        count_check_later += 1

                do_mobile_ar = item[key_mobile_ar]
                if do_mobile_ar != "":
                    if int(float(do_mobile_ar)) == 1:
                        count_mobile_ar +=1

        count_invalid = count_total - count_include - count_check_later

        print (str(count_total))
        print (str(count_invalid))
        print (str(count_include))
        print (str(count_check_later))
        print (str(count_mobile_ar))

        valuedict = {"count_total": count_total, "count_invalid":count_invalid, "count_include":count_include, "count_check_later":count_check_later}
        valuelist = [["count_total", count_total], ["count_invalid", count_invalid], ["count_include", count_include], ["count_check_later", count_check_later], ["count_mobile_ar", count_mobile_ar]]
        #print (str(valuedict))

        return valuelist

    def get_all_includes(self):

        res = []

        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            key_include = json_data['keys']['review_elements']['include']

        for item in self.my_csv_data_list:
            if int(float(item[key_include])) == 1:
                #print(item)
                res.append(item)

        print("Found " + str(len(res)) + " items with include.")

        return res