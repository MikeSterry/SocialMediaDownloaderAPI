from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from handlers.InstagramHandler import InstagramHandler
from handlers import YouTubeHandler, FacebookHandler, TwitterHandler
from utils.FileSystemCleaner import FileSystemCleaner
from utils.Constants import *

""" 
This script sets up a Flask application that provides endpoints to download videos from various social media platforms.
It includes a scheduled job to clean up resources older than 7 days from the output directory.
It uses handlers for Instagram, YouTube, Facebook, and Twitter to manage the download processes.
It also includes a file system cleaner utility to remove old files from the output directory.
"""
def clean_up_resources():
    clean_up_directory = '/output'
    max_file_age_seconds = 60 * 60 * 24 * 7  # 7 days
    logging.info("Cleaning up resources...")
    FileSystemCleaner(directory=clean_up_directory, max_age_seconds=max_file_age_seconds).clean()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(clean_up_resources, 'interval', minutes=60)
scheduler.start()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
logging.basicConfig(level=logging.INFO)

""" 
Main entry point for the Flask application.
It defines the routes for downloading content from various social media platforms.
It handles requests to download videos from Instagram, YouTube, Facebook, and Twitter.
It also includes a health check endpoint to verify the service is running.
"""
@app.route('/download', methods=['GET'])
def download_generic():
    url = request.args.get('url')
    if not url:
        logging.error('Invalid request. No url provided')
        return Response("Invalid Request. No url provided", status=400)
    logging.info(f'Received request to download content from url: {url}')

    try:
        if INSTAGRAM_DOT_COM in url:
            return _download_from_instagram(url)
        elif FACEBOOK_DOT_COM in url.lower():
            return _download_from_facebook(url)
        elif YOUTUBE_DOT_COM in url.lower():
            return _download_from_youtube(url)
        elif THREADS_DOT_COM in url.lower():
            return Response("Service does not accept Threads at this time", status=400)
        elif PINTEREST_DOT_COM in url.lower():
            return Response("Service does not accept Pinterest at this time", status=400)
        elif LINKEDIN_DOT_COM in url.lower():
            return Response("Service does not accept LinkedIn at this time", status=400)
        elif VIMEO_DOT_COM in url.lower():
            return Response("Service does not accept Vimeo at this time", status=400)
        elif X_DOT_COM in url:
            return _download_from_x(url)
        else:
            return Response("Invalid Service", status=400)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return Response("Unable to generate video output", status=500)

""" 
Endpoint to download YouTube audio from a given URL.
It accepts a URL as a query parameter and returns the audio data.
"""
@app.route('/download_youtube_audio', methods=['GET'])
def download_youtube_audio():
    url = request.args.get('url')
    if not url:
        logging.error('Invalid request. No url provided')
        return Response("Invalid Request. No url provided", status=400)
    logging.info(f'Received request to download YouTube audio from url: {url}')

    try:
        _download_from_youtube(url, audio=True)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return Response("Unable to generate video output", status=500)

"""
Endpoint to check if the service is up and running.
It returns a simple "OK" response with a 200 status code.
"""
@app.route('/up', methods=['GET'])
def up_page():
    return Response("OK", status=200)

"""
Function to handle downloading content from Instagram.
It uses the InstagramHandler to download video content from the provided URL.
:param url: The URL of the Instagram post (reel or photo).
:return: A Flask Response object containing the video data.
"""
def _download_from_instagram(url):
    logging.info(f'Downloading content from Instagram URL: {url}')
    instagram_handler = InstagramHandler()
    video_data = instagram_handler.download_video(url)
    return Response(video_data, mimetype=VIDEO_MP4)

"""
Function to handle downloading content from YouTube.
It uses the YouTubeHandler to download either video or audio content based on the provided URL.
:param url: The URL of the YouTube video.
:param audio: If True, download audio only; otherwise, download video.
:return: A Flask Response object containing the video or audio data.
"""
def _download_from_youtube(url, audio: bool = False):
    logging.info(f'Downloading content from YouTube URL: {url}')
    youtube_handler = YouTubeHandler()
    video_data = youtube_handler.download(url, audio)
    return Response(video_data, mimetype='x-matroska')

"""
Function to handle downloading content from Facebook.
It uses the FacebookHandler to download video content from the provided URL.
:param url: The URL of the Facebook video.
:return: A Flask Response object containing the video data.
"""
def _download_from_facebook(url):
    logging.info(f'Downloading content from Facebook URL: {url}')
    facebook_handler = FacebookHandler()
    video_data = facebook_handler.download_video(url)
    return Response(video_data, mimetype=VIDEO_MP4)

"""
Function to handle downloading content from X (formerly Twitter).
It uses the TwitterHandler to download video content from the provided URL.
:param url: The URL of the X post.
:return: A Flask Response object containing the video data.
"""
def _download_from_x(url):
    logging.info(f'Downloading content from X URL: {url}')
    twitter_handler = TwitterHandler()
    video_data = twitter_handler.download_twitter_video(url)
    return Response(video_data, mimetype=VIDEO_MP4)

""" 
Main entry point for the Flask application.
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
