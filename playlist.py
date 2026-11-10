import yt_dlp


def get_playlist_info(url):

    url = url.strip()

    if not url:
        return None, "Please enter a YouTube URL."

    options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

        if not info:
            return None, "Could not retrieve video information."

        # =====================================================
        # SINGLE VIDEO
        # =====================================================

        if info.get("_type") != "playlist":

            video_id = info.get("id")

            if not video_id:
                return None, "Could not find video ID."

            title = info.get(
                "title",
                "Unknown Video"
            )

            webpage_url = info.get(
                "webpage_url"
            )

            if not webpage_url:

                webpage_url = (
                    f"https://www.youtube.com/watch?v={video_id}"
                )

            video = {
                "index": 1,
                "title": title,
                "id": video_id,
                "url": webpage_url
            }

            return {
                "title": title,
                "videos": [video],
                "type": "single"
            }, None

        # =====================================================
        # PLAYLIST
        # =====================================================

        playlist_title = info.get(
            "title",
            "YouTube Playlist"
        )

        entries = info.get(
            "entries",
            []
        )

        videos = []

        index = 1

        for entry in entries:

            if not entry:
                continue

            video_id = entry.get("id")

            if not video_id:
                continue

            title = entry.get(
                "title",
                f"Video {index}"
            )

            webpage_url = entry.get(
                "webpage_url"
            )

            if not webpage_url:

                webpage_url = (
                    f"https://www.youtube.com/watch?v={video_id}"
                )

            videos.append(
                {
                    "index": index,
                    "title": title,
                    "id": video_id,
                    "url": webpage_url
                }
            )

            index += 1

        if not videos:

            return None, "No videos found in this playlist."

        return {
            "title": playlist_title,
            "videos": videos,
            "type": "playlist"
        }, None

    except yt_dlp.utils.DownloadError as e:

        return None, str(e)

    except Exception as e:

        return None, str(e)