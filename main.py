from pytubefix import YouTube, Playlist


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


def download_youtube_video(video_url: str, filename: str | None = None):
    # video: YouTube = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    video: YouTube = YouTube(video_url)
    filename = filename if filename else clean_str(video.title) + '.mp4'
    video.streams.get_highest_resolution().download(filename=filename)
    print_video_info(True, 'Downloaded', video.length, video_url, filename)


def download_youtube_playlist_opts(
        playlist_url: str,
        do_print: bool,
        do_download: bool,
        reverse_order: bool,
        prefix_min: str | None,  # included, eg '002-'
        prefix_max: str | None  # included, eg '004-'
):
    playlist = Playlist(playlist_url)
    ind: int = 0
    use_range: bool = True if prefix_max and prefix_min else False
    in_range: bool = not use_range
    video_urls: list[str] = [str(video_url) for video_url in playlist.video_urls]
    video_urls = reversed(video_urls) if reverse_order else video_urls
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
            download_youtube_video(video_url, filename)
        if use_range and prefix == prefix_max:
            # in_range eq False
            break


def download_youtube_playlist(playlist_url: str):
    download_youtube_playlist_opts(
        playlist_url=playlist_url,
        do_print=True,  # True-defaulted
        do_download=True,  # True-defaulted
        reverse_order=False,  # False-defaulted
        prefix_min='041-',  # None-defaulted, included, eg '002-'
        prefix_max='051-'  # None-defaulted, included, eg '004-'
    )


# Playlist - Joe Dispenza - Mind Insider
# download_youtube_playlist('https://www.youtube.com/watch?v=wLsaBmrkYMQ&list=PLMhxh4YcRFWxuB0Kqxrb47p3x_kZgEwQ3')

# Theta Billionaire Brain Wave: Activate Wealth and Success Mindset
download_youtube_video('https://www.youtube.com/watch?v=HQwYA3G5bSU&list=RDHQwYA3G5bSU&start_radio=1')
