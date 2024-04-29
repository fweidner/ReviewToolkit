from operator import truediv
from tkinter import *
from tkinter import messagebox
import json
import webbrowser
import re
import time 
import random
import csv

import DataHandler

class Controller:

    def __init__(self):
        print('creating controller...')
        self.my_data_handler = DataHandler.DataHandler()

        input_file = ""
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            input_file = json_data['input_file']
        self.my_data_handler.init(input_file)

        self.do_sanity_check_for_columns_and_review_elements()

        self.set_meta_info_keys()

        self.my_data_handler.print_count()       

    def set_meta_info_keys(self):
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            self.key_abstract = json_data['keys']['abstract']
            self.key_url = json_data['keys']['url']
            self.key_title = json_data['keys']['title']
            self.key_year = json_data['keys']['year']
           
    def do_sanity_check_for_columns_and_review_elements(self):
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            review_elements = json_data['keys']['review_elements']

        tmp = self.my_data_handler.get_header_of_input_file() #it's a dict not a list
        print (tmp)

        wrong_items_list = []
        result_per_review_element = TRUE
        for item in review_elements:
            current_review_element = review_elements[item]#.replace(" ", "_")
            current_review_element = str.lower(review_elements[item])#.replace(" ", "_")

            if item in tmp:
                print ("yay:" + str(item) + " is there.")
                continue
            else:
                print (current_review_element)
                print (item)
                print (tmp)
                print ("U fckd up!")
                result_per_review_element = FALSE
                wrong_items_list.append(item + " - " + review_elements[item] )
        
        if not result_per_review_element:
            
            error_message = "Sorry, the following elements from JSON are not in the CSV: \n\n"
            error_message += str(wrong_items_list) 
            error_message += "\n\nYou have to update the CSV manually bc someone was to lazy to implement it."
            error_message += "\n\nSimply add \"population;intervention;comparison;outcomes;context;checklater;include\" to your csv (with correct delim, here \";\").)"
            error_message += "\n\nProceed with caution."

            print(error_message)


            messagebox.showerror("Error", error_message)#HACK that's not very controller-ish

    def set_row_index_count_string(self, _stringvar):
        res = self.get_row_index_count_string()
        _stringvar.set(res)

    def get_row_index_count_string(self):        
        total_items = self.get_count(False)
        current_row_index = self.get_row_index()
        res = "Entry " + str(current_row_index+1) + " out of " + str(total_items) 
        return res

    def get_count(self, _print = False):
        return self.my_data_handler.print_count(_print)

    def get_row_index(self):
        return self.my_data_handler.get_row_index()

    def set_new_abstract(self, tmp, _tf_abstract):        
        _tf_abstract.delete(1.0, END)

        abstract = tmp[self.key_abstract]

        abstract = self.clean_abstract(abstract)

        _tf_abstract.insert(1.0, abstract)

    def set_new_title(self, tmp, _tf_title):
        _tf_title.delete(1.0, END)
        _tf_title.insert(1.0, tmp[self.key_title])

    def set_new_entry_url(self, tmp, _entry_url):
        _entry_url.delete(0, END)
        _entry_url.insert(0, tmp[self.key_url])
        
        self.current_url = tmp[self.key_url]


        doiprefix = "https://doi.org/"
        if "http" not in self.current_url: #I'm too lazy too parse, if it's not a doi, you're on your own.
            self.current_url = doiprefix + tmp[self.key_url]
        else: 
            self.current_url = tmp[self.key_url]
        # if len(self.current_url) > 45:
        #     _entry_url['text'] = self.current_url[0:45] + "..."
        # else:
        #     _entry_url['text'] = self.current_url

    def set_review_items(self, tmp, _review_elements_list):
        for item in tmp: # from file
            for list_element in _review_elements_list:  # from app
                #print (item.replace("_", " ") + " vs " + str(list_element[0]) )
                if item.replace("_", " ") == list_element[0]:
                    #print(str(tmp[item]))
                    if tmp[item] == "1" or tmp[item] == 1 or tmp[item]==1.0 or tmp[item] == "1.0":
                        list_element[2].select()
                        list_element[1].set(1)
                    else:
                        #print ('nay')
                        list_element[2].deselect()
                        list_element[1].set(0) 

                #else:
                #    print ('nay')

    def set_new_year(self, tmp, _tf_year):
        _tf_year.delete(0, END)
        _tf_year.insert(0, tmp[self.key_year])

    ##########
    # update current
    def update_current_item_in_file(self, _tf_abstract, _tf_title, _review_elements_list, _tf_year, _tf_doi):
        abstract = _tf_abstract.get(1.0, END)
        title = _tf_title.get(1.0, END)
        year = _tf_year.get()
        doi = _tf_doi.get()

        self.my_data_handler.update_current_item_in_file(abstract, title, _review_elements_list, year, doi)
        #print (text_from_textfield)

    ##########
    # set prev/next item
    def set_single_item(self, tmp, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year):
        if tmp != -1:
            #print(str(tmp))
            self.set_new_abstract(tmp, _tf_abstract)
            self.set_new_title(tmp, _tf_title)
            self.set_new_entry_url(tmp,_entry_url)
            self.set_new_year(tmp, _tf_year)

            self.set_review_items(tmp,_review_elements_list)
        else:
            self.my_data_handler.reset_reader()
    
    def set_next_item(self, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year, _iterator_options):
        
        tmp = self.get_next_or_prev_per_condition(False, _iterator_options)

        self.set_single_item(tmp, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year)

    def set_prev_item(self, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year, _iterator_options):

        tmp = self.get_next_or_prev_per_condition(True, _iterator_options)

        self.set_single_item(tmp, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year)
    
    def set_specific_item(self, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _row_index, _tf_year):
        
        tmp = self.my_data_handler.get_specific_item(_row_index)
        
        self.set_single_item(tmp, _tf_abstract, _tf_title, _entry_url, _review_elements_list, _tf_year)       

    ##########
    # save operations
    def save(self):
        print('save')
        self.my_data_handler.save_tmp_file()

    def do_swap_save(self):
        print("swap_save")
        self.my_data_handler.swap_save()

    def open_url(self, _entry_url):
        
        print ('controller open url:' + _entry_url.get())  
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            browser_path = json_data['browser']
        url = self.current_url 
        webbrowser.register('browser',
	        None,
	        webbrowser.BackgroundBrowser(browser_path))
        webbrowser.get('browser').open(url)

    def do_exit(self, _result, _text_abstract, _entry_title, _entry_url, _review_element_list, _entry_year):
        if _result is None:
            print ("Yes, do some more work!")
            return False
        elif _result is False:
            print ("Do nothing!? Dangerino!")
            return True
        else:
            print ("dosave stuff")
            self.update_current_item_in_file(_text_abstract, _entry_title, _review_element_list, _entry_year, _entry_url)
            self.do_swap_save()
            return True

    def clean_abstract(self, _tmp_abstract):

        tmptext = _tmp_abstract.replace("\n", " ")        

        tmptext = re.sub(r'\s+', " ", tmptext)

        tmptext = _tmp_abstract.lstrip()

        return tmptext



