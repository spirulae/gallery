import re
from hashlib import md5
import os
import datetime

image_dir = 'img/'
#image_dir = '../miscellaneous/discord/attachments'

image_files = [file for file in os.listdir(image_dir)
               if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort(key=lambda x: -int(x.split('-')[0]))

hashes = set()


def snowflake_time(snowflake):
    return datetime.datetime.utcfromtimestamp(((int(snowflake) >> 22) + 1420070400000) / 1000)

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Spirulae Gallery</title>
    <style>
        img { max-height: 180px; max-width: 30%; }
    </style>
</head>
<body>
"""

prev_month = None

for fi in range(len(image_files)):
    image_file = os.path.join(image_dir, image_files[fi])
    h = md5(open(image_file, 'rb').read()).hexdigest()
    if h in hashes:
        continue
    hashes.add(h)

    date = snowflake_time(image_files[fi].split('-')[0])
    month = date.strftime('%B %Y')
    date = date.strftime('%Y-%m-%d')

    print(fi, '/', len(image_files), date)

    if month != prev_month:
        if prev_month != None:
            html += "<br/><hr/>\n"
        html += "<h1>" + month + "</h1>\n"
        prev_month = month
    html += f"""<img src="{image_file}" title="{date}" loading="lazy"/>\n"""

html += """</body>"""

print(len(hashes), "images")


open("gallery.html", "w").write(html)
