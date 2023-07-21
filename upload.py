import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from apiclient.http import MediaFileUpload

FILE_PATH = os.environ.get("FILE_PATH")
FOLDER_ID = os.environ.get("FOLDER_ID")

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_file(drive_service, file_path, folder_id):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id],
        'mimeType': '*/*'
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id').execute()

    print("File uploaded successfully. File ID:", file.get("id"))

def execute():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            creds = flow.run_local_server(host='localhost', port=8080)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        upload_file(service, FILE_PATH, FOLDER_ID)

    except HttpError as error:
        print(f'An error occurred: {error}')

