import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_image(url):
    try:
        os.makedirs("Fetched_Images", exist_ok=True)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename or "." not in filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join("Fetched_Images", filename)

        filehash = hashlib.md5(response.content).hexdigest()
        existing_files = os.listdir("Fetched_Images")
        for file in existing_files:
            with open(os.path.join("Fetched_Images", file), "rb") as f:
                if hashlib.md5(f.read()).hexdigest() == filehash:
                    print(f"✗ Duplicate found: {filename} (already saved as {file})")
                    return

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("Connecting communities through shared images\n")

    url = input("Enter the image URL: ").strip()
    fetch_image(url)

if __name__ == "__main__":
    main()
