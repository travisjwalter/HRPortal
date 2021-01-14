from __future__ import print_function
import pickle
import os.path
import re
import uuid
from google.auth import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import googleapiclient.discovery

from script import createUser, assign_user_group, assign_user_attribute, deactivate_user, reactivate_user, getUserAttribute

# This script was created by Travis Walter on October 10th, 2020
# This script interfaces with the Google Admin SDK, predominately the User and Group APIs with accreditation via a service account file (which has been redacted)

allHandsGroupID = ""

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group']

SERVICE_ACCOUNT_FILE = ''
creds = service_account.Credentials.from_service_account_file( SERVICE_ACCOUNT_FILE, scopes=SCOPES)
delegated_creds = creds.with_subject('')

service = build('admin', 'directory_v1', credentials=delegated_creds)

# Function that suspends a user within a google workspace
def suspendUser(email):
    print("Suspending " + str(email))
    try:
        user = service.users().get(userKey=str(email)).execute()
        user['suspended'] = True
        service.users().update(userKey=str(email), body=user).execute()
    except HttpError as err:
        print("User not found")

# Function that reactivates a user within a google workspace
def reactivateUser(email):
    print("Reactivating User " + str(email))
    try:
        user = service.users().get(userKey=str(email)).execute()
        user['suspended'] = False
        service.users().update(userKey=str(email), body=user).execute()
    except HttpError as err:
        print("User not found")

# Function that adds a user to a group within a google workspace
def addUserToGroup(group, member):
    print("Adding User " + str(member) + " to " + str(group))
    try:
        memberList = service.members().list(groupKey=allHandsGroupID, includeDerivedMembership="true").execute()
        for i in memberList['members']:
            try:
                if str(i['email']) == str(member):
                    service.members().insert(groupKey=str(group), body=i).execute()
                    print("User added sucessfully!")
                    break
                else:
                    continue
            except KeyError as keyerr:
                continue

    except HttpError as err:
        print("User not found")

# Function that removes a user from a group within a google workspace
def removeUserFromGroup(group, member):
    print("Removing User " + str(member) + " from " + str(group))
    try:
        service.members().delete(groupKey=str(group), memberKey=str(member)).execute()
        print("User removed successfully!")
    except HttpError as err:
        print("User not found")

# Function that creates a group within a google workspace
def createGroup(groupName, groupEmail):
    print("Creating group " + groupName + " at " + groupEmail)
    requestBodyDict = {
        "email":str(groupEmail),
        "name":str(groupName)
    }
    try:
        service.groups().insert(body=requestBodyDict).execute()
    except HttpError as err:
        print(err)

# Function that deletes a group within a google workspace
def deleteGroup(group):
    print("Deleting group " + group)
    try:
        service.groups().delete(groupKey=str(group)).execute()
    except HttpError as err:
        print(err)

# Function that removes a user from a google workspace
def removeUser(user):
    try:
        service.users().delete(userKey=str(user)).execute()
    except HttpError as err:
        print(err)