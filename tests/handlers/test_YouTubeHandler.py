import unittest
from unittest.mock import patch
from handlers.YouTubeHandler import YouTubeHandler


class TestYouTubeHandler(unittest.TestCase):
    def setUp(self):
        self.handler = YouTubeHandler()

    @patch('handlers.YouTubeHandler.yt_dlp.YoutubeDL')
    def test_download_video(self, mock_youtube_dl):
        mock_instance = mock_youtube_dl.return_value
        mock_instance.download.return_value = None

        url = "https://www.youtube.com/watch?v=test_video"
        result = self.handler.download(url, audio=False)

        self.assertIsNone(result)
        mock_youtube_dl.assert_called_once()

    @patch('handlers.YouTubeHandler.yt_dlp.YoutubeDL')
    def test_download_audio(self, mock_youtube_dl):
        mock_instance = mock_youtube_dl.return_value
        mock_instance.download.return_value = None

        url = "https://www.youtube.com/watch?v=test_audio"
        result = self.handler.download(url, audio=True)

        self.assertIsNone(result)
        mock_youtube_dl.assert_called_once()

    def test_get_filename_processor(self):
        processor = self.handler._get_filename_processor()
        self.assertIsInstance(processor, str)

    def test_get_audio_options(self):
        options = self.handler._get_audio_options()
        self.assertIn('format', options)
        self.assertEqual(options['format'], 'bestaudio')

    def test_get_video_options(self):
        options = self.handler._get_video_options()
        self.assertIn('format', options)
        self.assertEqual(options['format'], 'bestvideo+bestaudio')

    @patch('handlers.YouTubeHandler.logging.error')
    def test_yt_dlp_monitor_error(self, mock_logging_error):
        monitor_data = {'info_dict': {}}
        with self.assertRaises(ValueError):
            self.handler._yt_dlp_monitor(monitor_data)
        mock_logging_error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
