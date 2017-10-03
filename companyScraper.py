# -*- coding: utf-8 -*-
import requests
from time import sleep
import sys
import pandas as pd

def printProgress(iteration, total, prefix='', suffix='', decimals=1, bar_length=50):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


class Form():
    """
    class representing a form of a company
    """
    def __init__(self, name, formType, cik, date, url):
        """
        name: name of company
        formType: kind of form represented ex 10-k or 8-k
        cik: central index key
        date: string representing date form was submitted
        url: taken from company.idk - takes url column and removes all -s from info
        right of last /
        """
        #must replace / in name or causes issues writing files
        self.name = name.replace("/", "")
        self.formType = formType
        self.cik = cik
        self.date = date
        self.url = url

    def generateURL(self):
        """
        generates and returns url to get csv of desired document
        """
        csvURL = "https://www.sec.gov/Archives/edgar/data/" + self.cik + "/" + self.url + "/Financial_Report.xlsx"
        return csvURL


    

def getForms(formType):
    """
    generates and returns array of forms of every listed company
    formType: kind of form represented ex 10-k or 8-k
    """
    #read in company.idx file
    file = open('company.idx', 'r')
    #split file by \n
    pastDelimiter = False
    forms = []
    for line in file:
        if not pastDelimiter:
            if line[0] == '-':
                pastDelimiter = True
        else:
            #splits up data into relevant parts and creates a company object
            #delimiter is used as 2 spaces between each element
            delimiter = line.find("  ")
            name = line[:delimiter]
            #reduce line to remove indexes containing name
            line = line[62:]
            delimiter = line.find("  ")
            formTypeLine = line[:delimiter]
            #at this point - check if the line read corresponds to the form type - if it doesnt go to next line
            if formTypeLine == formType:
                #reduce line to remove indexes containing form type
                line = line[12:]
                delimiter = line.find("  ")
                cik = line[:delimiter]
                #reduce line to remove indexes containing cik
                line = line[12:]
                delimiter = line.find("  ")
                date = line[:delimiter]
                #only url should remain
                line = line[12:]
                delimiter = line.find("  ")
                url = line[:delimiter]
                #format url - get rid of edgar/data
                url = url[11:]
                #get rid of cik
                delimiter = url.find("/")
                url = url[delimiter + 1:]
                #remove -s and .txt
                url = url.replace('-', "")
                url = url.replace('.txt', "")
                #create form object
                form = Form(name, formType, cik, date, url)
                forms.append(form)
    return forms

def downloadFiles(forms):
    """
    uses array of Form objects to download and organize files
    forms: array of forms to download
    """
    numForms = len(forms)
    for i, form in enumerate(forms):
        with requests.Session() as s:
            #setup to avoid connection errors
            downloadDone = False
             #counter to detect when network errors should stop the program - I have decided that after five attempts
            #to connect an error should stop the program
            connectionCounter = 0
            while not downloadDone:
                if connectionCounter <= 5:
                    try:
                        download = s.get(form.generateURL())
                        downloadDone = True
                    except requests.exceptions.ConnectTimeout:
                        print("\nConnection refused by the server")
                        print("The connection will be attempted again in 5 seconds")
                        sleep(5)
                        connectionCounter += 1
                        continue
                else:
                    download = s.get(url)
                    downloadDone =True
            #writes doc to directory
            fileName = form.name + "-" + form.formType + "-" + form.date + ".xlsx"
            f1 = open(fileName, "a+b")
            f1.write(download.content)
            f1.close()
        #update progress bar
        sleep(0.1)
        printProgress(i, numForms, prefix = "Progress:", suffix = "Complete")



forms = getForms("10-K")
downloadFiles(forms)
