import os
from tqdm import tqdm

"""
FileHandler is responsible for reading and writing files.
It provides methods to read video files, write files to the output directory,
and delete files.
It also includes methods to write files with a desired file size and to delete files.
"""
class FileHandler:
    def read_video_file(self, locaiton: str) -> bytes:
        with open(locaiton, 'rb') as f:
            video_data = f.read()
            return video_data
    """
    Write a file to the specified output directory.
    :param output_dir: The directory where the file will be written.
    :param filename: The name of the file to be written.
    :param content: The content of the file as bytes.
    """
    def write_file(self, output_dir: str, filename: str, content: bytes):
        download_path = os.path.join(output_dir, filename)
        block_size = 1024
        with open(download_path, "wb") as file:
            for data in content.iter_content(block_size):
                file.write(data)

    """
    Write a file to the specified output directory with a desired file size.
    :param output_dir: The directory where the file will be written.
    :param filename: The name of the file to be written.
    :param desired_file_size: The desired size of the file in bytes.
    :param file_size_request: The request object containing the file content.
    """
    def write_file_by_desired_file_size(self, output_dir: str, filename: str, desired_file_size: int, file_size_request):
        t = tqdm(total=desired_file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
        block_size = 1024
        with open(output_dir + filename + '.mp4', 'wb') as f:
            for data in file_size_request.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()

    """
    Delete a file if it exists.
    :param filename: The name of the file to be deleted.
    :return: None
    """
    def delete_file(self, filename: str):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print(f"The file {filename} does not exist.")
