from instaloader import Instaloader, Post
import logging

from handlers.FileHandler import FileHandler

"""
InstagramHandler is responsible for downloading videos from Instagram using Instaloader.
It provides methods to download videos from Instagram posts (reels or photos) using their URLs.
It returns a filename processor that formats the output file names.
"""
class InstagramHandler:
    def __init__(self):
        self.output_dir = "/output/instagram/"
        self.loader = Instaloader(dirname_pattern=self.output_dir + "{target}", save_metadata=False, download_video_thumbnails=False)
        self.filehandler = FileHandler()

    """
    Download a video from Instagram using the provided URL.
    :param url: The URL of the Instagram post (reel or photo).
    :return: The video data as bytes.
    """
    def download_video(self, url: str) -> bytes:
        try:
            shortcode = self._get_shortcode_from_url(url)
            post = self._download_post_from_shortcode(shortcode)
            video_file_location = self._get_post_file(post)
            video_data = self.filehandler.read_video_file(video_file_location)
            return video_data
        except Exception as e:
            logging.error(f"Error downloading from Instagram: {e}")
            raise ValueError(f"Failed to download video: {e}")

    """
    Extract the shortcode from the Instagram post URL.
    :param url: The URL of the Instagram post.
    :return: The shortcode extracted from the URL.
    """
    def _get_shortcode_from_url(self, url: str) -> str:
        try:
            if 'instagram.com' not in url:
                raise ValueError("Invalid Instagram URL")
            parts = url.split('/')
            # Extract the shortcode from the URL
            if 'reel' in parts:
                return parts[parts.index('reel') + 1].split('?')[0]
            elif 'p' in parts:
                return parts[parts.index('p') + 1].split('?')[0]
            else:
                raise ValueError("Shortcode not found in URL")
        except Exception as e:
            logging.error(f"Error extracting shortcode from URL: {e}")
            raise ValueError("Failed to extract shortcode from URL")

    """
    Download the Instagram post using the shortcode.
    :param shortcode: The shortcode of the Instagram post.
    :return: The Post object representing the downloaded post.
    """
    def _download_post_from_shortcode(self, shortcode: str) -> Post:
        try:
            context = self.loader.context
            post = Post.from_shortcode(context, shortcode)
            self.loader.download_post(post, target=post.owner_username)
            return post
        except Exception as e:
            logging.error(f"Error downloading post from shortcode: {e}")
            raise ValueError("Failed to download post from shortcode")

    """
    Get the file path for the downloaded post.
    :param post: The Post object representing the downloaded post.
    :return: The file path where the post is saved.
    """
    def _get_post_file(self, post: Post) -> str:
        try:
            directory = f'{self.output_dir}{post.owner_username}'
            formatted_post_date = post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')
            file_extension = 'jpg'
            if post.is_video:
                file_extension = 'mp4'
            filename = f'{formatted_post_date}_UTC.{file_extension}'
            return f'{directory}/{filename}'
        except Exception as e:
            logging.error(f"Error getting post file: {e}")
            raise ValueError("Failed to get post file")
