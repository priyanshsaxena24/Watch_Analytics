import json

def time_to_seconds(timestr):
    parts = timestr.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = int(parts[0]), int(parts[1])
        return minutes * 60 + seconds
    else:
        return int(timestr)

# Load the first JSON file (daily watch time data)
with open('data.json', 'r') as file:
    daily_watch_time = json.load(file)

# Load the second JSON file (video details)
with open('vid_data.json', 'r') as file:
    video_details = json.load(file)

# Create a dictionary from the video details for quick access by videoID
video_details_dict = {video['videoID']: video for video in video_details['videos']}

# Prepare the merged data structure
merged_data = {}

# Loop through each day and each video watch record, enriching with video details
for day, videos in daily_watch_time.items():
    merged_videos = []
    for video in videos:
        video_id = video['videoID']
        if video_id in video_details_dict:
            # Merge the watch time data with the detailed video data
            merged_video_data = {**video, **video_details_dict[video_id]}
            # Convert watch time to seconds if needed (assumes all time values need conversion)
            if isinstance(merged_video_data['watchTime'], str):
                merged_video_data['watchTime'] = time_to_seconds(merged_video_data['watchTime'])
            merged_videos.append(merged_video_data)
    merged_data[day] = merged_videos


# Save the merged data to a new JSON file
with open('merged_data.json', 'w') as file:
    json.dump(merged_data, file)
