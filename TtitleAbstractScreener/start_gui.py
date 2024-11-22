from tkinter import *
import json

import MainWindow

def process_config(_root):
   
    with open('config.json','r') as json_file:
        json_data = json.load(json_file)
        scaling = float(json_data['scaling'])
        width = int(json_data['windowsize']['width'])
        height = int(json_data['windowsize']['height'])
    
    _root.tk.call('tk', 'scaling', scaling)
    _root.geometry(str(width)+"x"+str(height))

def main():
    root = Tk()
    
    process_config(root)
        #dfeault scaling = 1.5
    
    app = MainWindow.MainWindow()

    root.protocol("WM_DELETE_WINDOW", app.exit_program)
    root.mainloop()

if __name__ == '__main__':
    main()


# TODO [x] crreate dialog to save over original file and create backup!
# TODO [x] create copy for autosave
# TODO [x] save annotations from review_elements in seperate columns
# TODO [x] package it to executable
# TODO [x] show url/link (clickable!)
# TODO [x] on next, read and set review element items!
# TODO [x] reset textboxes on next/prev
# TODO [x] add label curr/num
# TODO [x] go to item
# TODO [x] add year
# TODO [x] save items on go to specific
# TODO [x] shorten url text to 180 chars
# TODO [x] clean up abstract on copy!
# TODO [x] font size
# TODO [x] word break / alignment
# TODO [x] BUG: Can't dynamically update review_elements.
# TODO [x] change headings in review_elements
# TODO [x] fix in DataHandler.py: my_csv_data_list to my_csv_data_dict
# TODO [x] allow use of <- and -> in text fields
# TODO [x] lstrip items
# TODO [x] fix filter system
# TODO [x] change labels in filters
# TODO [x] add filter for check_later
# TODO [x] make doi editable
# TODO [x] make title larger (scales)
# TODO [x] add 1-5 keys to review-element checkboxes ==> F-Keys
# TODO [ ] Add context menu
# TODO [ ] clean up MainWindow.py - it started good but than it just got wild
# TODO [ ] make bullet points fully dynamic (also in controller and datahandler)
# TODO [ ] speed when searching; optimize while loop
# TODO [ ] Dynamic filters based on json
# TODO [ ] Auto open URL checkbox in settings. 
# TODO [ ] User ID management
# TODO [ ] Porper search field.
# TODO [ ] Customizable Keyboard shortcuts
# BUG [x] Somehow include is not properly excluded when first four are active
# BUG [ ] Details get only updated after next/prev - not a prob for all except doi!
# TODO [ ] IF 0000, then open duckduckgo search
