import requests
import json

API_key = 'AIzaSyA1GSZTEbP_EmJ3NRquxAnHblXhsy5o4_c'
video_id = 't4mJ5FcNkTY'
request_url_channel_info = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics'
request_url_video_info = 'https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=snippet,contentDetails'

r = requests.get(request_url_video_info.format(video_id, API_key))
responseJson = json.loads(r.content)
channel_id = responseJson['items'][0]['snippet']['channelId']

r = requests.get("{}&id={}&key={}".format(request_url_channel_info, channel_id, API_key))
responseJson = json.loads(r.content)
print((responseJson['items'][0]['snippet']['thumbnails']['default']['url']).replace('s88', 's100'))
