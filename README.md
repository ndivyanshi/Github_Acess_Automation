# Github_Acess_Automation

The obective of this code is to automate adding collaborators to Github repositories.

Following components were used to implement this code:
1. Python 'gspread' API for google sheets
2. PyGitHub - a Python library to access the GitHub REST API.

The workflow for this process :
1. User fills in the following details in a google spreadsheet:
  a. github username
  b. selects the repository they need access to
2. Download the google spreadsheet as a CSV and run the python script
3. Python script checks the validity of provided github username, checks for an approval prior to adding collaborator
4. Updates the flag field in the google spreadsheet after adding a collaborator
