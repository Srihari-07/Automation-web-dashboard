from pathlib import Path 
import logging
from datetime import datetime

def setup_logging_System():
	# Getting the Parent Directory of the current Script and Creating a new Logs Folder
	main_dir = Path(__file__).parent
	log_dir = main_dir / "Logs"
	log_dir.mkdir(exist_ok = True)

	# Date time Format for Log fileName 
	timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

	log_file = log_dir / f"organizer_{timestamp}.log"

	# Creating a new Custom Child Logger object dedicated to handle one type of logs only
	logger = logging.getLogger("Downloads_organizer")
	logger.setLevel(logging.INFO)

	if logger.hasHandlers():
		logger.handlers.clear() # Fine for basic scripts but not for long running scripts

	# Formatter object specifying the Format of the Log entries
	formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

	# File handler to write the log messages to the given file
	file_handler = logging.FileHandler(log_file) 
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	logger.info("Demo Message of Info Log")

	

setup_logging_System()