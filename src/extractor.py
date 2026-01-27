import yt_dlp

def get_video_qualities(video_formats):
    return sorted(set(
        f['height'] for f in video_formats
        if f.get('vcodec') != 'none' and f.get('height')
    ))


def get_audio_qualities(audio_formats):
    return sorted(set(
        f['abr'] for f in audio_formats
        if f.get('acodec') != 'none'
    ))


def extract_youtube_stream(url):
    yt_opts = {
        'quiet': True,
        'skip_download': True,
        'restrictfilenames': True
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    video_formats = [
        f for f in info['formats']
        if f.get('vcodec') != 'none'
    ]

    audio_formats = [
        f for f in info['formats']
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none'
    ]

    return {
    'title': info.get('title'),
    'qualities': get_video_qualities(video_formats),
    'video_formats': video_formats,
    'audio_formats': audio_formats
}
