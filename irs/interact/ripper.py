import os
import sys
import glob
import shutil

import youtube_dl


def rip_from_url(video_url, output_name):
    """This method downloads a video, converts it to an MP3 and renames it
    :param video_url: a string, youtube url of the video you want to download
    :param output_name: a string, the name of the output file
    """

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': _DownloadLogger(),
        'progress_hooks': [_download_hook],
        'output': "tmp_file",
        'prefer-ffmpeg': True,
        'ffmpeg_location': os.environ["irs_ffmpeg_dir"],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    for f in glob.glob("./*%s*" % video_url.split("/watch?v=")[-1]):
        shutil.move(f, output_name)


class _DownloadLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# TODO: update the download log
def _download_hook(d):
    if d['status'] == 'finished':
        print("Done!")