import re

# List of YouTube URLs
urls = [
    "https://www.youtube.com/watch?v=CHuu-CHkMxI&t=8s",
    "https://www.youtube.com/watch?v=QY8dhl1EQfI",
    "https://www.youtube.com/watch?v=w0bkWcoAveY&t=1807s"
]

# Regex pattern to find the value of 'v' until '&' if it exists
pattern = re.compile(r'(?<=v=)[^&]+')
v_id = []
# Extracting the values
for url in urls:
    match = pattern.search(url)
    if match:
        v_id.append(match.group())
        print("Extracted value:", match.group())
    else:
        print("No match found.")
print(v_id)