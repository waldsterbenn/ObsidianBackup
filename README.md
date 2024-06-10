# Obsidian Folder Backup

This project is designed to automatically backup the `Obsidian` folder every time windows starts, using a Python script and Windows Task Scheduler.

## Prerequisites

1. Python 3.11 installed on your machine.

## Setup

### 1. Python Script

Make sure the Python script `main.py` is located in the `C:\src\ObsidianBackup\` directory.

### 2. Create a Batch File

1. Create a new text file using Notepad.
2. In the text file, add the following line:

```
"C:\path_to_python\python.exe" "C:\src\ObsidianBackup\main.py"
```

Replace `path_to_python` with the path to your Python 3.11 installation, typically something like `c:\python39\python.exe`.

3. Save the file with a `.bat` extension, for example, `run_backup.bat`, in the same directory as `main.py`.

### 3. Schedule the Task

1. Press `Win + R`, type `taskschd.msc`, and press Enter to open the Task Scheduler.
2. In the Actions Pane, click "Create Basic Task".
3. Name the task (e.g., "ObsidianBackup") and provide a description if desired. Click "Next".
4. Choose the "Weekly" trigger and click "Next".
5. Set it to recur every 1 week and choose the day and time you want the backup to happen. Click "Next".
6. In the Action step, choose "Start a program" and click "Next".
7. Browse and select the `run_backup.bat` file you created in step 2.
8. Click "Next", review your settings, and click "Finish".

### 4. Additional Configuration in Task Scheduler

If the computer isn't on at the scheduled time, ensure the task runs as soon as possible after the scheduled start is missed. To do this:

1. In Task Scheduler, locate your task.
2. Right-click on it and select "Properties".
3. Go to the "Settings" tab.
4. Check the option "Run task as soon as possible after a scheduled start is missed".

## Usage

Once set up, the Python script will automatically zip the `Obsidian` folder every week at the scheduled time and save it to the `C:\users\ls\Documents\ObsidianBackup\` directory.

Preferably you should point to a folder that is cloud backed by Google Drive or OneDrive, so shit don't disappear.
