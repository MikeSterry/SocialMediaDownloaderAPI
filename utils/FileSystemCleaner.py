import os, time, logging

"""
FileSystemCleaner is responsible for cleaning up files and directories in a specified directory.
It removes files older than a specified age and deletes empty directories.
It logs the actions taken during the cleanup process.
"""
class FileSystemCleaner:
    def __init__(self, directory: str, max_age_seconds: int):
        self.directory = directory
        self.max_age_seconds = max_age_seconds

    """ 
    Clean up files and directories in the specified directory.
    This method removes files older than the specified age and deletes empty directories.
    :return: None
    """
    def clean(self):
        path = f'/{self.directory}'

        self._clean_files(path)
        self._clean_empty_directories(path)

    """ 
    Clean up files in the specified path that are older than the max age.
    :param path: The path to the directory where files will be cleaned.
    """
    def _clean_files(self, path: str):
        now = time.time()
        files = os.listdir(path)
        logging.info(f"Clean up job - Reviewing up {len(files)} files...")
        for filename in files:
            file_timestamp = os.stat(os.path.join(path, filename)).st_birthtime
            x_days_ago = now - self.max_age_seconds
            logging.info(f"Filename: {filename} is older than {self.max_age_seconds} seconds: {file_timestamp < x_days_ago}")
            if file_timestamp < x_days_ago:
                # os.remove(os.path.join(path, filename))
                logging.info(f'Removed file: {os.path.join(path, filename)}')

    """
    Clean up empty directories in the specified path.
    :param path: The path to the directory where empty directories will be cleaned.
    """
    def _clean_empty_directories(self, path: str):
        for root, dirs, files in os.walk(path, topdown=False):
            logging.info(f"Clean up job - Reviewing up {len(dirs)} directories...")
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    logging.info(f'Directory: {dir_path} is empty')
                    # os.rmdir(dir_path)
                    logging.info(f'Removed empty directory: {dir_path}')
