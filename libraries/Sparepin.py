from datetime import datetime
import traceback
from RPA.Browser.Selenium import Selenium
Selenium.auto_close=False
import time
from configs import OUTPUT_PATH,WORKITEMS

from pprint import pprint
import os
from selenium.webdriver.common.keys import Keys
from RPA.PDF import PDF
pdf=PDF()

from RPA.Robocorp.WorkItems import WorkItems 

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





class Sparepin:
    def orderPartsFromDict(self,workerDict):
        
            print(workerDict)
            print("")
            self.orderParts(
                workerDict["Order number"],
                workerDict["Head"],
                workerDict["Body"],
                workerDict["Legs"],
                workerDict["Address"],
                )
    def init_browser(self):
        global browser_lib
        if(not browser_lib):
            browser_lib = Selenium(auto_close=False)
            browser_lib.set_download_directory(OUTPUT_PATH,True)
            browser_lib.auto_close=False
            browser_lib.open_available_browser("https://robotsparebinindustries.com/#/robot-order",headless=False)

    def orderParts(self,orderId,head,body,legs,address):
        self.init_browser()
        try:
            browser_lib.go_to("https://robotsparebinindustries.com/#/robot-order")
            try:
                alerts=browser_lib.wait_until_page_contains_element("xpath://div[@class='alert-buttons']",timeout=1)
                alerts=browser_lib.find_element("xpath://button[contains(.,'OK')]")
                #browser_lib.select_frame("//iframe[@title='SP Consent Message']")
                browser_lib.click_button(alerts.find_element_by_xpath("//button[contains(.,'OK')]"))#"//button[@title='Hyväksy kaikki evästeet']")
                #browser_lib.unselect_frame()
            except AssertionError as assE:
                print(assE)
                if("almacmp-modal-layer1" not in str(assE)):
                    raise
            print("popupclicked")
            print(f"starting to select:{head}")
            browser_lib.select_from_list_by_value("id:head",str(head))
            print("head")
            bodySelector=f"//*[@for='id-body-{body}']/input"
            print(bodySelector)

            print("body selected")
            legsSelector="//label[contains(.,'Legs:')]/following-sibling::input"
            browser_lib.input_text(legsSelector,str(legs))
            browser_lib.input_text("id:address",str(address))
            for i in range(3):
                browser_lib.find_element(bodySelector).click()
                time.sleep(0.2)
            print("")
            
            browser_lib.click_button("id:preview")
            browser_lib.wait_until_page_contains_element("id:robot-preview-image")
            print("preview clicked")
            print("")
            for i in range(10):
                browser_lib.click_button("id:order")
                try:
                    browser_lib.wait_until_page_contains_element("xpath://*[@id='order-completion']",timeout=0.8)
                    break
                except Exception as e:
                    print(e)
                    alerts=browser_lib.find_elements("//*[@role='alert']")
                    if(alerts):
                        print("Got alert, will try again")
                    else:
                        break
                    if(i==9):
                        raise
                
            html_content_as_string=browser_lib.get_element_attribute("id:order-completion","outerHTML")
            print("creating pdf from html:"+html_content_as_string)
            pdf_path=os.path.join(OUTPUT_PATH,f"{orderId}.pdf")
            pdf.html_to_pdf(html_content_as_string,pdf_path )
            savedScreenshot=browser_lib.capture_element_screenshot("id:robot-preview-image",f"orderScreenshot_{orderId}.png") 
            pdf.add_files_to_pdf([savedScreenshot],target_document=pdf_path,append=True)
            print("done")
        except Exception as e:
            print(str(e))
            raise
if __name__ == "__main__":
    
    sp=Sparepin()
    for i in range(10):
        sp.orderParts(f"idd{i}",1,2,3,"address")
