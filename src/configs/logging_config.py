import logging
import inspect
from pathlib import Path
from datetime import datetime

def setup_logging(loggerName):
    # Using inspect to find the caller's script location
    caller_frame = inspect.stack()[1]
    caller_script = Path(caller_frame.filename)

    # Getting the directory where the calling script is located
    script_dir = caller_script.parent
    log_dir = script_dir / "Logs"
    log_dir.mkdir(exist_ok=True)

    # Create a unique filename based on the current time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"organizer_{timestamp}.log"

    # 1. Get the 'root' logger
    logger = logging.getLogger(loggerName)
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