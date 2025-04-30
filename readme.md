# 📸 Google Photos Auto-Sync Tool

Automatically upload new photos from a local folder to your Google Photos account, organizing them into a specific album. If the album doesn’t exist, it is created automatically.

---

## ✅ Features

- 🔐 Google OAuth2 authentication
- 📂 Watches a local folder for new image files
- ☁️ Uploads new images to Google Photos
- 🗂️ Adds uploaded images to a specified album
- 🪶 Lightweight and CLI-based — no external UI required

---

## 🚀 Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/google-photos-sync.git
cd google-photos-sync
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Enable Google Photos API

- Go to Google Cloud Console
- Create a new project
- Enable the Google Photos Library API
- Go to APIs & Services > Credentials
- Create OAuth 2.0 Client ID (Application type: Desktop App)
- Download the credentials.json and place it in the project's root directory

### 4. Run the script

```bash
python photo_sync.py
```

The first time, it will open a browser window for you to log in and authorize the app.

### 5. Configuration

Copy the .env.sample to a .env file and add the necessary values.

You can change ALBUM_TITLE to any name you like — the album will be created if it doesn’t already exist.

### 6. Permissions

This script uses the following Google Photos scope:

```bash
https://www.googleapis.com/auth/photoslibrary.appendonly
```

This allows uploading photos and creating albums. It does not allow reading or deleting existing photos.

### 7. What's Coming Next

I'm actively working on improving this tool to make it production-ready and more user-friendly:

🚀 Published App Mode
No more need to create your own credentials — a verified version will be available that you can install and authorize with one click.

⚙️ Autostart on Boot
Automatically launch the sync script at system startup (macOS, Windows, Linux supported).

⚡ Parallel Uploads
Improve performance by uploading multiple images in parallel with intelligent retry and throttling logic.

📆 Smart Album Organization
Automatically organize uploads by day/week/month using dynamic album names like Uploads - April 2025.

📹 Video File Support
Add support for .mp4, .mov, and other common video formats.

🧊 Cross-Platform Installer
Bundle the app into a one-click executable (with Python and dependencies included).

🪟 Optional GUI
Lightweight config panel for selecting the folder and toggling options like startup sync.
