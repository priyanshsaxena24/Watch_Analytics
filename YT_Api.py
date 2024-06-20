import json
from googleapiclient.discovery import build
import pprint

api_key = 'AIzaSyDCl63gOVqroMQ8IoUNF5ePYEIbMEkiPro'

yt = build('youtube','v3',developerKey=api_key)
fin_data=[]
category = []
final_data = {}
video=[]
with open ('data.json','r') as f:
    data = json.load(f)
    for i in data.keys():
        for j in data[i]:
            video.append(j[0])
            request = yt.videos().list(
                part='snippet',
                id = j[0]
            )
            response = request.execute()
            for item in response['items'] : 
                cat = item['snippet']['categoryId']
                category.append(cat)
                channel = item['snippet']['channelTitle']
                final_data[j[0]] = [cat,channel]
            fin_data.append(final_data)


# request = yt.videos().list(
#                 part='snippet',
#                 id = video
#             )
# response = request.execute() 
# print(len(response['items']))
# for item in response['items'] : 
#     cat = item['snippet']['categoryId']
#     channel = item['snippet']['channelTitle']
