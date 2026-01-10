import numpy as np
from skimage.feature import hog
import cv2
import argparse

parser = argparse.ArgumentParser(description= 'Generate HOG features')
parser.add_argument('-fileName', type=str, help= 'Image filename prefix', required=True)
parser.add_argument('-pipeline', type=str, choices=['P1', 'P2'], help='P1 or P2', required=True)


args = parser.parse_args()

if args.pipeline == 'P2':
	pp = 0
	ort = 6
	pix = 16
	cel = 3
elif args.pipeline == 'P1':
	pp = 1
	ort = 9
	pix = 16
	cel = 3

fn = args.fileName

preprocess = pp


dataset = np.load(f'./Image_datasets/{fn}.npy')

output_features = []
output_image = []

print(f'Start {pp}_{ort}{pix}{cel}')

for i in range(dataset.shape[0]):
	image = dataset[i].astype(np.uint8)
	if preprocess==2:
		image = (image/(image.max()-image.min()))*255
		#image = image.astype(int)
	elif preprocess==1:
		image = cv2.equalizeHist(image)
		#image = image.astype(int)
	elif preprocess==3:
		image = image/image.std()
		#image = (image/(image.max()-image.min()))*255
		#image = image.astype(int)
	hog_features, hog_image = hog(image, orientations=ort, pixels_per_cell=(pix, pix), cells_per_block=(cel, cel), visualize=True, block_norm="L2-Hys")
	output_features.append(hog_features)
	output_image.append(hog_image)
	
	
np.save(f'./HOG_datasets/{fn}_HOGfeatures_{pp}_{ort}{pix}{cel}.npy', np.array(output_features))
print(f'{fn}_HOGfeatures_{pp}_{ort}{pix}{cel}.npy saved in folder HOG_datasets\nFeature vector length {len(hog_features)}')
