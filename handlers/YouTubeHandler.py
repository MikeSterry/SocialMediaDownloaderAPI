from typing import Optional

import ffmpeg
from pytubefix import YouTube
from pytubefix.cli import on_progress

from handlers.FileHandler import FileHandler


class YouTubeHandler:
    def __init__(self, url: str):
        self.output_dir = "/output/youtube/"
        self.yt = YouTube(url, on_progress_callback=on_progress)
        self.filehandler = FileHandler()

    def download_youtube(self) -> Optional[bytes]:
        video = self.yt.streams.filter(resolution='1080p').first()
        audio = self.yt.streams.filter(only_audio=True).first()
        video_filename = None
        audio_filename = None
        output_filename = None
        if video and audio:
            video_filename = self._download_mp4_video(video)
            audio_filename = self._download_mp4_audio(audio)
            output_filename = self._merge_video_audio()
        elif video and not audio:
            output_filename = self._download_mp4_video(video)
        elif audio and not video:
            output_filename = self._download_mp4_audio(audio)
        else:
            raise ValueError("No suitable video or audio streams found.")

        if video_filename:
            self.filehandler.delete_file(video_filename)
        if audio_filename:
            self.filehandler.delete_file(audio_filename)

        if output_filename:
            return self.filehandler.read_video_file(output_filename)

        return None

    def _download_mp4_video(self, video=None) -> str:
        print('Downloading Video...')
        filename = f'{self.output_dir}/{self.yt.title}_video.mp4'
        video.download(filename=filename)
        return filename

    def _download_mp4_audio(self, audio=None) -> str:
        print('Downloading Audio...')
        filename = f'{self.output_dir}/{self.yt.title}_audio.mp4'
        audio.download(filename=filename)
        return filename

    def _merge_video_audio(self, video_filename=None, audio_filename=None) -> str:
        output_file = f'{self.output_dir}/{self.yt.title}.mp4'

        print('Merging Video and Audio...')
        ffmpeg.input(video_filename).output(audio_filename, output_file).run()

        return output_file