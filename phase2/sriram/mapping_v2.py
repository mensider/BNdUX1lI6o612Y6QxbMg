# import the opencv library
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyrsistent import rex

webcam = cv2.VideoCapture('http://192.168.43.1:8080/video')


def clahe(img, clip_limit=2.0, grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    return clahe.apply(img)


def bigbox(src):
    # HSV thresholding to get rid of as much background as possible
    hsv = cv2.cvtColor(src.copy(), cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 0, 120])
    upper_blue = np.array([180, 38, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(src, src, mask=mask)
    b, g, r = cv2.split(result)
    g = clahe(g, 5, (3, 3))

    # Adaptive Thresholding to isolate the bed
    img_blur = cv2.blur(g, (9, 9))
    img_th = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 51, 2)

    contours, hierarchy = cv2.findContours(img_th,
                                           cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # Filter the rectangle by choosing only the big ones
    # and choose the brightest rectangle as the bed
    max_brightness = 0
    canvas = src.copy()
    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        if w * h > 100:
            mask = np.zeros(src.shape, np.uint8)
            mask[y:y + h, x:x + w] = src[y:y + h, x:x + w]
            brightness = np.sum(mask) / w * h
            if brightness > max_brightness:
                brightest_rectangle = rect
                max_brightness = brightness

    return brightest_rectangle

def neighbour(ls, term):
    ls = np.array(ls)
    l = ls[ls <= term][-1]
    h = ls[ls > term][0]

    l = np.argmax(ls == l)
    h = np.argmax(ls == h)

    return l, h

def box_it(image):
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th1, img_bin = cv2.threshold(gray_scale, 125, 200, cv2.THRESH_BINARY)
    img_bin = ~img_bin

    line_min_width = 15

    kernal_h = np.ones((1, line_min_width), np.uint8)
    kernal_v = np.ones((line_min_width, 1), np.uint8)

    img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)

    img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)

    img_bin_final = img_bin_h | img_bin_v

    final_kernel = np.ones((3, 3), np.uint8)
    img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=1)

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

    dimage = image.copy()

    w_sum = 0
    h_sum = 0

    for jj, [x, y, w, h, area] in enumerate(stats[2:]):
        w_sum += w
        h_sum += h

    w_avg = w_sum / len(stats[2:])
    h_avg = h_sum / len(stats[2:])

    X, Y, N, W, H = [], [], [], [], []

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    numbers = [str(i + 1) for i in range(14)]

    combination = []

    for l in letters:
        for n in numbers:
            combination.append(l + n)

    ### skipping the first 2 labels, why?
    ### 1 and 0 and the background and residue connected components whihc we do not require
    # for jj, [x, y, w, h, area] in zip(combination, stats[2:]):

    for jj, [x, y, w, h, area] in enumerate(stats[2:]):
        if w > w_avg / 2 and w < 1.5 * w_avg and h > h_avg / 2 and h < 1.5 * h_avg:

            X.append(x)
            Y.append(y)
            W.append(w)
            H.append(h)
            N.append(jj)
            cv2.rectangle(dimage, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(dimage, str(jj), (x + w//2, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow('Detected Boxes', dimage)
    print(N)
    return np.array(X), np.array(Y), W, H, N, w_avg, h_avg


# image_path = '/home/sts/Desktop/flipkart/image.jpeg'
#
# X, Y, W, H = box_it(image)


def where_bot(rx, ry, dimage, imageFrame, color):
    min_dist = 1e6
    for x, y, n, w, h in zip(X, Y, N, W, H):
        dist = (x - rx) ** 2 + (y - ry) ** 2
        if min_dist > dist:
            min_dist = dist
            xx = x
            yy = y
            ww = w
            hh = h
            nn = n

    # cv2.putText(dimage, 'X', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.rectangle(imageFrame, (xx, yy),
                  (xx + ww, yy + hh),
                  color, 2)
    cv2.imshow('frame', imageFrame)

    print('Robot at', nn)

    return nn


first_time = 1
while (1):

    _, image = webcam.read()
    imageFrame = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)

    # if first_time == 0:
    #     imageFrame = imageFrame[leastx:highestx, leasty:highesty]

    if first_time == 1:
        init_image = imageFrame
        X, Y, W, H, N, w_avg, h_avg = box_it(init_image)
        leastx = min(X)
        highestx = max(X)
        leasty = min(Y)
        highesty = max(Y)

        print('Image Captured!!')
        first_time = 0

    # Reading the video from the
    # webcam in image frames

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    red_lower = np.array([140, 0, 0], np.uint8)
    red_upper = np.array([180, 150, 100], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and
    # define mask
    green_lower = np.array([40, 50, 50], np.uint8)
    green_upper = np.array([80, 200, 150], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([100, 100, 0], np.uint8)
    blue_upper = np.array([140, 250, 150], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame,
                              mask=red_mask)

    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask=green_mask)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                               mask=blue_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            if (w / h < 2 and h / w < 2):
                cell = where_bot(x, y, init_image, imageFrame, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            if (w / h < 2 and h / w < 2):
                cell = where_bot(x, y, init_image, imageFrame, (0, 255, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            if (w / h < 2 and h / w < 2):
                cell = where_bot(x, y, init_image, imageFrame, (255, 0, 0))

    # Program Termination
    # cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break