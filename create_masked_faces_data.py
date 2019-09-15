import cv2
import os
import numpy as np

img_path = 'face_images'
mask_path = 'face_masks'
final_images_path = 'masked_faces'

MAX_RANDOM_SCALE = 5.0
MIN_RANDOM_SCALE = 1.0

MASK_BASE_SIZE = 50
MAX_MASK_COUNT = 2

REPEAT_IMG = 3

# Load mask files
masks = []
mask_file_list = [f for f in os.listdir(mask_path) if os.path.isfile(os.path.join(mask_path, f))]
for file in mask_file_list:
	masks.append(cv2.imread(os.path.join(mask_path, file))//255)

print(len(masks))

# Load image files and append generated "input" image
img_list = os.listdir(img_path)
img_count = len(img_list)
for i, img_file in enumerate(img_list):
	for j in range(REPEAT_IMG):
		print("Processing image {}.{}/{}".format(i+1, j, img_count))
		img = cv2.imread(os.path.join(img_path, img_file))
		shape = img.shape
		#if shape[0] < 300 or shape[1] < 300:
		#	print("Image {} omited".format(i+1))
		#	continue

		# Number of masks to apply to the image
		num_masks = np.random.random_integers(low=1, high=MAX_MASK_COUNT)

		rnd_mask_idx = np.random.randint(len(masks), size=num_masks)
		masks_to_apply = [masks[i] for i in rnd_mask_idx]

		scales = (MAX_RANDOM_SCALE-MIN_RANDOM_SCALE)*np.random.random(num_masks) + MIN_RANDOM_SCALE

		mask_sizes = [MASK_BASE_SIZE*s for s in scales]
		pos_x = [np.random.random_integers(low=0, high=int(shape[1]-mask_sizes[i])) for i in range(num_masks)]
		pos_y = [np.random.random_integers(low=0, high=int(shape[0]-mask_sizes[i])) for i in range(num_masks)]

		mask = np.ones_like(img)

		for idx, m in enumerate(masks_to_apply):
			scaled_m = cv2.resize(m, (int(mask_sizes[idx]), int(mask_sizes[idx])))
			mask[pos_y[idx]:int(pos_y[idx]+mask_sizes[idx]), pos_x[idx]:int(pos_x[idx]+mask_sizes[idx]), :] *= scaled_m

		final_img = np.tile(img, (1, 2 ,1))  # Repeat twice in the columns axis only
		final_img[:, shape[1]:, :] *= mask

		final_img = cv2.resize(final_img, (256*2, 256), cv2.INTER_AREA)

		# cv2.imshow('asdf', final_img)
		# cv2.waitKey()
		base_name, ext = os.path.splitext(img_file)
		new_filename = base_name + '_' + str(j) + ext
		cv2.imwrite(os.path.join(final_images_path, new_filename), final_img)