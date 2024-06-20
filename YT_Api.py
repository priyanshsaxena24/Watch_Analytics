from pprint import pprint as pp
import json
from googleapiclient.discovery import build

api_key = 'AIzaSyDCl63gOVqroMQ8IoUNF5ePYEIbMEkiPro'

yt = build('youtube','v3',developerKey=api_key)

request = yt.videos().list(
        part='snippet,contentDetails',
        id = '5yauOziwbtE'


    )

response = request.execute()

print(response['items'][0]['snippet']['channelTitle'])