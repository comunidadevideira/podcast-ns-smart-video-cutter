from retinaface import RetinaFace
import subprocess
import math

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
IMAGE_WIDTH = 640
IMAGE_HEIGTH = 360
HEAD_PERCENTAGE_FOR_FRAME_WIDHT=25

def crop_video_detecing_face(source_video, source_image):

    faces = RetinaFace.detect_faces(source_image)
    print(f"Face detected at: {faces['face_1']['facial_area']}")
    x1, y1, x2, y2 = faces['face_1']['facial_area']

    face_width = x2 - x1

    total_width = face_width / (HEAD_PERCENTAGE_FOR_FRAME_WIDHT / 100)

    final_x = ((x2 + x1) / 2 ) - (total_width / 2)

    if (final_x < 0): # Protext overlap on X axis
        final_x = 0

    if (final_x + total_width > IMAGE_WIDTH):
        final_x = final_x - (final_x + total_width - IMAGE_WIDTH)

    total_height = total_width * (VIDEO_HEIGHT / VIDEO_WIDTH)
    final_y = y1 - (y2 - y1)

    if (final_y < 0): # Protext overlap on Y axis
        final_y = 0

    if (final_y + total_height > IMAGE_HEIGTH):
        final_y = final_y - (final_y + total_height - IMAGE_HEIGTH)

    final_x = math.trunc(final_x) # Round
    final_y = math.trunc(final_y)
    total_width = math.trunc(total_width)
    total_height = math.trunc(total_height)

    # Crop the video
    cropped_video_command = [
        'ffmpeg', '-i', source_video,
        '-vf', f"crop={total_width}:{total_height}:{final_x}:{final_y}, scale=1080:1920",
        '-c:v', 'libx264', f"cropped_{source_video}"
    ]

    subprocess.run(cropped_video_command)
