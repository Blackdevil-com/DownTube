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
            tmp = d.get("tmpfilename")  # ✅ REAL temp file
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
        }


    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    elif video_only:
        ydl_opts.update({
            "format": f"bestvideo[height={resolution}]/best",
            "merge_output_format": "mp4",
            "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
            }]
        })

    else:
        ydl_opts.update({
            "format": f"bestvideo[height={resolution}]+bestaudio/best",
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

        raise
