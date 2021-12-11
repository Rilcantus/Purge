#IMPORT NEEDED MODULES
import glob
import time
import sys
import os
import re
import extract_msg
import shutil
import tkinter as tk
from dateutil.parser import parse
from datetime import datetime as dt
from tkinter.filedialog import asksaveasfilename

#MAIN CODE STARTS BELOW

#MAIN DICT AND LIST
PURGE = r'C:'
divDict = {}
numOfEmails = 0
outies = {}

#CLASS FOR SHARED FUNCTIONS BETWEEN FILE AND CLEAN

class Funcs:
   
    def startUp():
        os.chdir(PURGE)
        listFold = os.listdir(PURGE)
        direct = {}
        for item in listFold:
            item = item.split('-')
            i = len(item)
            if i == 1:
                item.append('placeholder')
            direct.update({(item[0]):(item[1])})
        global divDict
        divDict = direct.copy()
   
    
    def foldCheck(ans):
        a = ans
        if a in divDict:
            b = divDict[a]
            c = r'{}-{}'.format(a,b)
            return c
        else:
            print('Folder not valid')
            

    def pullEmail(email):
        msg = extract_msg.Message(email)
        msgDate = msg.date
        msgBody = msg.body
        msgName = msg.name
        msgSub = msg.subject
        msg.close()
        return msgDate, msgBody, msgName, msgSub
    
    def noReplyCheck(body):
        body = body.split()
        bodyList = []
        for x in body:
            if '@' in x:
                bodylist.append(x)
        msgName = bodyList[0]
        return msgName
    
    def emailSplitter(email):
        email = email.split('@')
        email = email[0]
        email = email.replace('.', ' ')
        email = email.capitalize()
        return email
    
    def nameHandler(name, body):
        if name in outies:
            name = name.split(' ')
            name = name[1]
        else:
            name = name.split('"')
            if '<noreply@company.com>' in name:
                name = Funcs.noReplyCheck(body)
                name = Funcs.emailSplitter(name)
            else:
                try:
                    name = name[1]
                except:
                    name = name[0]
        return name
    
    def dater(date):
        date = parse(date)
        date = date.strftime('%Y-%m-%d')
        return date
    
    def subFormater(name, date, ans, fold):
        sub = r'{} - {} - {}{}.msg'.format(name, date, ans, fold)
        return sub
    
    def strFinder(sub):
        x = re.search(r'\d\d\d\d\d\d, sub)
        x = x.group()
        div = x[0:3]
        store = x[3:6]
        return div, store
    
    def redirector(inputStr):
        viewTxt.insert("1.0", inputStr)
        windows.update()
        time.sleep(1)
    
    def saveReport():
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", ".txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        with open(filepath,"w") as output_files:
            text = viewTxt.get(1.0, tk.END)
            output_file.write(text)
        window.title(f"REPORT - {filepath}")
        
            

class Clean():
    
    def __init__(self):
        i = 0
        ans = cleanEnt.get()
        folder = Funcs.foldCheck(ans)
        reqPath = r'{}\{}'.format(PURGE,Folder)
        os.chdir(reqPath)
        listOfFolds = os.listdir(reqPath)
        numOfFolds = len(listOfFolds)
        perFolder = 0
        while i < numOfFolds:
            x = 0
            n = 1
            eachFold = os.path.join(reqPath,listOfFolds[i])
            os.chdir(eachFold)
            allEmails = len(os.listdir(eachFold))
            for item in glob.glob('*'):
                try:
                   date, body, name, sub = Funcs.pullEmail(item)
                except PermissionError:
                    continue
                name = Funcs.nameHandler(name, body)
                date = Funcs.dater(date)
                newItem = Funcs.subFormater(name, date, ans, listOfFolds[i])
                try:
                    os.rename(item, newItem)
                except FileExistsError:
                    try:
                        newItem = r'{} - {} - {}{}({}).msg'.format(name, date, ans, listOfFolds[i], n)
                        os.rename(item, newItem)
                        n += 1
                    except FileExistsError:
                        continue
                x += 1 
                print('{} emails have been completed.\nLast email was -> {}\n\n'.format(x, newItem))
            perFolder += x
            global numOfEmails
            numOfEmails += x
            print('{} folder contained {} items'.format(listOfFolds[i], perFolder)

class File():

    def __init__(self):
        file = Funcs.foldCheck('000')
        filePath = r'{}\{}'.format(PURGE, file)
        os.chdir(filePath)
        n = 1
        for item in glob.glob('*.msg'):
            date, body, name, sub = Funcs.pullEmail(item)
            date = Funcs.dater(date)
            name = Funcs.nameHandler(name, body)
            div, store = Funcs.strFinder(sub)
            newItem = Funcs.subFormater(name, date, div, store)
            try:
                os.rename(item,newItem)
            except:
                newItem = r'{} - {} - {}{} ({}).msg'.format(name, date, div, store, n)
                os.rename(item, newItem)
                n += 1
            newpath = Funcs.foldCheck(div)
            storePath = r'\00{}'.format(store)
            sendPath = r'{}\{}{}'.format(PURGE,newPath, storePath)
            print(sendPath)
            print(newItem)
            try:
                shutil.move(newItem, sendPath)
            except:
                newItem = r'{} - {} - {}{} ({}).msg'.format(name, date, div, store, n)
                os.rename(item, newItem)
                n += 1
                shutil.move(newItem, sendPath)


#TKINTER WINDOW BELOW HERE
window = tk.Tk()
window.title("Filer 5000")

window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight =1)

viewTxt = tk.Text(window)
frameBtn = tk.Frame(window)

fileBtn = tk.Button(frameBtn, text="File", command=File)
cleanLbl = tk.Label(frameBtn, text="What Division?")
cleanEnt = tk.Entry(frameBtn, width=10)
cleanBtn = tk.Button(frameBtn, text ="Clean", command=Clean)
totalLbl = tk.Label(frameBtn, text="Filer")
saveBtn = tk.Button(frameBtn, text="Save Report", command=Funcs.saveReport)

cleanLbl.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
cleanEnt.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
cleanBtn.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
totalLbl.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
fileBtn.grid(row=4, column=0, sticky="ew", padx=5,pady=5)
saveBtn.grid(row=5, column=0, sticky="ew", padx=5)

frameBtn.grid(row=0, column=0, sticky="ns")
viewTxt.grid(row=0, column=1, sticky="nsew")

sys.stdout.write = Funcs.redirector

window.mainloop()

#TKINTER WINDOW ABOVE HERE
