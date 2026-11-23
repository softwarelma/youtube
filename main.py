from pytubefix import YouTube, Playlist
from yt_dlp import YoutubeDL


# 1. if not working: pip install --upgrade pytubefix
# 2. still not working? add or remove oauth on download_youtube_video
# 3. still nothing? try
# import os
# os.system(f'yt-dlp "{url}"')


def clean_str(s: str) -> str:
    return ''.join(c for c in s if c.isalnum() or c.isspace())


def print_video_info(do_print: bool, print_prefix: str, video_len: int, video_url: str, filename: str):
    if do_print:
        minutes = video_len // 60
        hours = minutes // 60
        minutes = minutes % 60
        seconds = video_len % 60
        print(f'{print_prefix} "{filename}" - {video_url} - {hours}h {minutes}m {seconds}s')


def download_youtube_video(video_url: str, do_auth: bool, filename: str | None = None):
    video: YouTube = YouTube(video_url, use_oauth=do_auth, allow_oauth_cache=do_auth)
    filename = filename if filename else clean_str(video.title) + '.mp4'
    video.streams.get_highest_resolution().download(filename=filename)
    print_video_info(True, 'Downloaded', video.length, video_url, filename)


def download_youtube_urllist_opts(
        video_urls: list[str],
        do_print: bool,
        do_auth: bool,
        do_download: bool,
        reverse_order: bool,
        prefix_min: str | None,  # included, eg '002-'
        prefix_max: str | None  # included, eg '004-'
):
    video_urls = reversed(video_urls) if reverse_order else video_urls
    ind: int = 0
    use_range: bool = True if prefix_max and prefix_min else False
    in_range: bool = not use_range
    for video_url in video_urls:
        video: YouTube = YouTube(video_url)
        prefix = str(ind + 1) + '-'
        ind += 1
        prefix = prefix.rjust(4, '0')
        if use_range and prefix == prefix_min:
            in_range = True
        if not in_range:
            continue
        filename: str = prefix + clean_str(video.title) + '.mp4'
        print_video_info(do_print, 'Found', video.length, video_url, filename)
        if do_download and in_range:
            download_youtube_video(video_url, do_auth, filename)
        if use_range and prefix == prefix_max:
            # in_range eq False
            break


def download_youtube_channel_opts(
        channel_url: str,
        do_print: bool,
        do_auth: bool,
        do_download: bool,
        reverse_order: bool,
        prefix_min: str | None,  # included, eg '002-'
        prefix_max: str | None  # included, eg '004-'
):
    opts = {
        "extract_flat": True,  # only metadata, don't download
        "quiet": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    video_urls: list[str] = ['https://www.youtube.com/watch?v=' + video["id"] for video in info["entries"]]
    download_youtube_urllist_opts(
        video_urls,
        do_print,
        do_auth,
        do_download,
        reverse_order,
        prefix_min,
        prefix_max
    )


def download_youtube_playlist_opts(
        playlist_url: str,
        do_print: bool,
        do_auth: bool,
        do_download: bool,
        reverse_order: bool,
        prefix_min: str | None,  # included, eg '002-'
        prefix_max: str | None  # included, eg '004-'
):
    playlist = Playlist(playlist_url)
    video_urls: list[str] = [str(video_url) for video_url in playlist.video_urls]
    download_youtube_urllist_opts(
        video_urls,
        do_print,
        do_auth,
        do_download,
        reverse_order,
        prefix_min,
        prefix_max
    )


def download_youtube_playlist(playlist_url: str, do_auth: bool):
    download_youtube_playlist_opts(
        playlist_url=playlist_url,
        do_print=True,  # True-defaulted
        do_auth=do_auth,  # False-defaulted
        do_download=False,  # True-defaulted
        reverse_order=False,  # False-defaulted
        prefix_min=None,  # None-defaulted, included, eg '002-'
        prefix_max=None  # None-defaulted, included, eg '004-'
    )


def download_youtube_channel(channel_url: str, do_auth: bool):
    download_youtube_channel_opts(
        channel_url=channel_url,
        do_print=True,  # True-defaulted
        do_auth=do_auth,  # False-defaulted
        do_download=True,  # True-defaulted
        reverse_order=True,  # False-defaulted
        prefix_min='051-',  # None-defaulted, included, eg '002-'
        prefix_max='100-'  # None-defaulted, included, eg '004-'
    )


# Dark Gnostic channel
# download_youtube_channel('https://www.youtube.com/@DarkGnostic-h6c/videos', False)

# Dark Gnostic
# download_youtube_playlist('https://www.youtube.com/watch?v=ws2e9kmfzzw&list=PLGhiyR9qzFdTi-iYxv2hOMm-JiSrSxTfV', False)

# Bashar Explains The Vibration Shift Unlocking New Dimensions For Total Freedom | Bashar Channeling
download_youtube_video('https://www.youtube.com/watch?v=sKHkx8VqWAw', False)
