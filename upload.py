import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']

TOKEN_PATH='/home/gabriel/env/dev/my-backup/token.json'
CREDENTIALS_PATH='/home/gabriel/env/dev/my-backup/credentials.json'

def upload_file(drive_service, file_path, folder_id):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id],
        'mimeType': 'application/zip'
    }

    media = MediaFileUpload(
        file_path, mimetype='application/zip', resumable=True)

    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id').execute()

    print("File uploaded successfully. File ID:", file.get("id"))

def execute(file_path, folder_id):
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            
            creds = flow.run_local_server(host='localhost', port=8080)
        
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        upload_file(service, file_path, folder_id)

    except HttpError as error:
        print(f'An error occurred: {error}')
