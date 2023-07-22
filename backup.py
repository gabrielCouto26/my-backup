import os
import shutil
from zipfile import ZipFile
from datetime import datetime

import upload


def main():
    try:
        print('Starting backup')
        start_time = datetime.now()

        FOLDER_ID = os.environ.get("GOOGLE_DRIVE_BACKUP_FOLDER_ID", '')
        if not FOLDER_ID:
            raise Exception('GOOGLE_DRIVE_BACKUP_FOLDER_ID environment variable is required')

        OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", '/home/gabriel/Backup')
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        file_name = f"Backup-{datetime.now()}.zip"

        # Create a new folder to copy the files
        temp_folder = os.path.join(OUTPUT_FOLDER, "temp")
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
            os.makedirs(temp_folder)

        file = open("backup_files.txt", "r")
        file_lines = file.read().splitlines()

        print('Copying files...')
        for file_path in file_lines:
            
            relative_path = os.path.relpath(file_path, start=os.path.dirname(file_path))
            target_path = os.path.join(temp_folder, relative_path)

            # Make sure the target directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # If it's a file, copy it to the temp folder
            if os.path.isfile(file_path):
                shutil.copy2(file_path, target_path)
            # If it's a directory, copy the entire directory recursively
            elif os.path.isdir(file_path):
                shutil.copytree(file_path, target_path)
            
        print('All files copied successfully to', temp_folder)

        # Generate the full path for the output zip file
        zip_path = os.path.join(OUTPUT_FOLDER, file_name)

        print('Zipping files...')
        # Create a zip file and write the files into it
        with ZipFile(zip_path, 'a') as zipf:
            for root, _, files in os.walk(temp_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, start=temp_folder)
                    zipf.write(file_path, arcname=relative_path)

        print('All files zipped successfully to', zip_path)

        # Remove the temporary folder after zipping
        shutil.rmtree(temp_folder)

        print('Proceding to upload...')

        # Upload the zip file to Google Drive
        upload.execute(zip_path, FOLDER_ID)

        print('Backup completed successfully.')
        end_time = datetime.now()
        print('Total time:', end_time - start_time)

    except Exception as e:
        print("Error: ", e)
        raise e

if __name__ == "__main__":
    main()