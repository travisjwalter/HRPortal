from __future__ import print_function
import pickle
import os.path
import uuid
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import googleapiclient.discovery

from script import createUser, assign_user_group, assign_user_attribute, deactivate_user, reactivate_user, getUserAttribute

# This script was created by Travis Walter on October 10th, 2020
# This script interfaces with Google Drive API with accreditation via a service account file (which has been redacted)

SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = ''
creds = service_account.Credentials.from_service_account_file( SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Function that creates a team drive
def create_td(td_name):
    request_id = str(uuid.uuid4())
    body = {'name': td_name}
    return service.drives().create(body=body, requestId=request_id, fields='id').execute().get('id')

# Function that adds a user to a team drive
def add_user(td_id, user, role='fileOrganizer'):
    body = {'type': 'user', 'role': role, 'emailAddress': user}
    return service.permissions().create(body=body, fileId=td_id,
            supportsAllDrives=True, fields='id').execute().get('id')

# Function that updates the permissions for the user in the team drive
def update_permissions(td_id, perm_id, new_role):
    #First retrieve the permission from the API
    body = {'role': new_role}
    return service.permissions().update(body=body, fileId=td_id, permissionId=perm_id, supportsAllDrives=True, fields='id').execute().get('id')

# Function that removes a user from the team drive
def remove_user(td_id, perm_id):
    service.permissions().delete(fileId=td_id, permissionId=perm_id, supportsAllDrives=True, fields='id').execute()

# Function that gets the user permission id from the team drive
def get_user_permissions(td_id, perm_id):
    return service.permissions().get(fileId=td_id, permissionId=perm_id, supportsAllDrives=True, fields='id').execute().get('id')
