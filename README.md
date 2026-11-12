# YTVideoD – YouTube Video & Playlist Downloader

**YTVideoD** is a Python-based desktop application that allows users to download individual YouTube videos and entire playlists with multiple video quality options. It provides a user-friendly graphical interface with download progress tracking, pause/resume functionality, and download management.

## 🚀 Features

- **Single Video Download:** Download individual YouTube videos using their URLs.
- **Playlist Download:** Detect and extract videos from YouTube playlists.
- **Video Selection:** Select specific videos from a playlist using checkboxes.
- **Multiple Quality Options:** Choose from different resolutions:
  - Best Available
  - 2160p (4K)
  - 1440p
  - 1080p
  - 720p
  - 480p
  - 360p
- **Download Progress:** Monitor download progress, speed, and estimated remaining time.
- **Pause & Resume:** Pause, resume, or cancel downloads.
- **Automatic Retry:** Retry failed downloads and continue supported partial downloads.
- **Custom Download Location:** Choose your preferred folder for saving videos.
- **FFmpeg Integration:** Merge video and audio streams when required.
- **Download History:** Store previous download information using SQLite.
- **Application Settings:** Maintain application preferences using a local database.
- **Multithreading:** Perform downloads in background threads to keep the GUI responsive.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| CustomTkinter | Modern graphical user interface |
| yt-dlp | YouTube video and playlist extraction and downloading |
| Pillow (PIL) | Image and thumbnail handling |
| SQLite | Local database management |
| FFmpeg | Audio and video stream merging |
| Threading | Background download operations |

## 📂 Project Structure

```text
YTVideoD/
│
├── main.py              # Main application and GUI
├── playlist.py          # Playlist extraction and management
├── downloader.py        # Video downloading functionality
├── database.py          # SQLite database operations
├── settings.py          # Application settings
│
├── requirements.txt     # Python dependencies
│
├── data/                # Database and application data
├── downloads/           # Downloaded videos
├── thumbnails/          # Video thumbnails
│
└── README.md            # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd YTVideoD
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

FFmpeg is required for merging separate audio and video streams.

Download FFmpeg from:

https://ffmpeg.org/download.html

Make sure FFmpeg is properly installed and accessible through your system PATH.

### 5. Run the Application

```bash
py main.py
```

## 💻 How to Use

1. Launch the YTVideoD application.
2. Paste a YouTube video or playlist URL.
3. Allow the application to identify the video or playlist.
4. Select the videos you want to download.
5. Choose your preferred video resolution.
6. Select the destination folder.
7. Start downloading.
8. Monitor download progress, speed, and estimated time.
9. Pause, resume, or cancel downloads whenever required.

## 🗄️ Database Management

YTVideoD uses SQLite for local data storage.

The database maintains:

- **download_history:** Stores information about previous downloads.
- **app_settings:** Stores application preferences and configuration.

SQLite eliminates the need for a separate database server.

## 🔒 Error Handling

The application includes handling for:

- Invalid YouTube URLs.
- Network interruptions.
- Failed downloads.
- Unavailable videos.
- Download interruptions.
- Missing FFmpeg dependencies.

The application does not bypass private-video restrictions, unavailable content, or access controls.

## 🎯 Project Objectives

- Develop a desktop-based YouTube video downloader.
- Provide an easy-to-use graphical interface.
- Support both individual video and playlist downloads.
- Implement download management with pause and resume functionality.
- Integrate SQLite for persistent application data.
- Apply multithreading for better application responsiveness.

## 🔮 Future Enhancements

- Audio-only download support.
- Download scheduling.
- Improved download queue management.
- Enhanced download history interface.
- Additional format selection options.
- Improved application themes and UI customization.

## 👨‍💻 Developer

**Developed by:** Deepak Singh

**Project Name:** YTVideoD – YouTube Video Downloader

**Language:** Python

**Project Type:** Desktop Application

---

**Note:** Use this application only for content you own or have permission to download. Follow YouTube's Terms of Service and applicable copyright laws.
