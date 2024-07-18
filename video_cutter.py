import csv
import subprocess
from smart_video_cropper import crop_video_detecing_face

# Define the input video file
INPUT_VIDEO = 'input_video.mp4'

# Read the CSV file
csv_file = 'video_segments.csv'
segments = []

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        segments.append(row)

# Function to convert time format
def convert_time_to_seconds(time_str):
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

# Loop through each segment and cut the video
for segment in segments:
    print(segment)
    title = segment['title']
    begin = segment['begin']
    end = segment['end']
    
    output_file = f"{title}.mp4"
    
    video_command = [
        'ffmpeg',
        '-i', INPUT_VIDEO,
        '-ss', begin,
        '-to', end,
        '-c', 'copy',
        f"{title}.mp4"
    ]
    
    image_command = [
        'ffmpeg',
        '-ss', begin,
        '-i', INPUT_VIDEO,
        '-vframes', '1',
        '-q:v', '2',
        f"{title}.jpg"
    ]

    subprocess.run(image_command)
    subprocess.run(video_command)
    crop_video_detecing_face(f"{title}.mp4", f"{title}.jpg")

print("Video segments have been created successfully.")