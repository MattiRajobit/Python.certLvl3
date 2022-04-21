*** Settings ***
Library           Collections
Library           RPA.Robocorp.WorkItems
Library           RPA.Excel.Files
Library           RPA.Tables
Library           RPA.Dialogs
Library           RPA.Robocorp.Vault
Library           Httplevel3
Library           MyLibrary
*** Variables ***
${ORDER_FILE_NAME}=    orders.csv


*** Keywords ***


*** Tasks ***
Split orders file
    [Documentation]    Reads orders file from input item and creates workeritems
    ...    Asks user if they want to continue with orders.
    
    CreateWorkItems

