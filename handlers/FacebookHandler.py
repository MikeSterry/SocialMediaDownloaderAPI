import logging
import re
import requests
from datetime import datetime
from handlers.FileHandler import FileHandler

class FacebookHandler:
    def __init__(self):
        self.filehandler = FileHandler()
        self.output_dir = "/output/facebook/"

    def download_video(self, url: str) -> bytes:
        html = requests.get(url).content.decode('utf-8')

        _qualityhd = re.search('hd_src:"https', html)
        _qualitysd = re.search('sd_src:"https', html)
        _hd = re.search('hd_src:null', html)
        _sd = re.search('sd_src:null', html)

        list = []
        _thelist = [_qualityhd, _qualitysd, _hd, _sd]
        for id, val in enumerate(_thelist):
            if val != None:
                list.append(id)

        print(f'html: {html}')
        if len(list) == 0:
            logging.error("No video found in the provided URL.")
            raise ValueError("No video found in the provided URL.")

        try:
            return self.download_video_by_quality('HD', html)
        except Exception as e:
            return self.download_video_by_quality('SD', html)

    def download_video_by_quality(self, quality, html):
        print(f"\nDownloading the video in {quality} quality... \n")
        video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
        file_size_request = requests.get(video_url, stream=True)
        file_size = int(file_size_request.headers['Content-Length'])
        filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        self.filehandler.write_file_by_desired_file_size(self.output_dir, filename, file_size, file_size_request)
        return self.filehandler.read_video_file(self.output_dir + filename + '.mp4')
