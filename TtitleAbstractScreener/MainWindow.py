from enum import Flag
from os import TMP_MAX
from tkinter import * 
from tkinter import messagebox
import tkinter as tk
import csv
import sys
import json

import Controller

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        Text.__init__(self, *args, **kwargs)

        # https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._callback)

    def _callback(self, command, *args):
        cmd = (self._orig, command) + args
        
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None #HACK

        if command in ("configure"): #HACK
            self.event_generate("<<TextModified>>")

        return result
        
class MainWindow(Frame):  
    def __init__(self):
        super().__init__()

        self.my_controller = Controller.Controller()

        self.initUI()

        #self.my_controller = Controller.Controller()

    # Init function for GUI
    def initUI(self):

        self.master.title("Review-Tool")
        self.pack(fill=BOTH, expand=True)

        self.init_menubar()

        tmp_frame = self.init_url()

        # self.init_doi()
        
        self.init_core_elements()

        self.init_review_elements()

        self.init_buttons()

        self.init_global_keybinds(self.master)

        self.init_count(tmp_frame)

        self.set_font(16)

    def set_font(self, _newsize):
        self.font_size = _newsize
        Font_tuple = ("Calibri", self.font_size, "normal")
        self.text_abstract.configure(font = Font_tuple)
        self.entry_title.configure(font=Font_tuple)
        

    def init_menubar(self):
        # menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # file pane
        fileMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Save", command=self.do_swap_save)
        fileMenu.add_command(label="Exit", command=self.exit_program)
        
        
        #settings pane
        settingsMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Settings", menu=settingsMenu)     

        #settingsMenu.add_command(label="Increase Font Size (STRG + \"+\"", command=self.increase_fontsize)
        #settingsMenu.add_command(label="Decrease Font Size (STRG + \"-\"", command=self.decrease_fontsize)
        settingsMenu.add_command(label="Show stats", command=self.open_stats)
        settingsMenu.add_command(label="Export x % (config.json)", command=self.export_items)
        settingsMenu.add_command(label="Export Includes", command=self.export_includes)
        
        #settings pane
        self.iteratorMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Iterator", menu=self.iteratorMenu)     

        self.show_only_maybe = tk.BooleanVar()
        self.iteratorMenu.add_checkbutton(label = "show only maybe", onvalue=1, offvalue=0, variable=self.show_only_maybe,
             command=self.set_iterator_menu_status)

        self.show_only_include = tk.BooleanVar()
        self.iteratorMenu.add_checkbutton(label = "show only include", onvalue=1, offvalue=0, variable=self.show_only_include,
             command=self.set_iterator_menu_status)

        self.show_only_filtered = tk.BooleanVar()
        self.iteratorMenu.add_checkbutton(label = "show only search", onvalue=1, offvalue=0, variable=self.show_only_filtered,
             command=self.set_iterator_menu_status)

        self.show_only_not_include = tk.BooleanVar()
        self.iteratorMenu.add_checkbutton(label = "show only not include", onvalue=1, offvalue=0, variable=self.show_only_not_include,
             command=self.set_iterator_menu_status)

        self.show_only_not_mobile_ar = tk.BooleanVar()        
        self.iteratorMenu.add_checkbutton(label = "show only not population", onvalue=1, offvalue=0, variable=self.show_only_not_mobile_ar,
             command=self.set_iterator_menu_status)

        self.show_only_empty = tk.BooleanVar()        
        self.iteratorMenu.add_checkbutton(label = "Show only empty", onvalue=1, offvalue=0, variable=self.show_only_empty,
             command=self.set_iterator_menu_status)

        # about pane
        aboutMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Help", menu=aboutMenu)

        aboutMenu.add_command(label="About", command=self.show_about)
        aboutMenu.add_command(label="Keyboard shortcuts", command=self.show_keyboard_shortcuts)

    def init_core_elements(self):

        # year
        frame_year = Frame(self)
        frame_year.pack(fill=X)

        lbl_year = Label(frame_year, text="Year", width=6)
        lbl_year.pack(side=LEFT, padx=5, pady=5)

        self.entry_year = Entry(frame_year)
        self.entry_year.pack(fill=X, padx=5, expand=True)

        #####################
        # title
        frame_title = Frame(self)
        frame_title.pack(fill=X)

        lbl_title = Label(frame_title, text="Title", width=6)
        lbl_title.pack(side=LEFT, padx=5, pady=5)

        # self.entry_title = Entry(frame_title)
        # self.entry_title.pack(fill=X, padx=5, expand=True)
        self.entry_title = Text(frame_title, wrap=tk.WORD, height=2)
        scroll_y = tk.Scrollbar(frame_title, orient="vertical", command=self.entry_title.yview)
        scroll_y.pack(side="right", fill="y")
        self.entry_title.configure(yscrollcommand=scroll_y.set)
        self.entry_title.pack(fill=BOTH, side=LEFT, padx=5, expand = True)

        #####################
        # abstract
        frame_abstract = Frame(self)
        frame_abstract.pack(fill=BOTH, expand=True)
        frame_abstract.pack_propagate(0)
        
        lbl_abstract = Label(frame_abstract, text="Abstract", width=6)
        lbl_abstract.pack(side=LEFT, anchor=N, padx=5, pady=5)
        
        self.text_abstract = CustomText(frame_abstract, wrap=WORD)
        self.text_abstract.bind("<Tab>", self.focus_next_widget)
        self.text_abstract.bind("<Shift-Tab>", self.focus_prev_widget)
        self.text_abstract.bind("<<TextModified>>", self.onModification)
        
        scroll_y = tk.Scrollbar(frame_abstract, orient="vertical", command=self.text_abstract.yview)
        scroll_y.pack(side="right", fill="y")
        self.text_abstract.configure(yscrollcommand=scroll_y.set)

        self.text_abstract.pack(fill=BOTH, side=LEFT, pady=5, padx=5, expand=True)


    def init_buttons(self):
         #frame buttons
        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        btn_openurl = Button(frame_buttons, text="Open URL", command=self.open_url)
        btn_openurl.pack(side=RIGHT, padx=5, pady=5)

        btn_next = Button(frame_buttons, text="Next", command=self.clickButtonNext)
        btn_next.pack(side=RIGHT, padx=5, pady=5)

        btn_prev = Button(frame_buttons, text="Prev", command=self.clickButtonPrev)
        btn_prev.pack(side=RIGHT, padx=5, pady=5)

     
        
    def init_review_elements(self):
        frame_review_elements = Frame(self)
        frame_review_elements.pack(side=LEFT, fill=X)

        with open('config.json', 'r') as json_file:
            json_data = json.load(json_file)
            review_elements_from_json = json_data['keys']['review_elements_desc']

        grid_element =  0
        self.review_elements_list = []
        for item in review_elements_from_json:
            #print (str(item) +  " - " + str(review_elements_from_json[item]))
            tmp = IntVar()
            tmp_button = Checkbutton(frame_review_elements, text=str(review_elements_from_json[item]), variable=tmp)
            
            self.review_elements_list.append([str(item),tmp,tmp_button])
        
            tmp_button.grid(row=grid_element, sticky=W)
            grid_element +=1   
                    
    def init_global_keybinds(self, master):
        master.bind('<Escape>', self.exit_program)
        master.bind('<Control-Left>', self.left_key)
        master.bind('<Control-Right>', self.right_key)

        master.bind('<Control-o>', self.open_url)

        master.bind('<Control-plus>', self.increase_fontsize)
        master.bind('<Control-minus>', self.decrease_fontsize)

        master.bind('<F1>', self.tooglep)
        master.bind('<F2>', self.tooglep)
        master.bind('<F3>', self.tooglep)
        master.bind('<F4>', self.tooglep)
        master.bind('<F5>', self.tooglep)
        master.bind('<F6>', self.tooglep)
        master.bind('<F7>', self.tooglep)
        master.bind('<F8>', self.tooglep)
        master.bind('<F9>', self.tooglep)

    def init_exit_prompt(self, event=None):
        result = messagebox.askyesnocancel ('Save?','You want to save your work in the original file (a backup will be created)?',icon = 'question', default='yes')
        return self.do_exit(result)

    def init_url(self):

        # frame_doi = Frame(self)
        # frame_doi.pack(fill=X)

        # lbl_year = Label(frame_doi, text="DOI", width=6)
        # lbl_year.pack(side=LEFT, padx=5, pady=5)

        # self.entry_year = Entry(frame_doi)
        # self.entry_year.pack(fill=X, padx=5, expand=True)


        frame_url = Frame(self)
        frame_url.pack(fill=X, padx=5, pady=5)      

        btn_openurltop = Button(frame_url, text="Open URL", command=self.open_url)
        btn_openurltop.pack(side=RIGHT, padx=5, pady=5)


        self.lbl_url = Entry(frame_url, text="", width=30)
        self.lbl_url.pack(side=RIGHT)    


        return frame_url

    def init_count(self, _frame):
        res = self.my_controller.get_row_index_count_string()
        self.row_index_count_stringvar = StringVar()
        self.row_index_count_stringvar.set(res)
        self.lbl_row_index = Label(_frame, textvariable=self.row_index_count_stringvar)
        self.lbl_row_index.pack(side=LEFT)    

        Label(_frame, text = "|").pack(side=LEFT, padx=(5,5))    

        self.lbl_row_index = Label(_frame, text = "Go to: ")
        self.lbl_row_index.pack(side=LEFT, padx=(0,5))    

        vcmd = (_frame.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_target_row_index = Entry(_frame, width=5, validate='key', validatecommand=vcmd)
        self.entry_target_row_index.pack(side=LEFT, expand=False)
        self.entry_target_row_index.bind('<Return>', self.clickButtonGo)

        self.btn_go = Button(_frame, text="Go!", command=self.clickButtonGo)
        self.btn_go.pack(side=LEFT, padx=5, pady=5)

    ############################################
    ### Buttons, keys, shortcuts, and actions ##
    ############################################
    

    def tooglep(self, event = None):
        print (str(event) + " go button pressed")

        index = (int)(event.keycode)
        index = index -112 #112 is the keycode for f1
        if len(self.review_elements_list) >= index:
            checkbox = self.review_elements_list[index][2]
            checkbox.toggle()


    def clickButtonGo(self, event=None):
        print (str(event) + " go button pressed")
        self.do_go()

    def clickButtonPrev(self, event=None):
        print (str(event) + " prev button pressed")
        self.do_prev()

    def clickButtonNext(self, event=None):
        print (str(event) + " next button pressed")
        self.do_next()

    def open_url(self, event=None):
        print(str(event) + "mainwindow openurl 1")
        self.do_open_url()

    def exit_program(self, event=None):
        print (str(event))
        res = self.init_exit_prompt()
        if res:
            sys.exit(0)

    def left_key(self, event):
        print (str(event) + " key pressed")
        self.do_prev()

    def right_key(self, event):    
        print (str(event) + " key pressed")
        self.do_next()
    
    def increase_fontsize(self, event):
        print (str(event) + " increase font size")
        self.font_size  = self.font_size + 1
        self.set_font(self.font_size)

    def decrease_fontsize(self, event):
        print (str(event) + " decrease font size")
        self.font_size  = self.font_size - 1
        self.set_font(self.font_size)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

    def focus_prev_widget(self, event):
        event.widget.tk_focusPrev().focus()
        return("break")

    def not_implemented_yet(self, event=None):
        print(str(event) + " - not implemented yet")
    
    def open_stats(self):
        print("open stats")
        self.open_stats_window()

    def set_iterator_menu_status(self):
        print ("TODO: toggle disabled/normal state")
        # if self.get_iterator_options()[0].get():
        #     self.iteratorMenu.entryconfig(1,state="disabled")
        #     self.iteratorMenu.entryconfig(2,state="disabled")
        # else:
        #     self.iteratorMenu.entryconfig(2,state="normal")
        #     self.iteratorMenu.entryconfig(1,state="normal")

        # if self.get_iterator_options()[2].get():
        #     self.iteratorMenu.entryconfig(0,state="disabled")
        #     self.iteratorMenu.entryconfig(1,state="disabled")
        # else:
        #     self.iteratorMenu.entryconfig(0,state="normal")
        #     self.iteratorMenu.entryconfig(1,state="normal")

        # if self.get_iterator_options()[3].get():
        #     self.iteratorMenu.entryconfig(0,state="disabled")
        #     self.iteratorMenu.entryconfig(1,state="disabled")
        # else:
        #     self.iteratorMenu.entryconfig(0,state="normal")
        #     self.iteratorMenu.entryconfig(1,state="normal")

    def show_about(self):
        print("show about") 
        self.show_about_messagebox()

    def show_keyboard_shortcuts(self):
        print("show keyboard shortcuts")
        self.show_keyboard_shortcuts_messagebox()

    def export_items(self):
        self.my_controller.export_items_to_csv()

    def export_includes(self):
        self.my_controller.export_includes_to_csv()
####################
####################
####################

    def show_about_messagebox(self):
        messagetext = "ReviewToolkit created @ TU Ilmenau 2021. Enjoy :)"
        messagebox.showinfo(title="About", message=messagetext)

    def show_keyboard_shortcuts_messagebox(self):

        messagetext = "Shortcuts:\n\n"
        messagetext += "STRG + ->: next\n"
        messagetext += "STRG + <-: prev\n"
        messagetext += "STRG + +: increase font size of abstract\n"
        messagetext += "STRG + -: decrease font size of abstract\n"
        messagetext += "STRG + o: open URL in browser (browser path in config.json\n"
        messagetext += "F keys for checkboxes\n"
        

        messagetext += "\n Enjoy :)"

        messagebox.showinfo(title="About", message=messagetext)

    def open_stats_window(self):
        # Toplevel object which will be treated as a new window
        newWindow = Toplevel(self.master)
        newWindow.title("Stats")
        newWindow.geometry("400x200")
    
        self.my_controller.get_stats(newWindow)
        
    def update_current(self):
        self.my_controller.update_current_item_in_file(self.text_abstract, self.entry_title, self.review_elements_list, 
            self.entry_year, self.lbl_url)

    def update_row_index_count_string(self):
        self.my_controller.set_row_index_count_string(self.row_index_count_stringvar)

    def do_next(self):
        #set next item
        self.cleanAbstract()
        self.update_current()# updates current elements to file to retain changes!
        self.my_controller.set_next_item(self.text_abstract, self.entry_title, self.lbl_url, self.review_elements_list, 
            self.entry_year, self.get_iterator_options())    
        self.update_row_index_count_string()
        self.do_save()

    def do_prev(self):
        self.update_current()
        self.my_controller.set_prev_item(self.text_abstract, self.entry_title, self.lbl_url, self.review_elements_list, 
            self.entry_year, self.get_iterator_options()) 
        self.update_row_index_count_string()
        self.do_save()

    def do_save(self):
        self.my_controller.save()

    def do_swap_save(self):
        self.my_controller.do_swap_save()

    def do_exit(self, _result):
        return (self.my_controller.do_exit(_result, self.text_abstract, self.entry_title, self.lbl_url, self.review_elements_list, 
            self.entry_year))

    def do_open_url(self):
        print("mainwindow openurl 2")
        self.my_controller.open_url(self.lbl_url)

    def do_go(self):      
        print ("go")

        self.update_current()# updates current elements to file to retain changes!

        new_row_index  = int(self.entry_target_row_index.get())-1
        print (str(new_row_index))
        self.my_controller.set_specific_item(self.text_abstract, self.entry_title, self.lbl_url, self.review_elements_list, 
            new_row_index, self.entry_year)

        self.update_row_index_count_string()

        self.entry_target_row_index.delete(0, 'end')        

    ###########
    # Helpers
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        #print("tr_input: d='%s' P='%s' s='%s'" % (action, value_if_allowed, prior_value))
        if value_if_allowed == "":
            return True

        if value_if_allowed:
            try:
                tmp = int(value_if_allowed)
                #print (tmp)
                if tmp > self.my_controller.get_count():
                    return False
                if tmp < 1:
                    return False
                return True
            except ValueError:
                return False
        else:
            return False
    
    def onModification(self, event):
        #chars = len(event.widget.get("1.0", "end-1c"))

        #tmptext = event.widget.get("1.0", "end-1c")
        #tmptext = self.my_controller.clean_abstract(tmptext)

        #print ("tmptext: " + str(tmptext))

        #event.widget.delete("1.0", "end-1c")
        #event.widget.insert(tk.INSERT, self.my_controller.clean_abstract())

        #TODO this method fixed copy/paste. filter by event so that it doesn't get called all the time.

        #print ("chars: " + str(chars))

        print ("DEPRECATED")

    def cleanAbstract(self):
        tmptext = self.text_abstract.get("1.0", "end-1c")
        tmptext = self.my_controller.clean_abstract(tmptext)

        #print ("tmptext: " + str(tmptext))

        self.text_abstract.delete("1.0", "end-1c")
        self.text_abstract.insert("1.0", tmptext)


    def get_iterator_options(self):
        return [self.show_only_maybe, self.show_only_include, self.show_only_filtered, self.show_only_not_include, self.show_only_not_mobile_ar, self.show_only_empty]
