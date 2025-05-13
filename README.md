# AutoBackup Drive

This project automatically creates backups of specified local files and directories, compresses them into a single ZIP file, and uploads the archive to a designated folder in Google Drive. The entire process is containerized using Docker for easy deployment.

---

## Features

- **Selective Backup:** Reads a list of files and directories from `backup_files.txt` and processes them accordingly.
- **Compression:** Generates a timestamped ZIP file containing all backup files.
- **Automatic Upload:** Utilizes the Google Drive API to securely upload the ZIP file to a specified folder.
- **Containerized Execution:** Docker integration provides a portable and reproducible runtime environment.
- **OAuth 2.0 Authentication:** Handles authentication with Google Drive using OAuth 2.0.

---

## Prerequisites

- **Google API Credentials:**  
  - A Google account with access to Google Drive.
  - A `credentials.json` file obtained from the [Google Cloud Console](https://console.cloud.google.com/).
  
- **Environment Variables:**  
  - Set the `GOOGLE_DRIVE_BACKUP_FOLDER_ID` environment variable with the target folder's ID in Google Drive.
  - Optionally, set the `OUTPUT_FOLDER` to specify where the ZIP files will be stored locally.

- **Software Requirements:**  
  - Docker
  - Docker Compose

---

## Setup and Usage

### 1. Prepare Your Credentials

- Place your `credentials.json` in the root directory of the project.
- The first time you run the backup, the application will open a browser window for Google authentication and generate a `token.json` file for subsequent executions.

### 3. Set your environment variables
  - Create a .env file
  ```bash
    GOOGLE_DRIVE_BACKUP_FOLDER_ID=your_google_drive_folder_id
    OUTPUT_FOLDER=/home/user/backup
  ```

### 3. Define Files to Backup

- Create a file named `backup_files.txt` in the project’s root directory.
- List all the file paths or directories you wish to backup, one per line.

### 4. Build and Run the Container

Using Docker Compose, you can build and run the container with a single command:

```bash
docker-compose up --build
