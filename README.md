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
  - A `credentials.json` file obtained from the [Google Cloud Console](https://console.cloud.google.com/). The OAuth 2.0 Client ID must be of type **Desktop application**.
  
- **Environment Variables:**  
  - Set the `GOOGLE_DRIVE_BACKUP_FOLDER_ID` environment variable with the target folder's ID in Google Drive.
  - Optionally, set the `OUTPUT_FOLDER` to specify where the ZIP files will be stored locally.

- **Software Requirements:**  
  - Docker & Docker Compose
  - Python 3.11+

---

## Setup and Usage

### 1. Prepare Your Credentials

- Download your OAuth 2.0 Client ID JSON file from the Google Cloud Console and save it as `credentials.json` in the root directory of this project.

### 2. Set Environment Variables
  - Create a `.env` file in the project root with the following content:
  ```bash
    GOOGLE_DRIVE_BACKUP_FOLDER_ID=your_google_drive_folder_id
    OUTPUT_FOLDER=/home/user/backup
  ```

### 3. Define Files to Backup

- Create a file named `backup_files.txt` in the project’s root directory.
- List all the file paths or directories you wish to backup, one per line.

### 4. First-Time Authentication (Required)

To allow the application to access your Google Drive, you must perform a one-time authentication locally. This process will open a browser window and create a `token.json` file, which will be used for all future automated backups.

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script to authenticate:**
    ```bash
    python3 backup.py
    ```
    Follow the instructions in your browser. Once you grant access, the `token.json` file will be created in the project root, and the first backup will run.

### 5. Run Subsequent Backups with Docker

After `token.json` has been created, you can run all future backups easily and non-interactively using Docker Compose.

```bash
docker-compose up --build
```
The backup .zip will be saved to the folder specified in OUTPUT_FOLDER and uploaded to Google Drive.
