# ReviewToolkit

This repository contains a simple tool that eases the process of paper scanning when doing a literature review

Contains two main projects:

* a scripts to scrape acm and ieee with scripts to prepare for the titleandabstract scanner
* python app to analyze the papers

(three day project, don't come at me pls)

0. create a folder called Results in subdir "Scraping"
1. update search terms
2. ScrapeACM (just run) => provides a file in Results/IEEE (abstract not scraped - I was lazy)
3. ScrapeIEEE (just run) => provides a file in Results/ACM (needs an IEEE api key)
4. ConcatAllArticles (update acm_file and ieee_file before running) => provides a file in Results wiht postfix _All
5. CleanUpDatabase (update input_file first) => provides a file in Results with postfix _All-Clean => input file for TitleAbstractScreener
6. run start_gui-py of TitleAbstractScreener
7. change value of input_file in config.json to the file wiht postfix _All-Clean
8. run. be happy.
