import glob
import os
import re
import extract_msg
from dateutil.parser import parse
from datetime import datetime as dt

# Default folder for PURGE files and step into the (must be network)
PURGE = 
os.chdir(PURGE)
# Dictionary of all DIV FOLDERS in PURGE (look into automating off existing list vr hard code)_
divDict = {
    ,
    
}


class Intro:
    
    def scene():
        print("Welcome to the filer system!")
        print("Are we Cleaning folders or Filing new messages?")
        req = input("Clean (1) or File (2)? ---> ")
        if req == '1':
            Clean()
        elif req == '2':
            File()
        else:
            print('not valid')
            
            
class Clean:
    
    def __init__(self):
        print("Cleaning, Okay what Division to start in?")
        req = input("Div (XXX) ---> ")
        div = Funcs.divCheck(req)
        print("Alright, {}".format(div))
        Funcs.cleanDiv(div)
        
        
class File:
    
    pass


class Funcs:
    
    def divCheck(Rdiv):
        if Rdiv in divDict:
            rdiv = divDict[Rdiv]
            return rdiv
        else:
            print("not valid")

    def cleanDiv(div):
        reqPath = '{purgePath}\{divNumber}'.format(purgePath=PURGE,divNumber=div)
        os.chdir(reqPath)
        name = div
        listOfFold = os.listdir(reqPath)
        numOfStores = len(listOfFold)
        i = 5
        fullPath = os.path.join(reqPath,listOfFold[i])
        os.chdir(fullPath)
        for item in glob.glob("*"):
            msg = extract_msg.Message(item)
            msgDate = msg.date
            msgName = msg.sender
            msgName = msgName.split('"')
            new = parse(msgDate)
            date = (new.strftime('%Y-%m-%d'))
            if '<noreply@.com>' in msgName:
                msgBody = msg.body
                msgBody = msgBody.split()
                bodylist = []
                for x in msgBody:
                    if '@' in x:
                        bodylist.append(x)
                msgName = bodylist[0]
                msgName = msgName.split('@')
                msgName = msgName[0]
                       
            else:
                msgName = msgName[1]
            
            newItem = r"{} - {} - {}{}.msg".format(msgName, date, name[:3], listOfFold[i])
            msg.close()
            os.rename(item, newItem)
        Clean()
            
        
            
   

   

Intro.scene()


