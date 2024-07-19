import csv
import os
from smart_video_cropper import crop_video_detecing_face, cut_video, extract_first_frame_image

# Define the input video file
INPUT_VIDEO = 'input_video.mov'
DESTINATION_FOLDER='/Users/samuelbezerrab/Developer/scripts/podcast-smart-video-cutter/exported/'
CSV_FILE = 'video_segments.csv'

# Read the CSV file
segments = []
input_video_extension = os.path.splitext(INPUT_VIDEO)[1]

with open(CSV_FILE, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        segments.append(row)

# Loop through each segment and cut the video
for segment in segments:
    print(segment)
    title = segment['title']
    begin = segment['begin']
    end = segment['end']

    extract_first_frame_image(INPUT_VIDEO, begin, f"{DESTINATION_FOLDER}{title}.jpg")
    cut_video(INPUT_VIDEO, begin, end, f"{DESTINATION_FOLDER}{title}.{input_video_extension}")
    crop_video_detecing_face(f"{DESTINATION_FOLDER}{title}.{input_video_extension}", f"{DESTINATION_FOLDER}{title}.jpg", f"{DESTINATION_FOLDER}{title}_cropped.{input_video_extension}")

print("Video segments have been created successfully.")
