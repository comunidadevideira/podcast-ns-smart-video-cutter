from retinaface import RetinaFace
from PIL import Image 
import subprocess
import math

VIDEO_PROPORTION = 1080 / 1920
HEAD_PERCENTAGE_FOR_FRAME_WIDHT=25 # %, the detected head correpond to X% of the frame desired width

def cut_video(source_video, begin, end, destination_video):
    ffmpeg_command = [
        'ffmpeg',
        '-ss', begin,
        '-to', end,
        '-i', source_video,
        '-c', 'copy',
        destination_video
    ]

    subprocess.run(ffmpeg_command)

def extract_first_frame_image(source_video, at_time, destination_video):
    ffmpeg_command = [
        'ffmpeg',
        '-ss', at_time,
        '-i', source_video,
        '-vframes', '1',
        '-q:v', '2',
        destination_video
    ]

    subprocess.run(ffmpeg_command)

def crop_video_detecing_face(source_video, source_image, destination_video):

    img = Image.open(source_image)
    image_width = img.width
    image_height = img.height

    faces = RetinaFace.detect_faces(source_image)
    print(f"Face detected at: {faces['face_1']['facial_area']}")
    x1, y1, x2, y2 = faces['face_1']['facial_area']

    face_width = x2 - x1

    total_width = face_width / (HEAD_PERCENTAGE_FOR_FRAME_WIDHT / 100)

    final_x = ((x2 + x1) / 2 ) - (total_width / 2)

    if (final_x < 0): # Protect overlap on X axis
        final_x = 0

    if (final_x + total_width > image_width):
        final_x = final_x - (final_x + total_width - image_width)

    total_height = total_width * VIDEO_PROPORTION
    final_y = y1 - (y2 - y1)

    if (final_y < 0): # Protect overlap on Y axis
        final_y = 0

    if (final_y + total_height > image_height):
        final_y = final_y - (final_y + total_height - image_height)

    final_x = round(final_x) # Round
    final_y = round(final_y)
    total_width = round(total_width)
    total_height = round(total_height)

    # Crop the video
    cropped_video_command = [
        'ffmpeg', '-i', source_video,
        '-vf', f"crop={total_width}:{total_height}:{final_x}:{final_y}",
        '-c:v', 'libx264', f"{destination_video}"
    ]

    subprocess.run(cropped_video_command)
