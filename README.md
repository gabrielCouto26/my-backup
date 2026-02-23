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
  - Python 3.11+

---

## Setup and Usage

### 1. Prepare Your Credentials

- Download your OAuth 2.0 Client ID JSON file from the Google Cloud Console and save it as `credentials.json` in the root directory of this project.

### 2. Set Environment Variables
  - Create a `.env` file in the project root with the following content. Make sure `GOOGLE_DRIVE_BACKUP_FOLDER_ID` is defined. `OUTPUT_FOLDER` is optional; if not defined, the local script will use `./local_backups`.
  ```bash
    GOOGLE_DRIVE_BACKUP_FOLDER_ID=your_google_drive_folder_id
    # OUTPUT_FOLDER=/path/to/your/local_backups
  ```

### 3. Define Files to Backup

- Create a file named `backup_files.txt` in the project’s root directory.
- List all the file paths or directories you wish to backup, one per line.

### 4. Execute Backups Locally (Without Docker)

This method is ideal for local development and for the first authentication. It uses the `run_local_backup.sh` script to manage the virtual environment and execute the backup.

1.  **Make the script executable:**
    ```bash
    chmod +x run_local_backup.sh
    ```

2.  **Execute the script:**
    ```bash
    ./run_local_backup.sh
    ```
    *   **First Execution:** If `token.json` does not exist, your browser will open for Google authentication. Follow the instructions. After granting access, `token.json` will be created and the first backup will run.
    *   **Subsequent Executions:** The script will use the existing `token.json` and execute the backup non-interactively.
    *   **Output Folder:** The `.zip` file will be saved to the folder defined by `OUTPUT_FOLDER` in your `.env`.

### 5. Execute Backups Using Docker (Optional)

After `token.json` has been created (preferably by local execution in step 4), you can run all future backups easily and non-interactively using Docker Compose.

```bash
docker-compose up --build
```
The `.zip` backup will be saved to the folder defined by `OUTPUT_FOLDER` in your `.env` and uploaded to Google Drive.
