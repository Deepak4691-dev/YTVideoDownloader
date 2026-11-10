import os

import threading

import tkinter as tk

from tkinter import filedialog


import customtkinter as ctk


from playlist import get_playlist_info

from downloader import VideoDownloader
from database import get_download_history, clear_download_history, add_download_history


# ============================================================

# APPEARANCE

# ============================================================


ctk.set_appearance_mode("dark")


ctk.set_default_color_theme("blue")


# ============================================================

# MAIN APPLICATION

# ============================================================


class YTVideoD(ctk.CTk):


    def __init__(self):


        super().__init__()


        # ----------------------------------------------------

        # Window

        # ----------------------------------------------------


        self.title(

            "YTVideoD - YouTube Video Downloader"

        )


        self.geometry(

            "1450x950"

        )


        self.minsize(

            1100,

            750

        )


        # ----------------------------------------------------

        # Data

        # ----------------------------------------------------


        self.playlist_videos = []


        self.selected_videos = []


        self.video_vars = {}


        self.queue_rows = {}


        # ----------------------------------------------------

        # Download state

        # ----------------------------------------------------


        self.downloader = None


        self.download_thread = None


        self.downloading = False


        self.paused = False


        self.current_index = 0
        self.download_quality = "Best Available"


        # ====================================================

        # HEADER

        # ====================================================


        self.header = ctk.CTkFrame(

            self,

            corner_radius=0

        )


        self.header.pack(

            fill="x"

        )


        self.title_label = ctk.CTkLabel(

            self.header,

            text="YTVideoD",

            font=ctk.CTkFont(

                size=38,

                weight="bold"

            )

        )


        self.title_label.pack(

            pady=(20, 0)

        )


        self.subtitle_label = ctk.CTkLabel(

            self.header,

            text=(

                "YouTube Playlist & Single Video "

                "Download Manager"

            ),

            font=ctk.CTkFont(

                size=18

            )

        )


        self.subtitle_label.pack(

            pady=(0, 20)

        )


        # ====================================================

        # MAIN SCROLL AREA

        # ====================================================


        self.main_scroll = ctk.CTkScrollableFrame(

            self

        )


        self.main_scroll.pack(

            fill="both",

            expand=True,

            padx=8,

            pady=8

        )


        # ====================================================

        # URL SECTION

        # ====================================================


        self.url_frame = ctk.CTkFrame(

            self.main_scroll

        )


        self.url_frame.pack(

            fill="x",

            pady=(0, 10)

        )


        self.url_title = ctk.CTkLabel(

            self.url_frame,

            text="YouTube URL",

            font=ctk.CTkFont(

                size=20,

                weight="bold"

            )

        )


        self.url_title.pack(

            pady=(18, 8)

        )


        self.url_row = ctk.CTkFrame(

            self.url_frame,

            fg_color="transparent"

        )


        self.url_row.pack(

            fill="x",

            padx=18,

            pady=(0, 18)

        )


        self.url_entry = ctk.CTkEntry(

            self.url_row,

            placeholder_text=(

                "Paste YouTube playlist or "

                "single video URL..."

            ),

            height=38

        )


        self.url_entry.pack(

            side="left",

            fill="x",

            expand=True,

            padx=(0, 12)

        )


        self.load_button = ctk.CTkButton(

            self.url_row,

            text="LOAD URL",

            width=200,

            height=38,

            command=self.load_playlist

        )


        self.load_button.pack(

            side="right"

        )


        # ====================================================

        # CONTENTS

        # ====================================================


        self.playlist_frame = ctk.CTkFrame(

            self.main_scroll

        )


        self.playlist_frame.pack(

            fill="x",

            pady=(0, 10)

        )


        self.playlist_title = ctk.CTkLabel(

            self.playlist_frame,

            text="Video / Playlist Contents",

            font=ctk.CTkFont(

                size=20,

                weight="bold"

            )

        )


        self.playlist_title.pack(

            pady=(18, 8)

        )


        self.playlist_scroll = ctk.CTkScrollableFrame(

            self.playlist_frame,

            height=280

        )


        self.playlist_scroll.pack(

            fill="x",

            padx=12,

            pady=5

        )


        self.playlist_buttons = ctk.CTkFrame(

            self.playlist_frame,

            fg_color="transparent"

        )


        self.playlist_buttons.pack(

            fill="x",

            padx=18,

            pady=(8, 18)

        )


        self.select_all_button = ctk.CTkButton(

            self.playlist_buttons,

            text="SELECT ALL",

            width=160,

            command=self.select_all

        )


        self.select_all_button.pack(

            side="left",

            padx=(0, 12)

        )


        self.clear_all_button = ctk.CTkButton(

            self.playlist_buttons,

            text="CLEAR ALL",

            width=160,

            command=self.clear_all

        )


        self.clear_all_button.pack(

            side="left"

        )


        self.add_selected_button = ctk.CTkButton(

            self.playlist_buttons,

            text="ADD SELECTED",

            width=190,

            command=self.add_selected

        )


        self.add_selected_button.pack(

            side="right"

        )


        # ====================================================

        # DOWNLOAD QUEUE

        # ====================================================


        self.queue_frame = ctk.CTkFrame(

            self.main_scroll

        )


        self.queue_frame.pack(

            fill="x",

            pady=(0, 10)

        )


        self.queue_title = ctk.CTkLabel(

            self.queue_frame,

            text="Selected Items / Download Queue",

            font=ctk.CTkFont(

                size=20,

                weight="bold"

            )

        )


        self.queue_title.pack(

            pady=(18, 8)

        )


        self.queue_scroll = ctk.CTkScrollableFrame(

            self.queue_frame,

            height=280

        )


        self.queue_scroll.pack(

            fill="x",

            padx=12,

            pady=(5, 18)

        )


        # ====================================================

        # SETTINGS

        # ====================================================


        self.settings_frame = ctk.CTkFrame(

            self.main_scroll

        )


        self.settings_frame.pack(

            fill="x",

            pady=(0, 10)

        )


        # ----------------------------------------------------

        # Folder

        # ----------------------------------------------------


        self.folder_label = ctk.CTkLabel(

            self.settings_frame,

            text="Download Location"

        )


        self.folder_label.grid(

            row=0,

            column=0,

            padx=12,

            pady=(18, 5),

            sticky="w"

        )


        self.folder_entry = ctk.CTkEntry(

            self.settings_frame,

            height=38

        )


        self.folder_entry.grid(

            row=1,

            column=0,

            padx=12,

            pady=(0, 18),

            sticky="ew"

        )


        default_folder = os.path.join(

            os.path.expanduser("~"),

            "Downloads",

            "YTVideoD"

        )


        self.folder_entry.insert(

            0,

            default_folder

        )


        self.folder_button = ctk.CTkButton(

            self.settings_frame,

            text="CHOOSE FOLDER",

            width=190,

            height=38,

            command=self.choose_folder

        )


        self.folder_button.grid(

            row=1,

            column=1,

            padx=12,

            pady=(0, 18)

        )


        # ----------------------------------------------------

        # Quality

        # ----------------------------------------------------


        self.quality_label = ctk.CTkLabel(

            self.settings_frame,

            text="Video Quality"

        )


        self.quality_label.grid(

            row=0,

            column=2,

            padx=12,

            pady=(18, 5),

            sticky="w"

        )


        self.quality_menu = ctk.CTkOptionMenu(

            self.settings_frame,

            values=[

                "Best Available",

                "2160p",

                "1440p",

                "1080p",

                "720p",

                "480p",

                "360p"

            ],

            width=190,

            height=38

        )


        self.quality_menu.set(

            "Best Available"

        )


        self.quality_menu.grid(

            row=1,

            column=2,

            padx=12,

            pady=(0, 18)

        )


        self.settings_frame.grid_columnconfigure(

            0,

            weight=1

        )


        # ====================================================

        # CONTROL BUTTONS

        # ====================================================


        self.control_frame = ctk.CTkFrame(

            self.main_scroll

        )


        self.control_frame.pack(

            fill="x",

            pady=(0, 10)

        )


        self.start_button = ctk.CTkButton(

            self.control_frame,

            text="START DOWNLOAD",

            height=45,

            command=self.start_download

        )


        self.start_button.pack(

            side="left",

            fill="x",

            expand=True,

            padx=(15, 6),

            pady=15

        )


        self.pause_button = ctk.CTkButton(

            self.control_frame,

            text="PAUSE",

            height=45,

            command=self.pause_download,

            state="disabled"

        )


        self.pause_button.pack(

            side="left",

            fill="x",

            expand=True,

            padx=6,

            pady=15

        )


        self.resume_button = ctk.CTkButton(

            self.control_frame,

            text="RESUME",

            height=45,

            command=self.resume_download,

            state="disabled"

        )


        self.resume_button.pack(

            side="left",

            fill="x",

            expand=True,

            padx=6,

            pady=15

        )


        self.cancel_button = ctk.CTkButton(

            self.control_frame,

            text="CANCEL CURRENT",

            height=45,

            command=self.cancel_download,

            state="disabled"

        )


        self.cancel_button.pack(

            side="left",

            fill="x",

            expand=True,

            padx=(6, 15),

            pady=15

        )


        # ====================================================

        # DOWNLOAD HISTORY

        self.history_frame = ctk.CTkFrame(
            self.main_scroll
        )
        self.history_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.history_title = ctk.CTkLabel(
            self.history_frame,
            text="Download History",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.history_title.pack(pady=(18, 8))

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_frame,
            height=220
        )
        self.history_scroll.pack(
            fill="x",
            padx=12,
            pady=5
        )

        self.history_buttons = ctk.CTkFrame(
            self.history_frame,
            fg_color="transparent"
        )
        self.history_buttons.pack(
            fill="x",
            padx=18,
            pady=(8, 18)
        )

        self.refresh_history_button = ctk.CTkButton(
            self.history_buttons,
            text="REFRESH HISTORY",
            width=180,
            command=self.load_history
        )
        self.refresh_history_button.pack(side="left")

        self.clear_history_button = ctk.CTkButton(
            self.history_buttons,
            text="CLEAR HISTORY",
            width=180,
            command=self.clear_history
        )
        self.clear_history_button.pack(side="right")

        # STATUS

        self.status_label = ctk.CTkLabel(
            self.main_scroll,
            text="Ready",
            font=ctk.CTkFont(size=15)
        )
        self.status_label.pack(
            pady=(5, 20)
        )

        self.load_history()

    # DATABASE - DOWNLOAD HISTORY

    def load_history(self):

        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        try:
            rows = get_download_history()
        except Exception as e:
            ctk.CTkLabel(
                self.history_scroll,
                text=f"Could not load history: {e}"
            ).pack(pady=15)
            return

        if not rows:
            ctk.CTkLabel(
                self.history_scroll,
                text="No download history yet."
            ).pack(pady=15)
            return

        for row_data in rows:
            row = ctk.CTkFrame(self.history_scroll)
            row.pack(fill="x", pady=4)

            title = row_data["title"] or "Unknown Video"
            status = row_data["status"] or "Unknown"
            quality = row_data["quality"] or "Unknown"
            downloaded_at = row_data["downloaded_at"] or ""
            file_path = row_data["file_path"] or ""

            ctk.CTkLabel(
                row, text=title, anchor="w"
            ).pack(fill="x", padx=12, pady=(8, 2))

            ctk.CTkLabel(
                row,
                text=f"Status: {status} | Quality: {quality} | {downloaded_at}",
                anchor="w"
            ).pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(
                row,
                text=file_path,
                anchor="w"
            ).pack(fill="x", padx=12, pady=(2, 8))

    def clear_history(self):

        clear_download_history()
        self.load_history()
        self.status_label.configure(
            text="Download history cleared."
        )

    def save_history_record(self, video, status, file_path=""):

        if not video:
            return

        try:
            add_download_history(
                video_id=video.get("id", ""),
                title=video.get("title", "Unknown Video"),
                url=video.get("url", ""),
                file_path=file_path or "",
                quality=self.download_quality,
                status=status
            )
        except Exception as e:
            print("Database error:", e)

        self.after(0, self.load_history)


    # LOAD URL

    # ========================================================


    def load_playlist(self):


        url = self.url_entry.get().strip()


        if not url:


            self.status_label.configure(

                text="Please enter a YouTube URL."

            )


            return


        self.load_button.configure(

            state="disabled",

            text="LOADING..."

        )


        self.status_label.configure(

            text="Loading..."

        )


        thread = threading.Thread(

            target=self.load_playlist_worker,

            args=(url,),

            daemon=True

        )


        thread.start()


    # ========================================================

    # LOAD WORKER

    # ========================================================


    def load_playlist_worker(

        self,

        url

    ):


        try:


            result, error = get_playlist_info(

                url

            )


            self.after(

                0,

                self.url_loaded,

                result,

                error

            )


        except Exception as e:


            self.after(

                0,

                self.url_loaded,

                None,

                str(e)

            )


    # ========================================================

    # URL LOADED

    # ========================================================


    def url_loaded(

        self,

        result,

        error

    ):


        self.load_button.configure(

            state="normal",

            text="LOAD URL"

        )


        if error:


            self.status_label.configure(

                text=f"Error: {error}"

            )


            return


        if not result:


            self.status_label.configure(

                text="Could not load URL."

            )


            return


        self.playlist_videos = result.get(

            "videos",

            []

        )


        content_type = result.get(

            "type",

            "playlist"

        )


        self.clear_playlist_widgets()


        self.video_vars.clear()


        # ----------------------------------------------------

        # Display videos

        # ----------------------------------------------------


        for video in self.playlist_videos:


            var = tk.BooleanVar(

                value=False

            )


            self.video_vars[

                video["id"]

            ] = var


            row = ctk.CTkFrame(

                self.playlist_scroll

            )


            row.pack(

                fill="x",

                pady=4

            )


            checkbox = ctk.CTkCheckBox(

                row,

                text=(

                    f'{video.get("index", "")}. '

                    f'{video.get("title", "Unknown")}'

                ),

                variable=var

            )


            checkbox.pack(

                fill="x",

                padx=12,

                pady=12

            )


        # ----------------------------------------------------

        # Status

        # ----------------------------------------------------


        if content_type == "single":


            self.status_label.configure(

                text="Single video loaded successfully."

            )


            # Automatically select the single video

            if self.playlist_videos:


                first_video = self.playlist_videos[0]


                self.video_vars[

                    first_video["id"]

                ].set(True)


        else:


            self.status_label.configure(

                text=(

                    f"Playlist loaded: "

                    f"{len(self.playlist_videos)} videos"

                )

            )


    # ========================================================

    # CLEAR CONTENTS

    # ========================================================


    def clear_playlist_widgets(self):


        for widget in (

            self.playlist_scroll.winfo_children()

        ):


            widget.destroy()


    # ========================================================

    # SELECT ALL

    # ========================================================


    def select_all(self):


        for var in self.video_vars.values():


            var.set(True)


    # ========================================================

    # CLEAR ALL

    # ========================================================


    def clear_all(self):


        for var in self.video_vars.values():


            var.set(False)


    # ========================================================

    # ADD SELECTED

    # ========================================================


    def add_selected(self):


        if self.downloading:


            self.status_label.configure(

                text=(

                    "Cannot modify queue "

                    "while downloading."

                )

            )


            return


        selected = []


        for video in self.playlist_videos:


            var = self.video_vars.get(

                video["id"]

            )


            if var and var.get():


                selected.append(

                    video

                )


        if not selected:


            self.status_label.configure(

                text=(

                    "Please select at least "

                    "one video."

                )

            )


            return


        self.selected_videos = selected


        self.build_queue()


        self.status_label.configure(

            text=(

                f"{len(selected)} video(s) "

                "added to queue."

            )

        )


    # ========================================================

    # BUILD QUEUE

    # ========================================================


    def build_queue(self):


        for widget in (

            self.queue_scroll.winfo_children()

        ):


            widget.destroy()


        self.queue_rows.clear()


        for video in self.selected_videos:


            video_id = video["id"]


            row = ctk.CTkFrame(

                self.queue_scroll

            )


            row.pack(

                fill="x",

                pady=5,

                padx=2

            )


            # ------------------------------------------------

            # Title / status

            # ------------------------------------------------


            top = ctk.CTkFrame(

                row,

                fg_color="transparent"

            )


            top.pack(

                fill="x",

                padx=10,

                pady=(10, 5)

            )


            title = ctk.CTkLabel(

                top,

                text=(

                    f'{video.get("index", "")}. '

                    f'{video.get("title", "Unknown")}'

                ),

                anchor="w"

            )


            title.pack(

                side="left",

                fill="x",

                expand=True

            )


            status = ctk.CTkLabel(

                top,

                text="Waiting"

            )


            status.pack(

                side="right"

            )


            # ------------------------------------------------

            # Progress

            # ------------------------------------------------


            progress = ctk.CTkProgressBar(

                row

            )


            progress.pack(

                fill="x",

                padx=12,

                pady=(3, 4)

            )


            progress.set(

                0

            )


            # ------------------------------------------------

            # Details

            # ------------------------------------------------


            details = ctk.CTkLabel(

                row,

                text="0% | Waiting",

                anchor="w"

            )


            details.pack(

                fill="x",

                padx=12,

                pady=(0, 10)

            )


            self.queue_rows[

                video_id

            ] = {

                "row": row,

                "title": title,

                "status": status,

                "progress": progress,

                "details": details

            }


    # ========================================================

    # CHOOSE FOLDER

    # ========================================================


    def choose_folder(self):


        folder = filedialog.askdirectory()


        if folder:


            self.folder_entry.delete(

                0,

                "end"

            )


            self.folder_entry.insert(

                0,

                folder

            )


    # ========================================================

    # START DOWNLOAD

    # ========================================================


    def start_download(self):


        if self.downloading:


            return


        if not self.selected_videos:


            self.status_label.configure(

                text=(

                    "Add videos to the "

                    "download queue first."

                )

            )


            return


        folder = self.folder_entry.get().strip()


        if not folder:


            self.status_label.configure(

                text=(

                    "Please select a download folder."

                )

            )


            return


        os.makedirs(

            folder,

            exist_ok=True

        )


        quality = self.quality_menu.get()
        self.download_quality = quality


        self.downloader = VideoDownloader(

            download_folder=folder,

            progress_callback=self.download_progress,

            quality=quality

        )


        self.current_index = 0


        self.paused = False


        self.downloading = True


        self.update_control_buttons()


        self.status_label.configure(

            text=(

                f"Downloading at {quality}..."

            )

        )


        self.download_thread = threading.Thread(

            target=self.download_all,

            daemon=True

        )


        self.download_thread.start()


    # ========================================================

    # DOWNLOAD QUEUE

    # ========================================================


    def download_all(self):


        while (

            self.current_index

            < len(self.selected_videos)

        ):


            video = self.selected_videos[

                self.current_index

            ]


            result = (

                self.downloader.download_video(

                    video

                )

            )


            # ------------------------------------------------

            # PAUSED

            # ------------------------------------------------


            if result == "paused":


                self.paused = True


                self.downloading = False


                self.after(

                    0,

                    self.update_control_buttons

                )


                self.after(

                    0,

                    self.status_label.configure,

                    {

                        "text":

                        "Download paused. "

                        "Click RESUME to continue."

                    }

                )


                return


            # ------------------------------------------------

            # CANCELLED

            # ------------------------------------------------


            if result == "cancelled":


                self.current_index += 1


                continue


            # ------------------------------------------------

            # COMPLETED / ERROR

            # ------------------------------------------------


            self.current_index += 1


        # ----------------------------------------------------

        # Queue finished

        # ----------------------------------------------------


        self.downloading = False


        self.paused = False


        self.after(

            0,

            self.update_control_buttons

        )


        self.after(

            0,

            self.status_label.configure,

            {

                "text":

                "Download queue completed."

            }

        )


    # ========================================================

    # PAUSE

    # ========================================================


    def pause_download(self):


        if not self.downloading:


            return


        if self.downloader:


            self.downloader.pause()


        self.status_label.configure(

            text="Pausing current download..."

        )


    # ========================================================

    # RESUME

    # ========================================================


    def resume_download(self):


        if not self.paused:


            return


        if not self.downloader:


            return


        self.downloader.resume()


        self.paused = False


        self.downloading = True


        self.update_control_buttons()


        self.status_label.configure(

            text="Resuming download..."

        )


        self.download_thread = threading.Thread(

            target=self.download_all,

            daemon=True

        )


        self.download_thread.start()


    # ========================================================

    # CANCEL

    # ========================================================


    def cancel_download(self):


        if not self.downloading:


            return


        if self.downloader:


            self.downloader.cancel()


        self.status_label.configure(

            text="Cancelling current download..."

        )


    # ========================================================

    # PROGRESS CALLBACK

    # ========================================================


    def download_progress(

        self,

        video,

        data

    ):


        self.after(

            0,

            self.update_queue_progress,

            video,

            data

        )


    # ========================================================

    # UPDATE PROGRESS

    # ========================================================


    def update_queue_progress(

        self,

        video,

        data

    ):


        if not video:


            return


        video_id = video.get(

            "id"

        )


        widgets = self.queue_rows.get(

            video_id

        )


        if not widgets:


            return


        status = data.get(

            "status",

            ""

        )


        percent = data.get(

            "percent",

            0

        )


        message = data.get(

            "message",

            ""

        )


        # ----------------------------------------------------

        # Progress bar

        # ----------------------------------------------------


        if percent is not None:


            widgets["progress"].set(

                max(

                    0,

                    min(

                        1,

                        percent / 100

                    )

                )

            )


        # ----------------------------------------------------

        # Starting

        # ----------------------------------------------------


        if status == "starting":


            widgets["status"].configure(

                text="Starting"

            )


            widgets["details"].configure(

                text="0% | Starting..."

            )


        # ----------------------------------------------------

        # Downloading

        # ----------------------------------------------------


        elif status == "downloading":


            speed = self.format_speed(

                data.get("speed")

            )


            eta = self.format_eta(

                data.get("eta")

            )


            widgets["status"].configure(

                text="Downloading"

            )


            widgets["details"].configure(

                text=(

                    f"{percent:.1f}% | "

                    f"{speed} | "

                    f"ETA: {eta}"

                )

            )


        # ----------------------------------------------------

        # Processing

        # ----------------------------------------------------


        elif status == "processing":


            widgets["status"].configure(

                text="Processing"

            )


            widgets["details"].configure(

                text=(

                    "100% | "

                    "Processing / merging..."

                )

            )


        # ----------------------------------------------------

        # Warning

        # ----------------------------------------------------


        elif status == "warning":


            widgets["status"].configure(

                text="Warning"

            )


            widgets["details"].configure(

                text=message

            )


        # ----------------------------------------------------

        # Paused

        # ----------------------------------------------------


        elif status == "paused":


            widgets["status"].configure(

                text="Paused"

            )


            widgets["details"].configure(

                text=(

                    "Paused | "

                    "Partial file saved"

                )

            )


        # ----------------------------------------------------

        # Cancelled

        # ----------------------------------------------------


        elif status == "cancelled":


            widgets["status"].configure(

                text="Cancelled"

            )


            widgets["details"].configure(

                text=(

                    "Cancelled | "

                    "Partial file kept"

                )

            )

            self.save_history_record(
                video, "Cancelled", data.get("file_path", "")
            )


        # ----------------------------------------------------

        # Completed

        # ----------------------------------------------------


        elif status == "completed":


            widgets["progress"].set(

                1

            )


            widgets["status"].configure(

                text="Completed"

            )


            widgets["details"].configure(

                text="100% | Completed"

            )

            self.save_history_record(
                video, "Completed", data.get("file_path", "")
            )


        # ----------------------------------------------------

        # Error

        # ----------------------------------------------------


        elif status == "error":


            widgets["status"].configure(

                text="Error"

            )


            widgets["details"].configure(

                text=message

            )

            self.save_history_record(
                video, "Error", data.get("file_path", "")
            )


    # ========================================================

    # FORMAT SPEED

    # ========================================================


    def format_speed(

        self,

        speed

    ):


        if not speed:


            return "--"


        if speed < 1024:


            return f"{speed:.0f} B/s"


        if speed < 1024 * 1024:


            return (

                f"{speed / 1024:.1f} KB/s"

            )


        if speed < 1024 * 1024 * 1024:


            return (

                f"{speed / (1024 * 1024):.1f} MB/s"

            )


        return (

            f"{speed / (1024 * 1024 * 1024):.1f} GB/s"

        )


    # ========================================================

    # FORMAT ETA

    # ========================================================


    def format_eta(

        self,

        eta

    ):


        if eta is None:


            return "--"


        try:


            eta = int(eta)


            minutes, seconds = divmod(

                eta,

                60

            )


            hours, minutes = divmod(

                minutes,

                60

            )


            if hours:


                return (

                    f"{hours}h {minutes}m"

                )


            if minutes:


                return (

                    f"{minutes}m {seconds}s"

                )


            return f"{seconds}s"


        except:


            return "--"


    # ========================================================

    # BUTTON STATES

    # ========================================================


    def update_control_buttons(self):


        # ----------------------------------------------------

        # Downloading

        # ----------------------------------------------------


        if self.downloading:


            self.start_button.configure(

                state="disabled"

            )


            self.pause_button.configure(

                state="normal"

            )


            self.resume_button.configure(

                state="disabled"

            )


            self.cancel_button.configure(

                state="normal"

            )


            self.load_button.configure(

                state="disabled"

            )


            self.add_selected_button.configure(

                state="disabled"

            )


        # ----------------------------------------------------

        # Paused

        # ----------------------------------------------------


        elif self.paused:


            self.start_button.configure(

                state="disabled"

            )


            self.pause_button.configure(

                state="disabled"

            )


            self.resume_button.configure(

                state="normal"

            )


            self.cancel_button.configure(

                state="disabled"

            )


            self.load_button.configure(

                state="disabled"

            )


            self.add_selected_button.configure(

                state="disabled"

            )


        # ----------------------------------------------------

        # Idle

        # ----------------------------------------------------


        else:


            self.start_button.configure(

                state="normal"

            )


            self.pause_button.configure(

                state="disabled"

            )


            self.resume_button.configure(

                state="disabled"

            )


            self.cancel_button.configure(

                state="disabled"

            )


            self.load_button.configure(

                state="normal"

            )


            self.add_selected_button.configure(

                state="normal"

            )


# ============================================================

# APPLICATION START

# ============================================================


if __name__ == "__main__":


    app = YTVideoD()


    app.mainloop()
