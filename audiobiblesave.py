import csv
import os
import re
import requests

# Set your exact paths here:
CSV_FILE_PATH = '/Users/tag-4974/youtube-search-project/AudioBible/Reference Sheet/test.csv'
DOWNLOAD_FOLDER = '/Users/tag-4974/youtube-search-project/AudioBible/Downloads'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', '', text)

with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    for row in reader:
        if len(row) < 4:
            continue
        
        book = sanitize_filename(row[0].strip())
        chapter = str(row[1]).strip().zfill(2)
        mp3_link = row[2].strip()
        version = sanitize_filename(row[3].strip())
        
        filename = f"{chapter}_{book} {version}.mp3"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        try:
            print(f"Downloading: {filename}")
            response = requests.get(mp3_link, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Saved to: {filepath}")
        
        except Exception as e:
            print(f"Failed to download {mp3_link}: {e}")
