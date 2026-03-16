import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

def setup_logging():
    script_dir = Path(__file__).parent
    log_dir = script_dir / "Logs"
    log_dir.mkdir(exist_ok=True)

    # Create a unique filename based on the current time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"organizer_{timestamp}.log"

    # 1. Get the 'root' logger
    logger = logging.getLogger("organizer")
    logger.setLevel(logging.INFO)

    logger.propagate = False

    # 2. CLEAR existing handlers (this is the secret for workers!)
    # This prevents logs from being sent to old files or doubling up
    if logger.hasHandlers():
        logger.handlers.clear()

    # 3. Create your new Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # 4. Create and add the File Handler
    file_h = logging.FileHandler(log_file,encoding='utf-8')
    file_h.setFormatter(formatter)
    logger.addHandler(file_h)

    # 5. Create and add the Stream Handler (for your terminal/console)
    stream_h = logging.StreamHandler()
    stream_h.setFormatter(formatter)
    logger.addHandler(stream_h)

    logger.info(f"--- New Execution Started: {timestamp} ---")
    return logger

# STEP 0: Define file categories and their extensions
CATEGORIES = {
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg", "webp", "heic", "ico"],
    "Documents": ["pdf", "docx", "doc", "txt", "rtf", "odt", "pptx", "ppt", "xlsx", "xls", "csv", "epub"],
    "Videos": ["mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v", "3gp"],
    "Music": ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma", "mid", "midi"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "iso", "xz"],
    "Code": ["py", "js", "html", "css", "java", "cpp", "c", "sh", "rb", "php", "json", "xml", "sql", "ts"],
    "Executables": ["exe", "msi", "bin", "dmg", "pkg", "app", "deb", "rpm"],
    "Fonts": ["ttf", "otf", "woff", "woff2"],
    "System": ["sys", "dll", "ini", "log", "bak", "tmp", "cfg"]
}

def organize_Downloads(progress_callback=None):

    # Initializing the logging first
    logger = setup_logging()

    moved_files = 0
    skipped_files = 0

    downloads_path = Path.home() / "Downloads" # Getting Downloads Folder

    if not downloads_path.exists():
        return False # FIX

    # 1. PRE-SCAN: Get only files (ignore folders) to know the TOTAL
    all_items = list(downloads_path.iterdir()) # Getting all the Items of Downloads Folder including Folders
    files_to_process = [f for f in all_items if f.is_file()] # list of all the files only
    total_files = len(files_to_process) # total Number of files (Used for calculating the Progress)

    # If the folder is empty, report 100% immediately
    if total_files == 0: 
        logger.info("Download's Folder already organized")
        if progress_callback: progress_callback(100)
        return {"Files Moved": 0, "Files Skipped": 0}

    # 2. LOOP through the pre-scanned files
    for index, currentFile in enumerate(files_to_process, start=1):
        
        file_extension = currentFile.suffix.lower().lstrip(".")
        category_name = "Others"
        
        for category, extensions in CATEGORIES.items():
            if file_extension in extensions:
                category_name = category
                break

        category_folder = downloads_path / category_name
        category_folder.mkdir(exist_ok=True)
        
        dest_path = category_folder / currentFile.name # Full Path 
        counter = 1
        original_name = currentFile.name 
        while dest_path.exists():
            new_name = f"{currentFile.stem}_{counter}{currentFile.suffix}"
            dest_path = category_folder / new_name 
            counter += 1
        
        if counter > 1:
            logger.warning(f"Conflict: '{original_name}' already exists. Renaming to '{dest_path.name}'")
    
        try:
            currentFile.rename(dest_path)
            logger.info(f"Successfully moved: {original_name} -> {category_name}/{dest_path.name}")
            moved_files += 1
        except Exception as e:
            logger.exception(f"Failed to move {original_name}") # This logs the full error traceback
            skipped_files += 1

        # 3. REPORT PROGRESS: Calculate and "ping" the callback
        if progress_callback:
            # (Current Index / Total) * 100
            percent = int((index / total_files) * 100)
            progress_callback(percent) # This triggers the DB Write in worker.py

    logger.info(f"--- Summary: Moved {moved_files}, Skipped {skipped_files} ---")
    return {
        "Files Moved": moved_files,
        "Files Skipped": skipped_files
    }
		
        
	

