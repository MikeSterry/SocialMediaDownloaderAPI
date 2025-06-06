import unittest
from unittest.mock import patch, mock_open
from handlers.FileHandler import FileHandler


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()

    @patch('builtins.open', new_callable=mock_open, read_data=b"video_data")
    def test_read_video_file(self, mock_open_file):
        file_path = "/path/to/video.mp4"
        result = self.file_handler.read_video_file(file_path)
        self.assertEqual(result, b"video_data")
        mock_open_file.assert_called_once_with(file_path, 'rb')

    # @patch('builtins.open', new_callable=mock_open)
    # def test_write_file(self, mock_open_file):
    #     file_path = "/path/to/output.txt"
    #     data = b"file_content"
    #     self.file_handler.write_file(file_path, data)
    #     mock_open_file.assert_called_once_with(file_path, 'wb')
    #     mock_open_file().write.assert_called_once_with(data)

    # @patch('builtins.open', new_callable=mock_open)
    # def test_write_file_by_desired_file_size(self, mock_open_file):
    #     file_path = "/path/to/output.txt"
    #     data = b"file_content"
    #     desired_size = 5
    #     self.file_handler.write_file_by_desired_file_size(file_path, data, desired_size)
    #     mock_open_file.assert_called_once_with(file_path, 'wb')
    #     mock_open_file().write.assert_called_once_with(data[:desired_size])

    # @patch('os.remove')
    # def test_delete_file(self, mock_remove):
    #     file_path = "/path/to/delete.txt"
    #     self.file_handler.delete_file(file_path)
    #     mock_remove.assert_called_once_with(file_path)


if __name__ == "__main__":
    unittest.main()
