import re
from hashlib import md5
import os
import markdown
from datetime import datetime
import json

json_path = "raw/attachments.json"
with open(json_path, 'r') as fp:
    attachment_info = json.load(fp)
image_url = {}
for url, filename in attachment_info:
    filename = filename[:filename.rfind('.')]
    image_url[filename] = url

image_dir = 'img/'
#image_dir = '../miscellaneous/discord/img'

image_files = [file for file in os.listdir(image_dir)
               if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
image_files.sort(key=lambda x: -int(x.split('-')[0]))

hashes = set()


def snowflake_time(snowflake):
    return datetime.utcfromtimestamp(((int(snowflake) >> 22) + 1420070400000) / 1000)

description = open("html_description.md").read()
description = markdown.markdown(description)

updated = datetime.now().strftime("%Y/%m/%d")
description = description.replace("{%updated%}", updated)

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Spirulae Gallery</title>
    <link rel="stylesheet" href="style.css" />
    <script src="script.js"></script>
</head>
<body>
    <div id="display-container" style="display:none">
        <img id="display" src="" />
    </div>

    <h1>Spirulae Gallery</h1>
    <div style="max-width:800px">
        """ + description + """
    </div>
    <hr/>

    <div id="content">
"""

prev_month = None

for fi in range(len(image_files)):
    filename = image_files[fi]
    image_file = os.path.join(image_dir, filename)
    h = md5(open(image_file, 'rb').read()).hexdigest()
    if h in hashes:
        continue
    hashes.add(h)

    snowflake = filename.split('-')[0]
    date = snowflake_time(snowflake)
    month = date.strftime('%B %Y')
    date = date.strftime('%Y-%m-%d')
    key = filename[:filename.rfind('.')]
    if key not in image_url:
        print("Missing info:", filename)
        continue
    url = image_url[key]

    #print(fi, '/', len(image_files), date)

    if month != prev_month:
        if prev_month != None:
            html += "<br/><hr/>\n"
        html += "<h1>" + month + "</h1>\n"
        prev_month = month
    html += f"""<a href="{url}"><img id="{snowflake}" src="{image_file}" title="{date}" loading="lazy"/></a>\n"""

html += """
    </div>
</body>"""

print(len(hashes), "images")


open("index.html", "w").write(html)
