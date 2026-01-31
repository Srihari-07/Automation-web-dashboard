import os
import shutil
from pathlib import Path

# STEP 0: Define file categories and their extensions
CATEGORIES = {
    "Images": ["jpg", "jpeg", "png", "gif"],
    "Documents": ["pdf", "docx", "txt", "pptx"],
    "Videos": ["mp4", "mkv", "avi"],
    "Music": ["mp3", "wav"],
    "Archives": ["zip", "rar", "7z"]
}

def organize_Downloads():
	# Counters to skip the track of files organized
	moved_files = 0
	skipped_files = 0

	downloads_path = Path.home() / "Downloads" # Download's Path

	if not downloads_path.exists():  # Checking if Download's Folder exists
		print("Downloads folder not found.")
		return

	for item in downloads_path.iterdir():
		if item.is_dir():
			continue

		file_extension = item.suffix.lower().lstrip(".")

		category_name = "others"
		for category, extensions in CATEGORIES.items():
			if file_extension in extensions:
				category_name = category
				break

		category_folder = downloads_path / category_name
		category_folder.mkdir(exist_ok=True)
		
		try:
			shutil.move(str(item), str(category_folder))
			moved_files += 1
		except Exception as e:
			print(f"Could not move {item.name}: {e}")
			skipped_files += 1

	print("\nDownloads folder organized!")
	print(f"Files moved: {moved_files}")
	print(f"Files skipped: {skipped_files}")

if __name__ == "__main__":
	organize_Downloads()