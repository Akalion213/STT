import subprocess
import os
from os.path import dirname, abspath
from STTWEBMAIN.models import Videos, Searches, Channels
from STTWEBMAIN.tagging import generate_tags, generate_similar_by_tags
from STTWEBMAIN.vtt_to_txt_test import get_sub_info, convert_subtitle
from STTWEBMAIN.search import video_search
from datetime import datetime
import ast
import json
import requests


def download_subtitles(video_id):
    downloaded = 0
    STT_dir = dirname(dirname(dirname((abspath(__file__)))))
    vtt_sub_directory = os.path.join(STT_dir, 'subs/vttsubs')
    save_location = vtt_sub_directory + '/%(id)s╬%(uploader)s╬%(title)s╬%(upload_date)s'
    response = str(subprocess.Popen(
        ["youtube-dl", "-o", save_location,
         "--ignore-errors", "--write-auto-sub", "--skip-download", video_id],  # '--cookies', 'C:/Users/HOME/Downloads/cookies.txt'
        stdout=subprocess.PIPE).communicate())
    for file in os.listdir(vtt_sub_directory):

        if video_id in file:
            downloaded = file

    return downloaded


def add_video_to_db(video_id, response):
    downloaded = 1
    video_info = get_sub_info(response)
    title = video_info['title']
    date = video_info['date']
    channel = video_info['channel']
    add_channel(video_id, channel)

    convert_subtitle(response)
    tags = generate_tags(response)
    video = Videos(downloaded=downloaded, video_id=video_id, title=title, date=date, channel=channel, tags=tags)
    video.save()
    video.similar_videos = generate_similar_by_tags(video_id)
    video.similar_videos_updated = datetime.now().replace(microsecond=0)
    video.save()
    add_video_to_search(video_id)


def add_video_to_search(video_id):
    searches = Searches.objects.all()
    video = Videos.objects.filter(video_id=video_id).first()
    for search in searches:
        current_search = video_search(video_id + '.en.txt', search.search)
        if current_search > 0:
            search_results = ast.literal_eval(search.result)
            new_results = [video_id, current_search, video.date, video.title, video.channel]
            search_results.append(new_results)
            search.result = search_results
            search.save()


def add_channel(video_id, channel):
    if not Channels.objects.filter(channel_name=channel).first():
        API_key = 'AIzaSyA1GSZTEbP_EmJ3NRquxAnHblXhsy5o4_c'
        request_url_channel_info = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics'
        request_url_video_info = 'https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails'

        r = requests.get(request_url_video_info.format(video_id, API_key))
        responseJson = json.loads(r.content)
        channel_id = responseJson['items'][0]['snippet']['channelId']

        r = requests.get("{}&id={}&key={}".format(request_url_channel_info, channel_id, API_key))
        responseJson = json.loads(r.content)
        profile_img_url = (responseJson['items'][0]['snippet']['thumbnails']['default']['url']).replace('s88', 's100')
        q = Channels(channel_name=channel, profile_img=profile_img_url)
        q.save()
