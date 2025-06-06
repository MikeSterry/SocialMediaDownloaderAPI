# Social Media Downloader API

A simple API to download media from various social media platforms.

## Features
- Download media from Instagram

## Usage
- Clone the repository
- Create docker image
- Run docker-compose up
- Access the API at `http://localhost:8000`

## Run locally
- Clone the repository
- Install ffmpeg binaries
- Build the python virtual environment
    - python -m venv .venv
    - source .venv/bin/activate
    - .venv/bin/pip install -r requirements.txt
- run python app.py

## Extra
- Put the API behind a reverse proxy like Nginx or Traefik
- Use a custom domain
- Build a custom iOS shortcut to call the API
- Put the iOS shortcut on the "share sheet" so you can send media to the API directly from the social media app
