import os
from tqdm import tqdm

class FileHandler:
    def read_video_file(self, locaiton: str) -> bytes:
        with open(locaiton, 'rb') as f:
            video_data = f.read()
            return video_data

    def write_file(self, output_dir: str, filename: str, content: bytes):
        download_path = os.path.join(output_dir, filename)
        block_size = 1024
        with open(download_path, "wb") as file:
            for data in content.iter_content(block_size):
                file.write(data)

    def write_file_by_desired_file_size(self, output_dir: str, filename: str, desired_file_size: int, file_size_request):
        t = tqdm(total=desired_file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
        block_size = 1024
        with open(output_dir + filename + '.mp4', 'wb') as f:
            for data in file_size_request.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()