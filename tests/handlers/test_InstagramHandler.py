import unittest
from unittest.mock import patch, MagicMock
from handlers.InstagramHandler import InstagramHandler


class TestInstagramHandler(unittest.TestCase):
    def setUp(self):
        self.handler = InstagramHandler()

    @patch('handlers.InstagramHandler.FileHandler.read_video_file')
    @patch('handlers.InstagramHandler.Instaloader.download_post')
    @patch('handlers.InstagramHandler.Post.from_shortcode')
    def test_download_video(self, mock_from_shortcode, mock_download_post, mock_read_video_file):
        mock_post = MagicMock()
        mock_post.owner_username = "test_user"
        mock_post.date_utc.strftime.return_value = "2023-10-01_12-00-00"
        mock_post.is_video = True
        mock_from_shortcode.return_value = mock_post
        mock_read_video_file.return_value = b"video_data"

        url = "https://www.instagram.com/reel/test_shortcode/"
        result = self.handler.download_video(url)

        self.assertEqual(result, b"video_data")
        mock_from_shortcode.assert_called_once_with(self.handler.loader.context, "test_shortcode")
        mock_download_post.assert_called_once_with(mock_post, target="test_user")
        mock_read_video_file.assert_called_once()

    def test_get_shortcode_from_url_valid_reel(self):
        url = "https://www.instagram.com/reel/test_shortcode/"
        result = self.handler._get_shortcode_from_url(url)
        self.assertEqual(result, "test_shortcode")

    def test_get_shortcode_from_url_valid_post(self):
        url = "https://www.instagram.com/p/test_shortcode/"
        result = self.handler._get_shortcode_from_url(url)
        self.assertEqual(result, "test_shortcode")

    def test_get_shortcode_from_url_invalid_url(self):
        url = "https://www.example.com/invalid_url/"
        with self.assertRaises(ValueError):
            self.handler._get_shortcode_from_url(url)

    # @patch('handlers.InstagramHandler.Instaloader.context')
    # @patch('handlers.InstagramHandler.Post.from_shortcode')
    # def test_download_post_from_shortcode(self, mock_from_shortcode, mock_context):
    #     mock_post = MagicMock()
    #     mock_from_shortcode.return_value = mock_post
    #
    #     result = self.handler._download_post_from_shortcode("test_shortcode")
    #     self.assertEqual(result, mock_post)
    #     mock_from_shortcode.assert_called_once_with(mock_context, "test_shortcode")

    def test_get_post_file_video(self):
        mock_post = MagicMock()
        mock_post.owner_username = "test_user"
        mock_post.date_utc.strftime.return_value = "2023-10-01_12-00-00"
        mock_post.is_video = True

        result = self.handler._get_post_file(mock_post)
        expected_path = "/output/instagram/test_user/2023-10-01_12-00-00_UTC.mp4"
        self.assertEqual(result, expected_path)

    def test_get_post_file_photo(self):
        mock_post = MagicMock()
        mock_post.owner_username = "test_user"
        mock_post.date_utc.strftime.return_value = "2023-10-01_12-00-00"
        mock_post.is_video = False

        result = self.handler._get_post_file(mock_post)
        expected_path = "/output/instagram/test_user/2023-10-01_12-00-00_UTC.jpg"
        self.assertEqual(result, expected_path)


if __name__ == "__main__":
    unittest.main()
