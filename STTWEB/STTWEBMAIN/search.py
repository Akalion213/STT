import os
from os.path import dirname, abspath
import json

# profile_image_url = dirname((abspath(__file__))) + '\\static\\profile\\'


def convert_date2(date):
    new_date2 = date[0:4] + '/' + date[4:6] + '/' + date[6:8]
    return new_date2


def video_deep_search(filename, search):
    results = []
    search = search.lower()
    txt_time_sub_dir = os.path.join(dirname(dirname(dirname((abspath(__file__))))), 'subs/txt_time_subs/')
    with open(os.path.join(txt_time_sub_dir, filename), encoding="utf8") as f:
        index = -1
        for line in f:
            index += 1
            #print(line, index)
            if search in line.lower():
                results.append(index)
    return results


def video_deep_search_details(results):
    from .util import convert_seconds
    lines = []
    final_results = []
    watch_link = 'https://youtu.be/'
    txt_time_sub_dir = os.path.join(dirname(dirname(dirname((abspath(__file__))))), 'subs/txt_time_subs')
    f = open(os.path.join(txt_time_sub_dir, results[0] + '.en.txt'), 'r', encoding="utf8")
    results_number = len(results) - 1  # Amount of times search term was used in video
    for line in f:
        lines.append(line)
    f.close()
    for index in results[1:]:
        video_time = int(lines[index][0:2]) * 3600 + int(lines[index][3:5]) * 60 + int(lines[index][6:8])
        if video_time > 3:
            video_time -= 3
        result_string = [str(video_time),     # watch_link + results[0] + '?t=' + str(video_time)
                         lines[index][9:].replace('\n', ' '), convert_seconds(video_time), video_time]

        final_results.append(result_string)

    return final_results


def video_search_all(search_term, channel):
    from STTWEBMAIN.models import Videos, Searches

    STT_dir = dirname(dirname(dirname((abspath(__file__)))))
    txt_time_sub_directory = os.path.join(STT_dir, 'subs/txt_time_subs')

    search = [x.lower() for x in search_term]
    print(search)
    results = []
    Continue = True
    Write = True

    if Searches.objects.filter(search=search, channel=channel).exists():  # if search already in database pull the results
        results = Searches.objects.filter(search=search, channel=channel).first()
        results = json.loads(results.result)
        Continue = False  # Don't search files
        Write = False  # Don't save the results to database

    if channel == 'all':
        videos = Videos.objects.filter(downloaded=1).all()
    else:
        videos = Videos.objects.filter(downloaded=1, channel=channel).all()

    if Continue:
        for video in videos:
            temp = video_search(video.video_id + '.en.txt', search)
            if temp > 1:
                temp_result = [video.video_id, temp, video.date, video.title, video.channel]
                results.append(temp_result)

        if Write:
            q = Searches(search=search, result=json.dumps(results), channel=channel)
            q.save()

    search_db = Searches.objects.filter(search=search, channel=channel).first()
    search_db.times_searched += 1
    search_db.save()
    return json.dumps(results)


def video_search(filename, search):
    txt_time_sub_dir = os.path.join(dirname(dirname(dirname((abspath(__file__))))), 'subs/txt_time_subs/')
    with open(os.path.join(txt_time_sub_dir, filename), encoding="utf8") as f:
        content = f.read().lower()

    if len(search) == 1:
        search = search[0].lower()
        if search in content:
            results = content.count(search)
        else:
            results = 0
    else:
        search = [x.lower() for x in search]
        results = 0
        for search_term in search:
            if search_term in content:
                results += content.count(search_term)
            else:
                results = 0

    return results
