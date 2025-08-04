import numpy as np
from skimage.feature import hog
import cv2
import argparse

parser = argparse.ArgumentParser(description= 'Generate HOG features')
parser.add_argument('fileName', type=str, help= 'file name')
parser.add_argument('pp', type=int, help= 'None: 0, Histogram equalization: 1, Image normalization: 2, Division by standard deviation: 3')
parser.add_argument('ort', type=int, help='Orientations. standard = 9')
parser.add_argument('pix', type=int, help='Pixels per cell. standard=8')
parser.add_argument('cel', type=int, help='Cells per block. standard=2')


args = parser.parse_args()

fn = args.fileName

preprocess = args.pp


dataset = np.load(f'./Image_datasets/{fn}.npy')

output_features = []
output_image = []

print(f'Start {args.pp}_{args.ort}{args.pix}{args.cel}')

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
	hog_features, hog_image = hog(image, orientations=args.ort, pixels_per_cell=(args.pix, args.pix), cells_per_block=(args.cel, args.cel), visualize=True, block_norm="L2-Hys")
	output_features.append(hog_features)
	output_image.append(hog_image)
	
	
np.save(f'./HOG_datasets/{fn}_HOGfeatures_{args.pp}_{args.ort}{args.pix}{args.cel}.npy', np.array(output_features))
print(f'Done {args.pp}_{args.ort}{args.pix}{args.cel}')
