import requests
import os
import time

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_file(file):
    # Use unique file name with timestamp
    file_name = f"{int(time.time())}_{file.name}"

    # Supabase storage upload URL
    url = f"{SUPABASE_URL}/storage/v1/object/media/{file_name}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        # Content-Type should match the file content type
        "Content-Type": getattr(file, 'content_type', 'application/octet-stream'),
    }

    # Upload the file data
    # We use file.read() to get the bytes, or just pass 'file' if it's a file-like object
    # In Django request.FILES, it's an UploadedFile object which can be read.
    response = requests.post(url, headers=headers, data=file)

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to upload to Supabase: {response.text}")

    # Public URL for the file (assuming bucket 'media' is public)
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/media/{file_name}"

    return public_url
