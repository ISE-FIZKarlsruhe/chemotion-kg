import os
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

API_URL = "https://www.chemotion-repository.net/api/v1/public/metadata/publications"
SAVE_DIR = "data"
LIMIT = 1000  # API limit per request
MAX_WORKERS = 10  # Number of concurrent downloads

# Function to create folder structure
def create_directory_structure(year, month):
    folder_path = os.path.join(SAVE_DIR, str(year), f"{month:02d}")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Function to sanitize filenames
def sanitize_filename(filename):
    return filename.replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_").replace("\\", "_")

# Function to download JSON-LD file
def download_file(url, save_folder):
    sanitized_name = sanitize_filename(url.split("inchikey=")[-1]) + ".jsonld"
    save_path = os.path.join(save_folder, sanitized_name)
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Saved: {save_path}")
    else:
        print(f"Failed to download {url}")

# Function to fetch and save data within date range
def fetch_and_save_data(start_date, end_date):
    current_date = start_date

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while current_date <= end_date:
            period_start = current_date.strftime("%Y-%m-%d")
            period_end = (current_date + timedelta(days=30)).strftime("%Y-%m-%d")

            offset = 0
            more_data = True
            tasks = []

            while more_data:
                params = {
                    "type": "Container",
                    "offset": offset,
                    "limit": LIMIT,
                    "date_from": period_start,
                    "date_to": period_end,
                }

                response = requests.get(API_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    publications = data.get("publications", [])
                    
                    if not publications:
                        more_data = False
                        break

                    save_folder = create_directory_structure(current_date.year, current_date.month)
                    for pub_url in publications:
                        tasks.append(executor.submit(download_file, pub_url, save_folder))

                    for future in as_completed(tasks):
                        future.result()

                    offset += LIMIT
                else:
                    print(f"Error fetching data: {response.status_code}")
                    more_data = False

            current_date += timedelta(days=31)
            current_date = current_date.replace(day=1)

if __name__ == "__main__":
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    fetch_and_save_data(start_date, end_date)
