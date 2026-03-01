import os
import shutil
from pathlib import Path

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
    moved_files = 0
    skipped_files = 0

    downloads_path = Path.home() / "Downloads" # Getting Downloads Folder

    if not downloads_path.exists():
        return False 

    # 1. PRE-SCAN: Get only files (ignore folders) to know the TOTAL
    all_items = list(downloads_path.iterdir()) # Getting all the Items of Downloads Folder including Folders
    files_to_process = [f for f in all_items if f.is_file()] # list of all the files only
    total_files = len(files_to_process) # total Number of files (Used for calculating the Progress)

    # If the folder is empty, report 100% immediately
    if total_files == 0: 
        if progress_callback: progress_callback(100)
        return {"Files Moved": 0, "Files Skipped": 0}

    # 2. LOOP through the pre-scanned files
    for index, currentFile in enumerate(files_to_process, start=1):
        
        file_extension = currentFile.suffix.lower().lstrip(".")
        category_name = "others"
        
        for category, extensions in CATEGORIES.items():
            if file_extension in extensions:
                category_name = category
                break

        category_folder = downloads_path / category_name
        category_folder.mkdir(exist_ok=True)
        
        try:
            shutil.move(str(currentFile), str(category_folder))
            moved_files += 1
        except Exception as e:
            skipped_files += 1

        # 3. REPORT PROGRESS: Calculate and "ping" the callback
        if progress_callback:
            # (Current Index / Total) * 100
            percent = int((index / total_files) * 100)
            progress_callback(percent) # This triggers the DB Write in worker.py

    return {
        "Files Moved": moved_files,
        "Files Skipped": skipped_files
    }
		
        
	