#########################
# STATS WINDOW ##########
#########################

    #BUG: tbh, that has nothing to do here. 
    def get_stats(self, _stats_window):
        valuelist = self.my_data_handler.get_stats()

        #for item in valuedict:
        #    label = Label(_stats_window, text =str(item) + ":" + str(valuedict[item]))
        #    label.pack(side=LEFT)

        frame_table = Frame(_stats_window)
        frame_table.pack(side=LEFT, padx=5)
  

        width = 2
        for i in range(len(valuelist)): #Rows
            for j in range(width): #Columns
                b = Entry(frame_table, text="")
                b.insert(END, valuelist[i][j])
                b.grid(row=i, column=j)


#########################
# SELECTIVE ITERATOR ####
#########################

    def get_new_item(self, _b_is_prev):
        if _b_is_prev:
            tmp = self.my_data_handler.get_prev_item()
        else:
            tmp = self.my_data_handler.get_next_item()

        return tmp

    def search(self, _tmp):
        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            searchTerm = json_data['searchTerm'].lower()
            #print (searchTerm)          
        #print(_tmp['title'])
        if searchTerm not in _tmp['title'].lower() and searchTerm not in _tmp['abstract'].lower():
            #print("term not found")
            return False
        else:
            return True
            #print("term found")

    #TODO refactor this as it is a messy dump of spaghetti!
    def get_next_or_prev_per_condition(self, _b_is_prev = False, _iterator_options=[]):
    

        current_index = self.my_data_handler.get_row_index()
        current_item = self.my_data_handler.get_specific_item(current_index)
        N = self.get_count()
        n = 0

        show_only_maybe = _iterator_options[0].get()
        show_only_include = _iterator_options[1].get()
        show_only_filtered = _iterator_options[2].get()
        show_only_not_include = _iterator_options[3].get()
        show_only_not_mobile_ar = _iterator_options[4].get()
        show_only_empty = _iterator_options[5].get()

        b_need_new_item = True

        while (b_need_new_item):
            #print("get item # " + str(self.my_data_handler.get_row_index()))
            b_need_new_item = False

            # get an initial item that we can check 
            tmp = self.get_new_item(_b_is_prev)
            
            # get our keys that we use in the csv file (basically the column names)
            with open('config.json', 'r') as json_file:
                json_data = json.load(json_file)
                key_include = json_data['keys']['review_elements']['include']
                key_maybe = json_data['keys']['review_elements']['checklater']
                key_mobile_ar = json_data['keys']['review_elements']['population']
                key_intervention = json_data['keys']['review_elements']['intervention']
                key_comparison = json_data['keys']['review_elements']['comparison']
                key_context = json_data['keys']['review_elements']['context']
                key_outcomes = json_data['keys']['review_elements']['outcomes']
                #if you add more than picoc, use them here.
                
            # init our bool values that actually indicate if an item (tmp) is tagged with maybe or include
            b_is_include = bool(int(float(tmp[key_include])))
            b_is_mobile_ar = bool(int(float(tmp[key_mobile_ar])))
            b_is_intervention = bool(int(float(tmp[key_intervention])))
            b_is_comparison = bool(int(float(tmp[key_comparison])))
            b_is_context = bool(int(float(tmp[key_context])))
            b_is_maybe = bool(int(float(tmp[key_maybe])))
            b_is_outcomes = bool(int(float(tmp[key_outcomes])))
            
            b_is_as_filter = self.search(tmp) 

            # set the bool values so that we can determine which filter we apply
            if show_only_maybe and not b_is_maybe:
                b_need_new_item = True
            if show_only_include and not b_is_include:
                b_need_new_item = True
            if not b_need_new_item and show_only_not_include and b_is_include:
                b_need_new_item = True
            if not b_need_new_item and show_only_filtered and not b_is_as_filter:
                b_need_new_item = True
            if not b_need_new_item and show_only_not_mobile_ar and not b_is_mobile_ar:
                b_need_new_item = True
            if not b_need_new_item and show_only_empty:
                if b_is_mobile_ar or b_is_outcomes or b_is_intervention or b_is_comparison or b_is_context or b_is_include or b_is_maybe:
                    b_need_new_item = True
               
            n = n + 1
            if n > N:
                self.alert("Warning", "No item found", "warning")
                return current_item
        
        return tmp


