import os
import shutil
from zipfile import ZipFile
from datetime import datetime


def main():
    try:
        file_name = f"Backup-{datetime.now()}.zip"
        output_folder = os.getcwd()

        # Create a new folder to copy the files
        temp_folder = os.path.join(output_folder, "temp")
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        file = open("backup_files.txt", "r")
        file_lines = file.read().splitlines()
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

            # Generate the full path for the output zip file
            zip_path = os.path.join(output_folder, file_name)

            # Create a zip file and write the files into it
            with ZipFile(zip_path, 'a') as zipf:
                for root, _, files in os.walk(temp_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, start=temp_folder)
                        zipf.write(file_path, arcname=relative_path)

            # Remove the temporary folder after zipping
            shutil.rmtree(temp_folder)

        print('Backup completed successfully.')

    except Exception as e:
        print("Error: ", e)

if __name__ == "__main__":
    main()