import json
from googleapiclient.discovery import build

# def time_to_seconds(timestr):
#     parts = timestr.split(':')
#     if len(parts) == 3:
#         hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
#         return hours * 3600 + minutes * 60 + seconds
#     elif len(parts) == 2:
#         minutes, seconds = int(parts[0]), int(parts[1])
#         return minutes * 60 + seconds
#     else:
#         return int(parts[0])

api_key = 'AIzaSyDCl63gOVqroMQ8IoUNF5ePYEIbMEkiPro'

yt = build('youtube','v3',developerKey=api_key)


categoryID = []

with open('data.json', 'r') as f:
    data = json.load(f)

vid_code = [j['videoID'] for i in data.keys() for j in data[i]]
time = [j['watchTime'] for i in data.keys() for j in data[i]]

# seconds = [time_to_seconds(ts) for ts in time]

req = yt.videos().list(
    part='snippet',
    id = vid_code
)

res = req.execute()
print(len(res['items']))
videos = []
category_ids = []

for item in res['items']:
    video = {
        'videoID' : item['id'],
        'channelName' : item['snippet']['channelTitle'],
        'videoTitle' : item['snippet']['title'],
        'categoryID' : item['snippet']['categoryId'],
    }
    categoryID.append(item['snippet']['categoryId'])
    videos.append(video)


req_1 = yt.videoCategories().list(
    part='snippet',
    id = categoryID
)  
res_1 = req_1.execute()

category_titles = {item['id']: item['snippet']['title'] for item in res_1['items']}

for video in videos:
    video['category'] = category_titles[video['categoryID']]

with open("vid_data.json", 'w') as file:
    json.dump({"videos": videos}, file)
