from typing import Optional

import yt_dlp, logging

from handlers.FileHandler import FileHandler

"""
YouTubeHandler is responsible for downloading videos and audio from YouTube using yt-dlp.
It provides methods to download either video or audio based on the provided URL.
It returns the video or audio data as bytes.
"""
class YouTubeHandler:
    def __init__(self):
        output_dir = "/output/youtube/"
        video_filename_processor = self._get_filename_processor(output_dir)
        audio_filename_processor = self._get_filename_processor(output_dir)
        self.video_opts = self._get_video_options(video_filename_processor)
        self.audio_opts = self._get_audio_options(audio_filename_processor)
        self.yt_dlp = yt_dlp

    """
    Download a video or audio from YouTube using the provided URL.
    :param url: The URL of the YouTube video.
    :param audio: If True, download audio only; otherwise, download video.
    :return: The video or audio data as bytes.
    """
    def download(self, url, audio: Optional[bool] = False) -> bytes:
        try:
            file_path = None
            if audio:
                file_path = self._download_audio(url)
            else:
                file_path = self._download_video(url)

            if not file_path:
                raise ValueError("YouTube download failed. No file path returned.")

            logging.info(f"YouTube download successful. File path: {file_path}")
            return FileHandler().read_video_file(file_path)
        except Exception as e:
            logging.error(f"Error downloading from YouTube: {e}")
            raise ValueError("YouTube download failed. Check logs for details.")

    """ 
    Download a video from YouTube using the provided URL.
    :param url: The URL of the YouTube video.
    :return: The file path of the downloaded video.
    """
    def _download_video(self, url) -> str:
        try:
            with self.yt_dlp.YoutubeDL(self.video_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                # ydl.download([url])
                file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp4').replace('.temp', '.mp4')
                return file_path
        except Exception as e:
            logging.error(f"Error downloading video from YouTube: {e}")
            raise ValueError("YouTube video download failed. Check logs for details.")

    """ 
    Download audio from YouTube using the provided URL.
    :param url: The URL of the YouTube video.
    :return: The file path of the downloaded audio.
    """
    def _download_audio(self, url):
        try:
            with self.yt_dlp.YoutubeDL(self.audio_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                # ydl.download([url])
                # strip extension name from file path
                # and replace with .mp3
                file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.temp', '.mp3')
                return file_path
        except Exception as e:
            logging.error(f"Error downloading audio from YouTube: {e}")
            raise ValueError("YouTube audio download failed. Check logs for details.")

    """
    Get the filename processor for the output directory.
    :param output_dir: The directory where the downloaded files will be saved.
    :return: The filename processor string.
    """
    def _get_filename_processor(self, output_dir: str) -> str:
        try:
            return output_dir.rstrip('/') + '/' + '%(title)s.%(ext)s'
        except Exception as e:
            logging.error(f"Error setting filename processor: {e}")
            raise ValueError("Error setting filename processor. Check logs for details.")

    """
    Get the audio options for yt-dlp.
    :param audio_filename_processor: The filename processor for audio files.
    :return: A dictionary of options for yt-dlp audio download.
    """
    def _get_audio_options(self, audio_filename_processor) -> dict:
        try:
            return {
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
        except Exception as e:
            logging.error(f"Error setting audio options: {e}")
            raise ValueError("Error setting audio options. Check logs for details.")

    """
    Get the video options for yt-dlp.
    :param video_filename_processor: The filename processor for video files.
    :return: A dictionary of options for yt-dlp video download.
    """
    def _get_video_options(self, video_filename_processor) -> dict:
        try:
            return {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': video_filename_processor,
                'progress_hooks': [self._yt_dlp_monitor],
                'quiet': True,
                'noplaylist': True,
                'getfilename': True,
            }
        except Exception as e:
            logging.error(f"Error setting video options: {e}")
            raise ValueError("Error setting video options. Check logs for details.")

    """ Monitor function for yt-dlp to log download progress.
    :param d: The dictionary containing download information.
    """
    def _yt_dlp_monitor(self, d):
        try:
            final_filename = d.get('info_dict').get('_filename')
        except Exception as e:
            logging.error(f"Error in yt-dlp monitor: {e}")
            raise ValueError("Error in yt-dlp monitor. Check logs for details.")
