import github
import os.path
import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from github import Auth
from github import Github
from github import GithubIntegration
from github import UnknownObjectException

# Read the PAT token from the credential.txt file
with open("credential.txt") as f: # Make sure to replace "credential.txt" with the correct filename if it's different
    token=f.readline().strip()

# Authenticate with GitHub using the token
auth = github.Auth.Token(token)
g=github.Github(auth=auth)

# Set up Google Sheets API credentials and access the google spreadsheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials =  ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials) # Make sure to replace "credentials.json" with the correct filename if it's different
sheet = client.open("Github_Acess_Form").sheet1 # Make sure to replace "Github_Acess_Form" with the correct spreadsheet name if it's different

# Check if the sheet is accessible and print the first row of data
first_row = sheet.row_values(1)
print(f"First row of data: {first_row}")

# create a dataframe from the csv file and filter the rows where flag is 0, then convert the required columns to lists
df = pd.read_csv("Request_form.csv")
new_df = df[df["Flag"]== 0]
print(new_df.head())
SrNo_list = new_df["SrNo"].tolist()
username_list = new_df["github_username"].tolist()
repo_list = new_df["repository"].tolist()
approval_list= new_df["approved"].tolist()
flag_list = new_df["Flag"].tolist()

# Function to check if the GitHub username exists
def check_username_exists(username):
    username_results = []
    for i in range (0,len(new_df)):
            try:
                g.get_user(username[i])
                print(f"Username '{username[i]}' exists.")
                username_results.append(True)
            except UnknownObjectException:
                print(f"Username '{username[i]}' does not exist.")
                username_results.append(False)
    return username_results    

a= (check_username_exists(username_list))

user= g.get_user()
# repos= user.get_repos()
# print(type(repos))
# repos_list = [repo.name for repo in repos]
# print(repos_list)

# Function to add a collaborator to the repository with push access if the username is correct and approval is yes, then update the flag to 1 in the google sheet
def add_collaborator(repo,collaborator_username):
    for i in range(0,len(new_df)):
        if a[i] == True and str(approval_list[i]).lower() == "yes":
            repo_name= user.login+"/"+f"{repo_list[i]}"
            repo=g.get_repo(repo_name)
            print(repo)
            collaborator_username = username_list[i]
            try:
                invitation = repo.add_to_collaborators(collaborator_username, permission="push")
                if invitation:
                    print(f"Invitation sent to {collaborator_username} with push permission for {repo.name}.")
                    sheet.update_acell(f"E{SrNo_list[i]+1}", 1)  # Update the "Flag" column to 1 in the Google Sheet
                else:
                    # This might happen if the user is already a collaborator
                    print(f"{collaborator_username} is already a collaborator or other issue occurred.")
            except Exception as e:
                print("_____EXCEPTION OCCURRED_____")
                print(f"An error occurred: {e}")
                print("_____EXCEPTION ENDED_____")

        else:
            print(f"Skipping {username_list[i]} for {repo_list[i]} due to incorrect username, or missing approval.")

b = add_collaborator(repo_list,username_list)



