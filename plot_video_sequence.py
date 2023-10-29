import os
import cv2
import numpy as np
from hashlib import md5

# Path to the directory containing the images
image_dir = 'raw'

# Output video file name and codec (e.g., 'output_video.mp4')
output_video = 'spirulae_raw.mp4'
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for mp4 format

# Fixed frame rate (frames per second)
frame_rate = 20

# Get a list of image files in the directory, sorted by file id
image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort(key=lambda x: int(x.split('/')[-1].split('-')[0]))

# Get the dimensions for the video frames
frame_height, frame_width = 480, 640

# Initialize the VideoWriter
video_writer = cv2.VideoWriter(output_video, fourcc, frame_rate, (frame_width, frame_height))

hashes = set()

# Loop through the images, resize and add them to the video
for fi in range(len(image_files)):
    image_file = image_files[fi]
    h = md5(open(image_file, 'rb').read()).hexdigest()
    if h in hashes:
        continue
    hashes.add(h)
    print(fi, '/', len(image_files))

    image = cv2.imread(image_file)

    image_height, image_width, _ = image.shape
    sc = min(frame_width / image_width, frame_height / image_height)
    new_width = round(sc * image_width)
    new_height = round(sc * image_height)
    image = cv2.resize(image, (new_width, new_height))

    padding_top = (frame_height - new_height) // 2
    padding_bottom = frame_height - new_height - padding_top
    padding_left = (frame_width - new_width) // 2
    padding_right = frame_width - new_width - padding_left

    padded_image = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    padded_image[padding_top:padding_top+new_height,
                 padding_left:padding_left+new_width, :] = image

    # Write the frame to the video
    video_writer.write(padded_image)

# Release the VideoWriter
video_writer.release()

print(len(hashes), "frames")

os.system("ffmpeg -y -i spirulae_raw.mp4 -vcodec libx264 -crf 28 spirulae.mp4")
