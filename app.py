import os
from flask import Flask, render_template, request, send_file, Response, stream_with_context
import requests
import config
import re # Import regex module
from googleapiclient.discovery import build
import yt_dlp # Import yt-dlp

app = Flask(__name__)

JAMENDO_API_KEY = config.JAMENDO_API_KEY
YOUTUBE_API_KEY = config.youtube

youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to generate SoundCloud embed URL
def get_soundcloud_embed_url(track_url):
    # Basic check for SoundCloud track URL format
    if "soundcloud.com/" in track_url and "/sets/" not in track_url:
        # SoundCloud embed widget URL format
        # This is a simplified approach. A more robust solution would use SoundCloud's oEmbed API.
        return f"https://w.soundcloud.com/player/?url={track_url}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    jamendo_tracks = []
    soundcloud_embeds = []
    youtube_videos = []

    if query:
        # Check if the query is a SoundCloud URL
        soundcloud_url_match = re.match(r'https?://(?:www\.)?soundcloud\.com/[\w-]+/[\w-]+/?', query)
        if soundcloud_url_match:
            embed_url = get_soundcloud_embed_url(query)
            if embed_url:
                soundcloud_embeds.append({"url": query, "embed_src": embed_url})
        else:
            # Perform Jamendo API search
            try:
                response = requests.get(
                    f"https://api.jamendo.com/v3.0/tracks/",
                    params={
                        "client_id": JAMENDO_API_KEY,
                        "search": query,
                        "limit": 20,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                data = response.json()
                if data and data.get('results'):
                    jamendo_tracks = data['results']
            except requests.exceptions.RequestException as e:
                print(f"Error fetching from Jamendo API: {e}")
                jamendo_tracks = []

            # Perform YouTube API search
            try:
                yt_response = youtube_service.search().list(
                    q=query,
                    part='snippet',
                    type='video',
                    maxResults=10
                ).execute()
                
                for item in yt_response.get('items', []):
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    thumbnail = item['snippet']['thumbnails']['high']['url']
                    
                    # Fetch content details for duration and statistics for view count
                    video_details_response = youtube_service.videos().list(
                        id=video_id,
                        part='contentDetails,statistics'
                    ).execute()
                    
                    duration = None
                    view_count = None
                    if video_details_response.get('items'):
                        details = video_details_response['items'][0]
                        if 'contentDetails' in details and 'duration' in details['contentDetails']:
                            duration = details['contentDetails']['duration']
                        if 'statistics' in details and 'viewCount' in details['statistics']:
                            view_count = details['statistics']['viewCount']

                    youtube_videos.append({
                        "id": video_id,
                        "title": title,
                        "description": description,
                        "thumbnail": thumbnail,
                        "duration": duration,
                        "view_count": view_count
                    })
            except Exception as e:
                print(f"Error fetching from YouTube API: {e}")
                youtube_videos = []

    return render_template('search_results.html', query=query, jamendo_tracks=jamendo_tracks, soundcloud_embeds=soundcloud_embeds, youtube_videos=youtube_videos)

import os
from flask import Flask, render_template, request, send_file, Response, stream_with_context
import requests
import config
import re # Import regex module
from googleapiclient.discovery import build
import yt_dlp # Import yt-dlp

app = Flask(__name__)

JAMENDO_API_KEY = config.JAMENDO_API_KEY
YOUTUBE_API_KEY = config.youtube

youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to generate SoundCloud embed URL
def get_soundcloud_embed_url(track_url):
    # Basic check for SoundCloud track URL format
    if "soundcloud.com/" in track_url and "/sets/" not in track_url:
        # SoundCloud embed widget URL format
        # This is a simplified approach. A more robust solution would use SoundCloud's oEmbed API.
        return f"https://w.soundcloud.com/player/?url={track_url}&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    jamendo_tracks = []
    soundcloud_embeds = []
    youtube_videos = []

    if query:
        # Check if the query is a SoundCloud URL
        soundcloud_url_match = re.match(r'https?://(?:www\.)?soundcloud\.com/[\w-]+/[\w-]+/?', query)
        if soundcloud_url_match:
            embed_url = get_soundcloud_embed_url(query)
            if embed_url:
                soundcloud_embeds.append({"url": query, "embed_src": embed_url})
        else:
            # Perform Jamendo API search
            try:
                response = requests.get(
                    f"https://api.jamendo.com/v3.0/tracks/",
                    params={
                        "client_id": JAMENDO_API_KEY,
                        "search": query,
                        "limit": 20,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                data = response.json()
                if data and data.get('results'):
                    jamendo_tracks = data['results']
            except requests.exceptions.RequestException as e:
                print(f"Error fetching from Jamendo API: {e}")
                jamendo_tracks = []

            # Perform YouTube API search
            try:
                yt_response = youtube_service.search().list(
                    q=query,
                    part='snippet',
                    type='video',
                    maxResults=10
                ).execute()
                
                for item in yt_response.get('items', []):
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    thumbnail = item['snippet']['thumbnails']['high']['url']
                    
                    # Fetch content details for duration and statistics for view count
                    video_details_response = youtube_service.videos().list(
                        id=video_id,
                        part='contentDetails,statistics'
                    ).execute()
                    
                    duration = None
                    view_count = None
                    if video_details_response.get('items'):
                        details = video_details_response['items'][0]
                        if 'contentDetails' in details and 'duration' in details['contentDetails']:
                            duration = details['contentDetails']['duration']
                        if 'statistics' in details and 'viewCount' in details['statistics']:
                            view_count = details['statistics']['viewCount']

                    youtube_videos.append({
                        "id": video_id,
                        "title": title,
                        "description": description,
                        "thumbnail": thumbnail,
                        "duration": duration,
                        "view_count": view_count
                    })
            except Exception as e:
                print(f"Error fetching from YouTube API: {e}")
                youtube_videos = []

    return render_template('search_results.html', query=query, jamendo_tracks=jamendo_tracks, soundcloud_embeds=soundcloud_embeds, youtube_videos=youtube_videos)

@app.route('/download_youtube_audio/<video_id>')
def download_youtube_audio(video_id):
    try:
        # Ensure the downloads directory exists
        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'), # Use video ID as filename
            'noplaylist': True, # Ensure only single video is downloaded
        }
        
        audio_file_path = os.path.join(download_dir, f"{video_id}.mp3")

        # Check if the file already exists to avoid re-downloading
        if not os.path.exists(audio_file_path):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
        
        return send_file(audio_file_path, as_attachment=True)

    except yt_dlp.utils.DownloadError as e:
        if "This video is unavailable" in str(e):
            return "Error: This video is unavailable for download.", 400
        elif "Too Many Requests" in str(e):
            return "Error: Too many download requests. Please try again later.", 429
        else:
            return f"Error during download: {e}", 500
    except FileNotFoundError:
        return "Error: FFmpeg is not installed. Please install FFmpeg to enable audio downloads.", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

@app.route('/play_youtube_audio/<video_id>')
def play_youtube_audio(video_id):
    try:
        download_dir = 'downloads'
        audio_file_path = os.path.join(download_dir, f"{video_id}.mp3")

        if not os.path.exists(audio_file_path):
            # If not downloaded, initiate download and then stream
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'),
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

        def generate_audio_stream():
            with open(audio_file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    yield chunk
        
        return Response(stream_with_context(generate_audio_stream()), mimetype='audio/mpeg')

    except yt_dlp.utils.DownloadError as e:
        if "This video is unavailable" in str(e):
            return "Error: This video is unavailable for playback.", 400
        elif "Too Many Requests" in str(e):
            return "Error: Too many playback requests. Please try again later.", 429
        else:
            return f"Error during playback: {e}", 500
    except FileNotFoundError:
        return "Error: FFmpeg is not installed. Please install FFmpeg to enable audio playback.", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)
