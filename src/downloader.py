import os
import yt_dlp

def download_youtube(url, resolution, progress_callback, control_flag, folder, audio_only, video_only):
    temp_files = set()

    def hook(d):
        if control_flag["cancel"]:
            raise Exception("Download cancelled")

        if control_flag["pause"]:
            raise Exception("Download paused")

        if d["status"] == "downloading":
            tmp = d.get("tmpfilename")
            if tmp:
                temp_files.add(tmp)

            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total:
                percent = (downloaded / total) * 100
                progress_callback(percent, downloaded, total)

    ydl_opts = {
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],
        "quiet": True,
        "restrictfilenames": True,
        "continuedl": True,
        "nopart": False,

        # 🔥 CRITICAL FIX
        # "extractor_args": {
        #     "youtube": {
        #         "player_client": ["android"]
        #     }
        # },
    }

    # 🎵 AUDIO ONLY
    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    # 🎥 VIDEO ONLY (MP4 preferred, fallback allowed)
    elif video_only:
        ydl_opts.update({
            "format": (
                f"bestvideo[ext=mp4][height<={resolution}]/"
            ),
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }],
        })

    # 🎬 VIDEO + AUDIO
    else:
        ydl_opts.update({
            "format": (
                f"bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/"
            ),
            "merge_output_format": "mp4",
            "postprocessor_args": ["-c:a", "aac"],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        if "cancelled" in str(e).lower():
            for f in temp_files:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except Exception:
                    pass
            raise Exception("Download cancelled")
        if "requested format is not available" in str(e).lower():
            raise Exception(
                "Selected quality is not available in MP4.\n"
                "Or check for new version"
        )

        raise
