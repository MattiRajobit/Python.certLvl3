*** Settings ***
Library           Screenshot
Library           RPA.Robocorp.WorkItems
Library           RPA.Tables
Library           Collections
Library           Sparepin
Library            RPA.Archive
Library    OperatingSystem
Library    Httplevel3
Library           String

*** Keywords ***
Load and Process Order
    [Documentation]    Handles one item and also does error handling for the item
    
    ${payload}=    Get Work Item Payload
    ${Item Handled}    ${output}=    Run Keyword And Ignore Error
    ...    Post Values    ${payload}
  
    IF    "${Item Handled}" == "PASS"
        Log    ${payload} item handled succesfully!
        #Setting robotCompleted variable, to know that this item was really finished by robot.
        Set Work Item Variable    robotCompleted    True
        Save Work Item
        Release Input Work Item    DONE
    ELSE
        # Giving a good error message here means that data related errors can
        # be fixed faster in Control Room.
        Exception Handling      ${output}    ${payload}
    END

Exception Handling
    [Documentation]    sets item failed, also does logging and restarting browser
    ...    Tags: OwnException
    [Arguments]    ${output}    ${payload} 
    @{words}=    Split String    ${output}       ,

    ${error_message}=    Set Variable
    ...    Failed to handle item for: ${payload}.
    
    IF    """${words}[0]""" == "BUSINESS"
        ${et}    Set Variable    BUSINESS
        ${error_message}=    Set Variable
        ...    FAILed with bussiness error: ${payload}. ${words}[1]
        Log    ${error_message}    level=WARN
        
    ELSE
        ${et}    Set Variable    APPLICATION
        Log    ${error_message}    level=ERROR
    END
    Release Input Work Item
    ...    state=FAILED
    ...    exception_type=${et}
    ...    message=${error_message}

   
 

*** Tasks ***
Load and Process All Orders
    [Documentation]    Orders all robots.
    ...    uses python library to order parts
    ...    After part order downloads pdf file
    ...    Also collects pdf files into zip package!
    For Each Input Work Item    Load and Process Order
   
    