############################################################################################


    def export_items_to_csv(self):
        print("export items")

        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            review_elements_from_json = json_data['percentage_of_items_to_export']
        
        review_elements_from_json = int(review_elements_from_json)
        print (str(review_elements_from_json))

        length = self.my_data_handler.print_count()
        num_items_to_export = int((length*review_elements_from_json)/100)

        randoms = random.sample(range(1, self.my_data_handler.print_count()), num_items_to_export)
        print (str(len(randoms)))

        res = []

        # get the header items
        one_article = self.my_data_handler.get_specific_item(1)
        res.append(one_article)

        # get the random items
        for item in randoms:
            one_article_as_dict = self.my_data_handler.get_specific_item(item)
            row = []
            for item2 in one_article_as_dict:
                row.append(one_article_as_dict[item2])
                #res.append(list())

            #print(row)
            res.append(row)
            #res[item] = self.my_data_handler.get_specific_item(item)

        #print(res)      

        with open('config.json', 'r') as json_file:
                    json_data = json.load(json_file)
                    file_for_irr = json_data['file_for_irr']
        with open(file_for_irr, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(res)

        print("Export done.")

    def export_includes_to_csv(self):
        print("Exporting includes...")

        includes = self.my_data_handler.get_all_includes()

        with open('config.json', 'r') as json_file:
                json_data = json.load(json_file)
                filename_for_includes = json_data['filename_with_includes']
                filepath_for_includes = json_data['filepath_with_includes']
        

        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d_%H-%M", t)
        print(current_time)

        final_dest = filepath_for_includes + str(current_time) + "-" + filename_for_includes

        print (final_dest)

        with open(final_dest, "w", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f,delimiter =';', fieldnames=self.my_data_handler.get_header_of_input_file())
                writer.writeheader()
                writer.writerows(includes)

        print("Exporting done.")

    def do_deprecated(self):
        time.sleep(5)
        print ("DEPRECATED")


    def alert(self, title, message, kind='info', hidemain=True):
        if kind not in ('error', 'warning', 'info'):
            raise ValueError('Unsupported alert kind.')

        show_method = getattr(messagebox, 'show{}'.format(kind))
        show_method(title, message)