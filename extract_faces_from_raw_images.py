import cv2
import os
import json

RAW_IMG_PATH = 'raw_face_images'
FINAL_IMG_PATH = 'face_images'
files = os.listdir(RAW_IMG_PATH) # [f for f in os.listdir(RAW_IMG_PATH) if os.path.isfile(f)]

# Sort numerically
file_splitext = [os.path.splitext(f) for f in files]
file_base, file_ext = list(zip(*file_splitext))[0], list(zip(*file_splitext))[1]
file_num = [int(n[3:]) for n in file_base]
file_num.sort()

sorted_files = ['img'+str(n)+'.png' for n in file_num]


with open('face_detection.json', 'r') as handle:
	data_info = [json.loads(line) for line in handle]

img_count = len(sorted_files)
for i, (file, info) in enumerate(zip(sorted_files, data_info)):
	print("Processing image {}/{}".format(i+1, img_count))

	img = cv2.imread(os.path.join(RAW_IMG_PATH, file))

	labels = info.get('annotation')
	if labels is None:
		continue

	for j, label in enumerate(labels):
		coords = label['points']
		w = label['imageWidth']
		h = label['imageHeight']
		
		p1 = (round(coords[0]['x']*w), round(coords[0]['y']*h))
		p2 = (round(coords[1]['x']*w), round(coords[1]['y']*h))

		print(p1)
		print(p2)
		print(file)
		face_crop = img[p1[1]:p2[1], p1[0]:p2[0], :]

		scaled_face_crop = cv2.resize(face_crop, (256, 256))

		base_name, _ = os.path.splitext(file)
		cv2.imwrite(os.path.join(FINAL_IMG_PATH, base_name +'_'+ str(j)+'.png') ,scaled_face_crop)

