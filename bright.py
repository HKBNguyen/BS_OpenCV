import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
# add option for image and radius of how big the Gaussian blur is to idenitfy the largest value
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-r", "--radius", type = int,
	help = "radius of Gaussian blur; must be odd")
# then actually parse the arguments
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

orig = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
