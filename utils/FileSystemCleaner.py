import os, time, logging

class FileSystemCleaner:
    def __init__(self, directory: str, max_age_seconds: int):
        self.directory = directory
        self.max_age_seconds = max_age_seconds

    def clean(self):
        path = f'/{self.directory}'
        now = time.time()

        # Remove old files
        for filename in os.listdir(path):
            file_timestamp = os.stat(os.path.join(path, filename)).st_mtime
            x_days_ago = now - self.max_age_seconds
            if file_timestamp < x_days_ago:
                # os.remove(os.path.join(path, filename))
                logging.info(f'Removed file: {os.path.join(path, filename)}')

        # Remove empty directories
        for root, dirs, files in os.walk(path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    # os.rmdir(dir_path)
                    logging.info(f'Removed empty directory: {dir_path}')