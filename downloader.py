import os

import shutil

import threading


import yt_dlp


class PauseDownload(Exception):

    """Internal exception used to pause a download."""

    pass


class CancelDownload(Exception):

    """Internal exception used to cancel a download."""

    pass


class VideoDownloader:


    def __init__(

        self,

        download_folder,

        progress_callback=None,

        quality="Best Available"

    ):


        self.download_folder = download_folder


        self.progress_callback = progress_callback


        self.quality = quality


        self.current_video = None

        self.last_file_path = ""


        # -----------------------------------------------------

        # Download control events

        # -----------------------------------------------------


        self.pause_event = threading.Event()


        self.cancel_event = threading.Event()


        # -----------------------------------------------------

        # Create download folder

        # -----------------------------------------------------


        os.makedirs(

            self.download_folder,

            exist_ok=True

        )


        # -----------------------------------------------------

        # Detect FFmpeg

        # -----------------------------------------------------


        self.ffmpeg_path = shutil.which(

            "ffmpeg"

        )


    # =========================================================

    # QUALITY FORMAT

    # =========================================================


    def get_format(self):


        quality_map = {


            "Best Available": None,


            "2160p": 2160,


            "1440p": 1440,


            "1080p": 1080,


            "720p": 720,


            "480p": 480,


            "360p": 360

        }


        height = quality_map.get(

            self.quality

        )


        # -----------------------------------------------------

        # Best available

        # -----------------------------------------------------


        if height is None:


            return "bv*+ba/b"


        # -----------------------------------------------------

        # Selected maximum resolution

        # -----------------------------------------------------


        return (

            f"bv*[height<={height}]+"

            f"ba/b[height<={height}]/"

            f"b[height<={height}]"

        )


    # =========================================================

    # PAUSE

    # =========================================================


    def pause(self):


        if self.current_video:


            self.pause_event.set()


    # =========================================================

    # RESUME

    # =========================================================


    def resume(self):


        self.pause_event.clear()


    # =========================================================

    # CANCEL

    # =========================================================


    def cancel(self):


        if self.current_video:


            self.cancel_event.set()


    # =========================================================

    # DOWNLOAD VIDEO

    # =========================================================


    def download_video(self, video):


        self.current_video = video


        # Reset cancellation for this video

        self.cancel_event.clear()


        video_url = video.get(

            "url"

        )


        if not video_url:


            self.send_progress(

                video,

                {

                    "status": "error",

                    "percent": 0,

                    "message": "Video URL not available"

                }

            )


            return "error"


        # -----------------------------------------------------

        # Output filename

        # -----------------------------------------------------


        output_template = os.path.join(

            self.download_folder,

            "%(title)s.%(ext)s"

        )


        # -----------------------------------------------------

        # FFmpeg

        # -----------------------------------------------------


        if self.ffmpeg_path:


            selected_format = self.get_format()


            merge_format = "mp4"


        else:


            # Without FFmpeg use a single-file format

            selected_format = (

                "b[ext=mp4]/b"

            )


            merge_format = None


        # -----------------------------------------------------

        # yt-dlp options

        # -----------------------------------------------------


        options = {


            "format": selected_format,


            "outtmpl": output_template,


            # Resume .part files

            "continuedl": True,


            # Don't overwrite completed files

            "nooverwrites": True,


            # Retry temporary failures

            "retries": 10,


            "fragment_retries": 10,


            "retry_sleep": {

                "http": 5,

                "fragment": 5,

                "extractor": 5

            },


            "windowsfilenames": True,


            "noplaylist": True,


            "quiet": True,


            "no_warnings": True,


            "progress_hooks": [

                self.progress_hook

            ],

            "postprocessor_hooks": [

                self.postprocessor_hook

            ]

        }


        if merge_format:


            options["merge_output_format"] = merge_format


        # -----------------------------------------------------

        # Starting

        # -----------------------------------------------------


        self.send_progress(

            video,

            {

                "status": "starting",

                "percent": 0,

                "message": "Starting..."

            }

        )


        # -----------------------------------------------------

        # FFmpeg warning

        # -----------------------------------------------------


        if not self.ffmpeg_path:


            self.send_progress(

                video,

                {

                    "status": "warning",

                    "percent": 0,

                    "message":

                    "FFmpeg not found - using single-file format"

                }

            )


        # =====================================================

        # DOWNLOAD

        # =====================================================


        try:


            with yt_dlp.YoutubeDL(

                options

            ) as ydl:


                ydl.download(

                    [video_url]

                )


            # -------------------------------------------------

            # Cancellation check

            # -------------------------------------------------


            if self.cancel_event.is_set():


                self.send_progress(

                    video,

                    {

                        "status": "cancelled",

                        "percent": 0,

                        "message":

                        "Cancelled - partial file kept",

                        "file_path": self.last_file_path

                    }

                )


                return "cancelled"


            # -------------------------------------------------

            # Completed

            # -------------------------------------------------


            self.send_progress(

                video,

                {

                    "status": "completed",

                    "percent": 100,

                    "message": "Completed",
                    "file_path": self.last_file_path

                }

            )


            return "completed"


        except PauseDownload:


            self.send_progress(

                video,

                {

                    "status": "paused",

                    "percent": 0,

                    "message":

                    "Paused - partial file saved",

                    "file_path": self.last_file_path

                }

            )


            return "paused"


        except CancelDownload:


            self.send_progress(

                video,

                {

                    "status": "cancelled",

                    "percent": 0,

                    "message":

                    "Cancelled - partial file kept",

                    "file_path": self.last_file_path

                }

            )


            return "cancelled"


        except yt_dlp.utils.DownloadError as e:


            error_message = str(e)


            # -------------------------------------------------

            # Friendly error messages

            # -------------------------------------------------


            if "Private video" in error_message:


                friendly = "Private video"


            elif "Video unavailable" in error_message:


                friendly = "Video unavailable"


            elif "Sign in" in error_message:


                friendly = "YouTube requires sign-in"


            elif "HTTP Error 403" in error_message:


                friendly = (

                    "Access denied by YouTube (HTTP 403)"

                )


            elif "HTTP Error 404" in error_message:


                friendly = (

                    "Video not found (HTTP 404)"

                )


            elif "ffmpeg" in error_message.lower():


                friendly = (

                    "FFmpeg problem: "

                    + error_message

                )


            else:


                friendly = error_message


            self.send_progress(

                video,

                {

                    "status": "error",

                    "percent": 0,

                    "message": friendly,
                    "file_path": self.last_file_path

                }

            )


            return "error"


        except Exception as e:


            self.send_progress(

                video,

                {

                    "status": "error",

                    "percent": 0,

                    "message": str(e),
                    "file_path": self.last_file_path

                }

            )


            return "error"


        finally:


            self.current_video = None


    # =========================================================

    def postprocessor_hook(self, data):

        file_path = data.get("filepath")

        if not file_path:
            file_path = data.get("_filename")

        if file_path:
            self.last_file_path = file_path


    # PROGRESS HOOK

    # =========================================================


    def progress_hook(self, data):


        # -----------------------------------------------------

        # Cancel

        # -----------------------------------------------------


        if self.cancel_event.is_set():


            raise CancelDownload()


        # -----------------------------------------------------

        # Pause

        # -----------------------------------------------------


        if self.pause_event.is_set():


            raise PauseDownload()


        status = data.get(

            "status"

        )


        # =====================================================

        # DOWNLOADING

        # =====================================================


        if status == "downloading":


            downloaded = data.get(

                "downloaded_bytes",

                0

            )


            total = data.get(

                "total_bytes"

            )


            if total is None:


                total = data.get(

                    "total_bytes_estimate"

                )


            if total:


                percent = (

                    downloaded / total

                ) * 100


            else:


                percent = 0


            speed = data.get(

                "speed"

            )


            eta = data.get(

                "eta"

            )


            self.send_progress(

                self.current_video,

                {

                    "status": "downloading",


                    "percent": percent,


                    "downloaded": downloaded,


                    "total": total,


                    "speed": speed,


                    "eta": eta,


                    "message": "Downloading..."

                }

            )


        # =====================================================

        # FINISHED DOWNLOAD / PROCESSING

        # =====================================================


        elif status == "finished":


            self.send_progress(

                self.current_video,

                {

                    "status": "processing",


                    "percent": 100,


                    "message":

                    "Processing / merging..."

                }

            )


    # =========================================================

    # SEND PROGRESS TO GUI

    # =========================================================


    def send_progress(

        self,

        video,

        data

    ):


        if self.progress_callback:


            self.progress_callback(

                video,

                data

            )
