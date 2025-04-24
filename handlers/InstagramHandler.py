from instaloader import Instaloader, Post

from handlers.FileHandler import FileHandler


class InstagramHandler:
    def __init__(self):
        self.output_dir = "/output/instagram/"
        self.loader = Instaloader(dirname_pattern=self.output_dir + "{target}", save_metadata=False, download_video_thumbnails=False)
        self.filehandler = FileHandler()

    def download_video(self, url: str) -> bytes:
        shortcode = self._get_shortcode_from_url(url)
        post = self._download_post_from_shortcode(shortcode)
        video_file_location = self._get_post_file(post)
        video_data = self.filehandler.read_video_file(video_file_location)
        return video_data

    def _get_shortcode_from_url(self, url: str) -> str:
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

    def _download_post_from_shortcode(self, shortcode: str) -> Post:
        context = self.loader.context
        post = Post.from_shortcode(context, shortcode)
        self.loader.download_post(post, target=post.owner_username)
        return post

    def _get_post_file(self, post: Post) -> str:
        directory = f'{self.output_dir}{post.owner_username}'
        formatted_post_date = post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')
        file_extension = 'jpg'
        if post.is_video:
            file_extension = 'mp4'
        filename = f'{formatted_post_date}_UTC.{file_extension}'
        return f'{directory}/{filename}'