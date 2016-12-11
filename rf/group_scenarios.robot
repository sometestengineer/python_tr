*** Settings ***
Library  rf.Addressbook
Library  Collections
# fixture for all test suites
Suite Setup  Init Fixtures
Suite Teardown  Destroy Fixtures

*** Test Cases ***
Add new group
    ${old_list}=  Get Group List
    ${group}=  New Group  name1  header1  footer1
    Create Group  ${group}
    ${new_list}=  Get Group List
    Append To List  ${old_list}  ${group}
    Group Lists Should Be Equal  ${new_list}  ${old_list}

Delete group
    ${old_list}=  Get Group List
    ${len}=  BuiltIn.Get Length  ${old_list}  # calc list len
    ${index}=  Evaluate  random.randrange(${len})  random  # evaluate to use python code, random for import random
    ${group}=  Get From List  ${old_list}  ${index}  # get from list = robot method
    Delete Group  ${group}
    ${new_list}=  Get Group List
    Remove Values From List  ${old_list}  ${group}
    Group Lists Should Be Equal  ${new_list}  ${old_list}