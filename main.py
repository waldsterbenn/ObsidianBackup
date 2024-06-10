import os
import shutil
from datetime import datetime
import hashlib
import sys
from plyer import notification


def compute_file_hash(filename):
    """Compute SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(filename, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            h.update(byte_block)
    return h.hexdigest()


def perform_backup(source_folder, destination_folder):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    zip_filename = os.path.join(
        destination_folder, f'{timestamp}_Obsidian_backup.zip')
    shutil.make_archive(zip_filename[:-4], 'zip', source_folder)
    print(f"DEBUG: Backup completed. Zipped file: {zip_filename}")
    with open(os.path.join(destination_folder, 'backup_log.txt'), 'a') as logfile:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logfile.write(
            f"\n{timestamp}: Changes found: {not is_identical_to_latest_backup(zip_filename, destination_folder)}")
    return zip_filename


def display_notification(title, message, duration=10):
    """Display a Windows toast notification using plyer."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=duration
        )
    except Exception as e:
        print(f"Notification error: {str(e)}")


def is_identical_to_latest_backup(new_backup_filename, backup_destination):
    if not os.path.exists(backup_destination):
        print(
            f"DEBUG: Backup destination {backup_destination} does not exist.")
        return False

    backup_files = [f for f in os.listdir(
        backup_destination) if f.endswith('_Obsidian_backup.zip')]
    print(f"DEBUG: Found {len(backup_files)} backup files.")

   # Remove the new_backup_filename from the list
    backup_files = [f for f in backup_files if f !=
                    os.path.basename(new_backup_filename)]

    if not backup_files:
        print("DEBUG: No existing backup files found (excluding the new backup).")
        return False

    latest_backup = sorted(backup_files)[-1]
    print(f"DEBUG: Latest backup: {latest_backup}")
    hash_of_latest = compute_file_hash(
        os.path.join(backup_destination, latest_backup))
    hash_of_new = compute_file_hash(new_backup_filename)
    print(
        f"DEBUG: Hash of latest backup:\t {hash_of_latest} ({latest_backup})")
    print(
        f"DEBUG: Hash of new backup:\t {hash_of_new} ({new_backup_filename})")

    return hash_of_latest == hash_of_new


def main_function():
    source_folder = "C:\\Users\\ls\\Documents\\Obsidian"
    backup_destination = "S:\\ProtonDrive\\My files\\ObsidianBackup\\"

    try:
        zip_filename = perform_backup(source_folder, backup_destination)

        if is_identical_to_latest_backup(zip_filename, backup_destination):
            print(
                "DEBUG: The new backup is identical to the latest backup. Deleting redundant backup.")
            os.remove(zip_filename)  # Delete the new backup file
            display_notification(
                "No backup", "New backup == old backup.")
            sys.exit(1)
        else:
            print("DEBUG: The new backup is different from the latest backup.")
            display_notification("Obsidian Backup Successful",
                                 f"Backup completed. Zipped file: {zip_filename}")
            sys.exit(0)
    except Exception as e:
        print(f"DEBUG: Backup error: {str(e)}")
        display_notification("Backup Failed", f"Error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main_function()
