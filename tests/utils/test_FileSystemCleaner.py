import unittest
from utils.FileSystemCleaner import FileSystemCleaner


class TestFileSystemCleaner(unittest.TestCase):
    def setUp(self):
        self.cleaner = FileSystemCleaner(directory="/test/directory", max_age_seconds=60 * 60 * 24 * 7)

    # @patch('os.path.getmtime')
    # @patch('os.remove')
    # @patch('os.listdir')
    # def test_clean_removes_old_files(self, mock_listdir, mock_remove, mock_getmtime):
    #     mock_listdir.return_value = ["file1.txt", "file2.txt"]
    #     current_time = time.time()
    #     mock_getmtime.side_effect = [current_time - (60 * 60 * 24 * 8), current_time - (60 * 60 * 24 * 6)]
    #
    #     self.cleaner.clean()
    #
    #     mock_listdir.assert_called_once_with("/test/directory")
    #     mock_getmtime.assert_any_call("/test/directory/file1.txt")
    #     mock_getmtime.assert_any_call("/test/directory/file2.txt")
    #     mock_remove.assert_called_once_with("/test/directory/file1.txt")

    # @patch('os.path.getmtime')
    # @patch('os.remove')
    # @patch('os.listdir')
    # def test_clean_does_not_remove_recent_files(self, mock_listdir, mock_remove, mock_getmtime):
    #     mock_listdir.return_value = ["file1.txt", "file2.txt"]
    #     current_time = time.time()
    #     mock_getmtime.side_effect = [current_time - (60 * 60 * 24 * 6), current_time - (60 * 60 * 24 * 5)]
    #
    #     self.cleaner.clean()
    #
    #     mock_listdir.assert_called_once_with("/test/directory")
    #     mock_getmtime.assert_any_call("/test/directory/file1.txt")
    #     mock_getmtime.assert_any_call("/test/directory/file2.txt")
    #     mock_remove.assert_not_called()

    # @patch('os.path.getmtime')
    # @patch('os.remove')
    # @patch('os.listdir')
    # def test_clean_handles_empty_directory(self, mock_listdir, mock_remove, mock_getmtime):
    #     mock_listdir.return_value = []
    #
    #     self.cleaner.clean()
    #
    #     mock_listdir.assert_called_once_with("/test/directory")
    #     mock_getmtime.assert_not_called()
    #     mock_remove.assert_not_called()


if __name__ == "__main__":
    unittest.main()
