from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler

from utils.Constants import *
from utils.FileSystemCleaner import FileSystemCleaner
import logging, os

from handlers.InstagramHandler import InstagramHandler

# Run this script to start the Flask app and schedule the cleanup job
# Remove any downloaded resources older than 7 days every hour
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


@app.route('/download', methods=['GET'])
def download_generic():
    url = request.args.get('url')
    logging.info(f'Received request to download content from url: {url}')
    if not url:
        logging.error('Invalid request. No url provided')
        return Response("Invalid Request. No url provided", status=400)

    if INSTAGRAM_DOT_COM in url:
        return download_from_instagram(url)
    elif FACEBOOK_DOT_COM in url.lower():
        return Response("Service does not accept Facebook at this time", status=400)
    elif YOUTUBE_DOT_COM in url.lower():
        return Response("Service does not accept YouTube at this time", status=400)
    elif THREADS_DOT_COM in url.lower():
        return Response("Service does not accept Threads at this time", status=400)
    elif PINTEREST_DOT_COM in url.lower():
        return Response("Service does not accept Pinterest at this time", status=400)
    elif LINKEDIN_DOT_COM in url.lower():
        return Response("Service does not accept LinkedIn at this time", status=400)
    elif VIMEO_DOT_COM in url.lower():
        return Response("Service does not accept Vimeo at this time", status=400)
    elif X_DOT_COM in url:
        return download_from_x(url)
    else:
        return Response("Invalid Service", status=400)

@app.route('/instagram', methods=['GET'])
def download_instagram():
    url = request.args.get('url')
    return download_from_instagram(url)

def download_from_instagram(url):
    logging.info(f'Downloading content from Instagram URL: {url}')
    instagram_handler = InstagramHandler()
    video_data = instagram_handler.download_video(url)
    return Response(video_data, mimetype='video/mp4')

def download_from_x(url):
    logging.info(f'Downloading content from X URL: {url}')
    logging.info('No plans to accept X/Twitter posts - returning x default response')
    cwd = os.getcwd()
    x_default_pic = cwd + '/static/x_default_pic.jpeg'
    return Response(x_default_pic, mimetype='image/jpg')

@app.route('/up', methods=['GET'])
def up_page():
    return Response("OK", status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
