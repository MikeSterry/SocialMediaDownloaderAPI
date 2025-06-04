from typing import Optional

import yt_dlp, logging, os

from handlers.FileHandler import FileHandler


class YouTubeHandler:
    def __init__(self):
        # self.output_dir = "/output/youtube/"
        output_dir = "/Users/mike/downloads/youtube/"
        video_filename_processor = output_dir.rstrip('/') + '/' + '%(title)s'
        audio_filename_processor = output_dir.rstrip('/') + '/' + '%(title)s'
        self.video_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': video_filename_processor,
            'progress_hooks': [self._yt_dlp_monitor],
            'quiet': True,
            'noplaylist': True,
            'getfilename': True,
        }
        self.audio_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                },
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0',
                }
            ],
            'quiet': True,
            # 'verbose': True,
            'noplaylist': True,
            'getfilename': True,
            'outtmpl': audio_filename_processor,
        }
        self.yt_dlp = yt_dlp

    def download(self, url, audio: Optional[bool] = False) -> bytes:
        file_path = None
        if audio:
            file_path = self._download_audio(url)
        else:
            file_path = self._download_video(url)

        if not file_path:
            raise ValueError("YouTube download failed. No file path returned.")

        logging.info(f"YouTube download successful. File path: {file_path}")
        return FileHandler().read_video_file(file_path)

    def _download_video(self, url) -> str:
        with self.yt_dlp.YoutubeDL(self.video_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            file_path = ydl.prepare_filename(info_dict) + '.mp4'
            return file_path


    def _download_audio(self, url):
        with self.yt_dlp.YoutubeDL(self.audio_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            file_path = ydl.prepare_filename(info_dict) + '.mp3'
            return file_path

    def _yt_dlp_monitor(self, d):
        final_filename = d.get('info_dict').get('_filename')