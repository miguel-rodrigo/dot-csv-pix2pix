import os
import json
import requests

with open('face_detection.json', 'r') as handle:
	data_info = [json.loads(line) for line in handle]

image_links = [line['content'] for line in data_info]

IMG_DOWNLOAD_DIR = 'raw_face_images'

img_count = len(image_links)
for i, link in enumerate(image_links):
	print("Downloading image {}/{}".format(i+1, img_count))
	with open(os.path.join(IMG_DOWNLOAD_DIR, 'img'+str(i)+'.png'), 'wb') as handle:
		response = requests.get(link, stream=True)

		if not response.ok:
			print(response)

		for block in response.iter_content(1024):
			if not block:
			    break
			handle.write(block)
