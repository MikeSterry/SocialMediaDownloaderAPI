import unittest
from unittest.mock import patch, MagicMock
from app import app, _download_from_instagram, _download_from_youtube, _download_from_facebook, _download_from_x

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app._download_from_youtube')
    def test_download_youtube_audio_valid_url(self, mock_download_from_youtube):
        mock_download_from_youtube.return_value = MagicMock(status=200, data=b"audio_data")
        response = self.client.get('/download_youtube_audio?url=https://www.youtube.com/watch?v=test_audio')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"audio_data")
        mock_download_from_youtube.assert_called_once_with('https://www.youtube.com/watch?v=test_audio', audio=True)

    def test_download_youtube_audio_invalid_url(self):
        response = self.client.get('/download_youtube_audio')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid Request. No url provided", response.data)

    def test_up_page(self):
        response = self.client.get('/up')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"OK")

    @patch('app.InstagramHandler')
    def test_download_from_instagram(self, mock_instagram_handler):
        mock_handler_instance = mock_instagram_handler.return_value
        mock_handler_instance.download_video.return_value = b"video_data"
        response = _download_from_instagram("https://www.instagram.com/reel/test_shortcode/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"video_data")
        mock_instagram_handler.assert_called_once()

    @patch('app.YouTubeHandler')
    def test_download_from_youtube(self, mock_youtube_handler):
        mock_handler_instance = mock_youtube_handler.return_value
        mock_handler_instance.download.return_value = b"video_data"
        response = _download_from_youtube("https://www.youtube.com/watch?v=test_video", audio=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"video_data")
        mock_youtube_handler.assert_called_once()

    @patch('app.FacebookHandler')
    def test_download_from_facebook(self, mock_facebook_handler):
        mock_handler_instance = mock_facebook_handler.return_value
        mock_handler_instance.download_video.return_value = b"video_data"
        response = _download_from_facebook("https://www.facebook.com/video/test_video")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"video_data")
        mock_facebook_handler.assert_called_once()

    @patch('app.TwitterHandler')
    def test_download_from_x(self, mock_twitter_handler):
        mock_handler_instance = mock_twitter_handler.return_value
        mock_handler_instance.download_twitter_video.return_value = b"video_data"
        response = _download_from_x("https://twitter.com/test_video")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"video_data")
        mock_twitter_handler.assert_called_once()


if __name__ == "__main__":
    unittest.main()
