import csv
import subprocess
from smart_video_cropper import crop_video_detecing_face

# Define the input video file
INPUT_VIDEO = 'input_video.mp4'
DESTINATION_FOLDER='/Users/samuelbezerrab/Developer/scripts/podcast-smart-video-cutter/exported/'

# Read the CSV file
csv_file = 'video_segments.csv'
segments = []

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        segments.append(row)

# Loop through each segment and cut the video
for segment in segments:
    print(segment)
    title = segment['title']
    begin = segment['begin']
    end = segment['end']
    
    video_command = [
        'ffmpeg',
        '-ss', begin,
        '-i', INPUT_VIDEO,
        '-to', end,
        '-c', 'copy',
        f"{DESTINATION_FOLDER}{title}.mp4"
    ]
    
    image_command = [
        'ffmpeg',
        '-ss', begin,
        '-i', INPUT_VIDEO,
        '-vframes', '1',
        '-q:v', '2',
        f"{DESTINATION_FOLDER}{title}.jpg"
    ]

    subprocess.run(image_command)
    subprocess.run(video_command)
    crop_video_detecing_face(f"{DESTINATION_FOLDER}{title}.mp4", f"{DESTINATION_FOLDER}{title}.jpg", f"{DESTINATION_FOLDER}{title}_cropped.mp4")

print("Video segments have been created successfully.")