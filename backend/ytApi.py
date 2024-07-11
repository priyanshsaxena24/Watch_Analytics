# import time
# import json
# import time
# from googleapiclient.discovery import build
# import re

# def parse_duration(duration_str):
#     match = duration_pattern.match(duration_str)
    
#     if not match:
#         return 0
#     hours = int(match.group(1)[:-1]) if match.group(1) else 0
#     minutes = int(match.group(2)[:-1]) if match.group(2) else 0
#     seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    
#     total_seconds = hours * 3600 + minutes * 60 + seconds
#     return total_seconds

# def chunk_list(lst, chunk_size):
#     """Divide a list into chunks of specified size."""
#     for i in range(0, len(lst), chunk_size):
#         yield lst[i:i + chunk_size]

# duration_pattern = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')

# api_key = 'AIzaSyDCl63gOVqroMQ8IoUNF5ePYEIbMEkiPro'
# yt = build('youtube','v3',developerKey=api_key)

# categoryID = []

# with open('data.json', 'r') as f:
#     data = json.load(f)

# vid_code = [j['videoID'] for i in data.keys() for j in data[i] if 'videoID' in j and j['videoID'] is not None]
# times = {j['videoID']: j['watchTime'] for i in data.keys() for j in data[i] if 'watchTime' in j and j['videoID']}

# videos_with_blank_watchtime = [vid for vid, time in times.items() if time == ""]

# for chunk in chunk_list(videos_with_blank_watchtime, 50):
#     req = yt.videos().list(
#         part='snippet,contentDetails',
#         id=','.join(chunk)
#     )
#     res = req.execute()
#     for item in res['items']:
#         duration_str = item['contentDetails']['duration']
#         duration_seconds = parse_duration(duration_str)
#         times[item['id']] = str(duration_seconds)

# for chunk in chunk_list(vid_code, 50):
#     req = yt.videos().list(
#         part='snippet',
#         id=','.join(chunk)
#     )

#     res = req.execute()
#     print(len(res['items']))
#     videos = []
#     category_ids = []

#     for item in res['items']:
#         video = {
#             'videoID': item['id'],
#             'channelName': item['snippet']['channelTitle'],
#             'videoTitle': item['snippet']['title'],
#             'categoryID': item['snippet']['categoryId'],
#             'watchTime': times[item['id']]
#         }
#         category_ids.append(item['snippet']['categoryId'])
#         videos.append(video)

# # Fetch category details
# req_1 = yt.videoCategories().list(
#     part='snippet',
#     id=','.join(set(category_ids))
# )
# res_1 = req_1.execute()

# category_titles = {item['id']: item['snippet']['title'] for item in res_1['items']}

# for video in videos:
#     video['category'] = category_titles[video['categoryID']]

# with open("vid_data.json", 'w') as file:
#     json.dump({"videos": videos}, file)







# # Fetch video details including duration for videos with blank watchTime
# if videos_with_blank_watchtime:
#     req = yt.videos().list(
#         part='contentDetails',
#         id=','.join(videos_with_blank_watchtime)
#     )
    
#     res = req.execute()
#     for item in res['items']:
#         duration_str = item['contentDetails']['duration']
#         duration_seconds = parse_duration(duration_str)
#         times[item['id']] = str(duration_seconds)

# req = yt.videos().list(
#     part='snippet',
#     id = vid_code
# )


# res = req.execute()
# videos = []
# category_ids = []

# for item in res['items']:
#     video = {
#         'videoID': item['id'],
#         'channelName': item['snippet']['channelTitle'],
#         'videoTitle': item['snippet']['title'],
#         'categoryID': item['snippet']['categoryId'],
#         'watchTime': times[item['id']]
#     }
#     category_ids.append(item['snippet']['categoryId'])
#     videos.append(video)

# req_1 = yt.videoCategories().list(
#     part='snippet',
#     id = categoryID
# )  
# res_1 = req_1.execute()

# category_titles = {item['id']: item['snippet']['title'] for item in res_1['items']}

# for video in videos:
#     video['category'] = category_titles[video['categoryID']]

# with open("vid_data.json", 'w') as file:
#     json.dump({"videos": videos}, file)






import json
import re
from googleapiclient.discovery import build

# Your YouTube API key
api_key = 'AIzaSyDCl63gOVqroMQ8IoUNF5ePYEIbMEkiPro'
yt = build('youtube', 'v3', developerKey=api_key)

# Regular expression to match the duration string
duration_pattern = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')

def parse_duration(duration_str):
    match = duration_pattern.match(duration_str)
    
    if not match:
        return 0
    
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def chunk_list(lst, chunk_size):
    """Divide a list into chunks of specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

with open('data.json', 'r') as f:
    data = json.load(f)

# Collect video IDs and their respective watch times
vid_code = [j['videoID'] for i in data.keys() for j in data[i] if 'videoID' in j and j['videoID'] is not None]
watch_times = {j['videoID']: j['watchTime'] for i in data.keys() for j in data[i] if 'watchTime' in j and j['videoID']}

# Identify videos with blank watchTime
videos_with_blank_watchtime = [vid for vid, time in watch_times.items() if time == "" and vid is not None]

# Fetch video details including duration for videos with blank watchTime
for chunk in chunk_list(videos_with_blank_watchtime, 50):
    req = yt.videos().list(
        part='snippet,contentDetails',
        id=','.join(chunk)
    )
    
    res = req.execute()
    for item in res['items']:
        duration_str = item['contentDetails']['duration']
        duration_seconds = parse_duration(duration_str)
        watch_times[item['id']] = str(duration_seconds)

# Initialize the final list to store all videos
videos = []
category_ids = []

# Fetch video details for all videos
for chunk in chunk_list(vid_code, 50):
    req = yt.videos().list(
        part='snippet',
        id=','.join(chunk)
    )

    res = req.execute()
    for item in res['items']:
        video = {
            'videoID': item['id'],
            'channelName': item['snippet']['channelTitle'],
            'videoTitle': item['snippet']['title'],
            'categoryID': item['snippet']['categoryId'],
            'watchTime': watch_times[item['id']]
        }
        category_ids.append(item['snippet']['categoryId'])
        videos.append(video)

# Fetch category details
req_1 = yt.videoCategories().list(
    part='snippet',
    id=','.join(set(category_ids))
)
res_1 = req_1.execute()

category_titles = {item['id']: item['snippet']['title'] for item in res_1['items']}

for video in videos:
    video['category'] = category_titles[video['categoryID']]

with open("vid_data.json", 'w') as file:
    json.dump({"videos": videos}, file)

print("Completed!")
