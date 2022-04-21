from audioop import reverse
from datetime import datetime
from importlib.resources import path
import traceback
from RPA.Browser.Selenium import Selenium
Selenium.auto_close=False
import time
from configs import OUTPUT_PATH,WORKITEMS
import json
from pprint import pprint
import os
from selenium.webdriver.common.keys import Keys
from RPA.PDF import PDF
pdf=PDF()
from RPA.HTTP import HTTP
http=HTTP()
import pandas as pd
from RPA.Robocorp.WorkItems import WorkItems 

from operator import itemgetter
from itertools import groupby
import requests

def printToOutput(toWRite:str):
    print(toWRite)
    with open(os.path.join(OUTPUT_PATH,"omaLog.txt"), "a+",encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%H:%M:%S %d.%m')}    {toWRite}\n")

    

def getAttributes(element):
    attrs = browser_lib.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    pprint(attrs)



def clickWithScript(xpath):
    for i in range(10):
        try:
            ele=browser_lib.find_element(xpath)
            browser_lib.driver.execute_script("arguments[0].click();",ele)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            if(i==9):
                raise

def checkboxAndVerify(selector,tryTimes=10):
    """
    Helper function to get checkbox selected.
    Clicks checkbox with script and checks that it got selected.
    """
    for i in range(tryTimes):
        try:
            
            clickWithScript(selector)
            #browser_lib.find_element(selector).click()#select_checkbox(selector)
            browser_lib.checkbox_should_be_selected(selector)
            #print(selector)
            getAttributes(browser_lib.find_element(selector))
            break
        except Exception as e:
            time.sleep(0.1*tryTimes)
            #browser_lib.scroll_element_into_view()
            if(i==tryTimes-1):
                raise
        

browser_lib=""





class Httplevel3:

    def createWorkItems(self):
        finalVals=self.sortDataToWanted()
        for item in finalVals:
            WORKITEMS.create_output_work_item(variables=item,save=True)

    def sortDataToWanted(self):
        http=HTTP()
        downloadDir=os.path.join(OUTPUT_PATH,f"traffic.json")
        returnv=http.download("https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",downloadDir,overwrite=True)
        print("downloaded")
        with open(downloadDir, "r",encoding="UTF-8") as file:                  
            everything=file.read()
            dictV=json.loads(everything)
        #with open("tiedosto.json", "w+",encoding="utf-8") as file:
        #    json.dump(dictV,file, sort_keys=True, indent=4, separators=(",", ": "))
        fullData=dictV["value"]
        #df = pd.DataFrame.from_records(fullData)
        #df.to_excel("traffic.xlsx")
        approvedValues=[]
        notApproved=[]

        
        for v in fullData:
            if(v["Dim1"]=="BTSX"):
                numValueF=float(v[numericKey])
                if(numValueF<5):
                    approvedValues.append(v)
                    continue
            notApproved.append(v)
        approvedValues.sort(key=lambda x:x[countryKey])
        groups = []
        uniquekeys = []
        for k, g in groupby(approvedValues, lambda x:x[countryKey]):
            vallist=list(g)
            groups.append(vallist)    # Store group iterator as a list
            uniquekeys.append(k)
            #print(vallist)
            #print(k)
            if(k=="ATG"):
                print("ATG")
            print("")
        print(groups[0][0])
        finalVals=[]
        for g in groups:
            g.sort(key=lambda x:x[timeKey],reverse=True)
            newest=g[0]
            finalVals.append(
                {
                "country":newest[countryKey],
                "year":newest[timeKey],
                "rate":newest[numericKey]
                }
            )
        print(groups[0][0])
        
        print("")
        df = pd.DataFrame.from_records(finalVals)
        df.to_excel("finalvals.xlsx")          
        return finalVals
    
    def postValuesOriginalKeys(self,v):
        if(len(v[countryKey])==3):
            for i in range(10):
                ret=requests.post(url=URL,data=v)
                print(ret)
                print("")
                if(ret.status_code==200):
                    print("success")
                    return ret
                else:
                    print("not succesfull")
                    print(ret.reason)
                    print("")
                    if(ret.reason=="Internal Server Error"):
                        print("internal error trying again")
                    else:
                        raise Exception(ret.reason)
            raise Exception("Internal Server Error")
        else:
            raise Exception(f"BUSINESS ,inconrrect value for country {v[countryKey]} should be 3-letters long")
    def postValues(self,v):
        if(len(v['country'])==3):
            for i in range(10):
                ret=requests.post(url=URL,data=v)
                print(ret)
                print("")
                if(ret.status_code==200):
                    print("success")
                    return ret
                else:
                    print("not succesfull")
                    print(ret.reason)
                    print("")
                    if(ret.reason=="Internal Server Error"):
                        print("internal error trying again")
                    else:
                        raise Exception(ret.reason)
            raise Exception("Internal Server Error")
        else:
            raise Exception(f"BUSINESS, inconrrect value for country {v['country']} should be 3-letters long")
countryKey="SpatialDim"
numericKey="NumericValue"
timeKey="TimeDim"
URL="https://robocorp.com/inhuman-insurance-inc/sales-system-api"
if __name__ == "__main__":
    
    http=HTTP()

    downloadDir=os.path.join(OUTPUT_PATH,f"traffic.json")
    returnv=http.download("https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",downloadDir,overwrite=True)
    print("downloaded")
    with open(downloadDir, "r",encoding="UTF-8") as file:                  
        everything=file.read()
        dictV=json.loads(everything)
    #with open("tiedosto.json", "w+",encoding="utf-8") as file:
    #    json.dump(dictV,file, sort_keys=True, indent=4, separators=(",", ": "))
    fullData=dictV["value"]
    #df = pd.DataFrame.from_records(fullData)
    #df.to_excel("traffic.xlsx")
    approvedValues=[]
    notApproved=[]

    for v in fullData:
        if(v["Dim1"]=="BTSX"):
            numValueF=float(v[numericKey])
            if(numValueF<5):
                approvedValues.append(v)
                continue
        notApproved.append(v)
    approvedValues.sort(key=lambda x:x[countryKey])
    groups = []
    uniquekeys = []
    for k, g in groupby(approvedValues, lambda x:x[countryKey]):
        vallist=list(g)
        groups.append(vallist)    # Store group iterator as a list
        uniquekeys.append(k)
        #print(vallist)
        #print(k)
        if(k=="ATG"):
            print("ATG")
        print("")
    print(groups[0][0])
    finalVals=[]
    for g in groups:
        g.sort(key=lambda x:x[timeKey],reverse=True)
        newest=g[0]
        finalVals.append(
            {
            "country":newest[countryKey],
            "year":newest[timeKey],
            "rate":newest[numericKey]
            }
        )
    print(groups[0][0])
    
    print("")
    df = pd.DataFrame.from_records(finalVals)
    df.to_excel("finalvals.xlsx")
    http3=Httplevel3()
    for v in finalVals:  
        http3.postValues(v)
    #df.sort_values("SpatialDim")
    #gf=df.groupby("SpatialDim")
    #gf.to_excel("traffic_ap.xlsx")  