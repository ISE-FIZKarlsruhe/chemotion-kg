import os
import logging
import multiprocessing
from datetime import datetime, timedelta
import subprocess

# Configure logging
def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), "Documents", "logs")
    os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists
    log_file = os.path.join(log_dir, "download_log.txt")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging initialized.")

# Function to run a Python subprocess for each date chunk
def run_downloader(start_date, end_date):
    command = [
        "python", "worker_downloader.py",
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    ]
    logging.info(f"Starting subprocess: {command}")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Completed subprocess for {start_date} to {end_date}")
        else:
            logging.error(f"Error in subprocess: {result.stderr}")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")

if __name__ == "__main__":
    setup_logging()

    START_DATE = datetime.strptime("2014-05-01", "%Y-%m-%d")
    END_DATE = datetime.strptime("2025-06-30", "%Y-%m-%d")
    processes = []

    current_date = START_DATE
    while current_date <= END_DATE:
        year_end = datetime(current_date.year, 12, 31)
        if year_end > END_DATE:
            year_end = END_DATE

        # Start a new process for each year
        p = multiprocessing.Process(target=run_downloader, args=(current_date, year_end))
        processes.append(p)
        p.start()
        
        logging.info(f"Started process for {current_date.year}")

        current_date = datetime(current_date.year + 1, 1, 1)

    for p in processes:
        p.join()

    logging.info("All processes completed.")
