import re

import requests
import bs4

from handlers.FileHandler import FileHandler

class TwitterHandler:
    """Handles downloading videos from Twitter posts."""

    def __init__(self):
        self.api_url = "https://twitsave.com/info?url="
        self.output_dir = "/output/twitter/"
        self.default_output_file_name = 'default_video.mp4'
        self.filehandler = FileHandler()

    def download_video(self, url, file_name) -> bytes:
        response = requests.get(url, stream=True)
        self.filehandler.write_file(self.output_dir, file_name, response.content)
        return self.filehandler.read_video_file(self.output_dir + file_name)

    def download_twitter_video(self, url):
        response = requests.get(self.api_url)
        data = bs4.BeautifulSoup(response.text, "html.parser")
        download_button = data.find_all("div", class_="origin-top-right")[0]
        quality_buttons = download_button.find_all("a")
        highest_quality_url = quality_buttons[0].get("href")  # Highest quality video url

        file_name = data.find_all("div", class_="leading-tight")[0].find_all("p", class_="m-2")[0].text  # Video file name
        file_name = re.sub(r"[^a-zA-Z0-9]+", ' ',file_name).strip() + ".mp4"  # Remove special characters from file name

        self.download_video(highest_quality_url, file_name)

    def get_file_name_from_url(self, url: str) -> str:
        return url.split("/")[-1] if url else self.default_output_file_name
