import os
import time
import mimetypes
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

WATCH_FOLDER = os.getenv("WATCH_FOLDER", "./photos")
ALBUM_ID = os.getenv("ALBUM_ID", None)
SCOPES = [scope.strip() for scope in os.getenv("SCOPES", "https://www.googleapis.com/auth/photoslibrary.appendonly").split(",")]

def get_authenticated_credentials():
    token_path = 'token.json'
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

creds = get_authenticated_credentials()

def upload_photo(file_path, album_id=None):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith('image/'):
        print(f"❌ Skipping non-image file: {file_path}")
        return

    print(f"📤 Uploading {file_path} to Google Photos...")

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-File-Name": os.path.basename(file_path),
        "X-Goog-Upload-Protocol": "raw"
    }

    with open(file_path, 'rb') as image_file:
        upload_response = requests.post(
            url='https://photoslibrary.googleapis.com/v1/uploads',
            data=image_file,
            headers=headers
        )

    upload_token = upload_response.text.strip()

    if upload_response.status_code != 200 or not upload_token:
        print(f"❌ Upload failed: {upload_response.text}")
        return

    create_item_body = {
        "newMediaItems": [
            {
                "description": "Synced from device",
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }
        ]
    }

    create_response = requests.post(
        url='https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
        headers={"Authorization": f"Bearer {creds.token}"},
        json=create_item_body
    )

    if create_response.status_code != 200:
        print(f"❌ Failed to create media item: {create_response.text}")
        return

    print(f"✅ Uploaded: {file_path}")

    # if album_id:
    #     try:
    #         created_item = create_response.json().get("newMediaItemResults", [])[0]
    #         media_item_id = created_item.get("mediaItem", {}).get("id")

    #         if media_item_id:
    #             add_response = requests.post(
    #                 url=f"https://photoslibrary.googleapis.com/v1/albums/{album_id}:batchAddMediaItems",
    #                 headers={"Authorization": f"Bearer {creds.token}"},
    #                 json={"mediaItemIds": [media_item_id]}
    #             )

    #             if add_response.status_code == 200:
    #                 print(f"📁 Added to album: {album_id}")
    #             else:
    #                 print(f"⚠️ Failed to add to album: {album_id} {add_response.text}")
    #     except Exception as e:
    #         print(f"⚠️ Could not add to album: {e}")

# === File Watcher ===
class NewPhotoHandler(FileSystemEventHandler):
    def __init__(self, album_id):
        self.album_id = album_id

    def on_created(self, event):
        if not event.is_directory:
            upload_photo(event.src_path, album_id=self.album_id)

def start_watching():
    observer = Observer()
    observer.schedule(NewPhotoHandler(ALBUM_ID), path=WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching {WATCH_FOLDER} for new photos... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    start_watching()
