import os
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


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

    logging.info(f"File uploaded successfully. File ID: {file.get('id')}")


def execute(file_path, folder_id):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)

            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        upload_file(service, file_path, folder_id)

    except HttpError as error:
        logging.error(f'An HTTP error occurred: {error}', exc_info=True)
    except Exception as error:
        logging.error(f'An unexpected error occurred: {error}', exc_info=True)
