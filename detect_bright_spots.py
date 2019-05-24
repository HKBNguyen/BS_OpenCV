from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

# construct argument parser and use option to look for image file
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

#read the image file into image and convert to grayscale and use Gaussian blur to reduce noise
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# threshold takes any pixel value >= 200 and converts it to 255 ie purely white
# anything lower than 200 is converted to purely black
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

# more smoothing to remove noise; erode and dilate to reduce more noise
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)


labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")

# loop over the unique components
for label in np.unique(labels):
	# if this is the background label, ignore it
	if label == 0:
		continue

	# otherwise, construct the label mask and count the
	# number of pixels
	labelMask = np.zeros(thresh.shape, dtype="uint8")
	labelMask[labels == label] = 255
	numPixels = cv2.countNonZero(labelMask)

	# if the number of pixels in the component is sufficiently
	# large, then add it to our mask of "large blobs"
	if numPixels > 300:
		mask = cv2.add(mask, labelMask)

cv2.imshow("Altered Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()