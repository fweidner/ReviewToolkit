
![image](https://github.com/fweidner/ReviewToolkit/assets/16336130/354731ce-2f87-4998-9257-395207ea4db1)


# ReviewToolkit

This repository contains a simple tool that eases the paper scanning process when doing a systematic literature review.

It contains two main projects:

* Scraping: scripts to scrape ACM and IEEE with scripts to prepare for the title and abstract scanner (this is more a helper project. 
* TitleAbstractScreener: python app to analyze the papers ==> This is really the main project. 

1. If you download a release, it shows you how the tool works (it loads data.csv with the options specified in config.json)
2. Check help when it is running for keyboard shortcuts.

If you start it via code:
1. Run start_gui-py of TitleAbstractScreener
1. Change the value of input_file in config.json to the file that has a similar structure to one of the demo.csv files (header is important)
1. Run. Be happy.
