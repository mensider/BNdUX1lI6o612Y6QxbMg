# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:34:42 2022

@author: HP
"""

import numpy as np
import cv2

# Capturing video through webcam=0
# please replace (0) by "IPWEBCAM ip address" to test on live phone video
webcam = cv2.VideoCapture("http://192.168.43.1:8080/video")
#webcam = cv2.VideoCapture(0)
while (1):

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and
    # # define mask
    # green_lower = np.array([65, 60, 60], np.uint8)
    # green_upper = np.array([80, 255, 255], np.uint8)
    green_lower = np.array([50, 80, 111], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    # Set range for blue color and
    # define mask
    blue_lower = np.array([90, 80, 111], np.uint8)
    blue_upper = np.array([130, 255, 255], np.uint8)
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
    # errorx=50;
    # errory=150;
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     Bluerow =0;Bluecol=0;Redcol=0;Redrow=0;Greencol=0;Greenrow=0;
    #     if (area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         imageFrame = cv2.rectangle(imageFrame, (x, y),
    #                                    (x + w, y + h),
    #                                    (0, 0, 255), 2)
    #
    #         cv2.putText(imageFrame, 'RedBot x=' + str(x) + 'y=' + str(y), (x, y),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #                     (0, 0, 255))
    #         bot1x = x+errorx;
    #         bot1y = y+errory;
    #         print(bot1x, bot1y);
    #         if (bot1x < 86):
    #             Redcol = '1';
    #         elif(bot1x < 138):
    #             Redcol = '2';
    #         elif(bot1x < 160):
    #             Redcol = '3';
    #         elif(bot1x < 241):
    #             Redcol = '4';
    #         elif(bot1x < 298):
    #             Redcol = '5';
    #         elif(bot1x < 351):
    #             Redcol = '6';
    #         elif(bot1x < 407):
    #             Redcol = '7';
    #         elif(bot1x < 462):
    #             Redcol = '8';
    #         elif(bot1x < 515):
    #             Redcol = '9';
    #         elif(bot1x < 572):
    #             Redcol = '10';
    #         elif(bot1x < 627):
    #             Redcol = '11';
    #         elif(bot1x < 684):
    #             Redcol = '12';
    #         elif(bot1x < 743):
    #             Redcol = '13';
    #         elif(bot1x < 798):
    #             Redcol = '14';
    #
    #         if (bot1y > 697):
    #             Redrow = 'a';
    #         elif(bot1y > 651):
    #             Redrow = 'b';
    #         elif(bot1y > 597):
    #             Redrow = 'c';
    #         elif(bot1y > 545):
    #             Redrow = 'd';
    #         elif(bot1y > 492):
    #             Redrow = 'e';
    #         elif(bot1y > 435):
    #             Redrow = 'f';
    #         elif(bot1y > 381):
    #             Redrow = 'g';
    #         elif(bot1y > 397):
    #             Redrow = 'h';
    #         elif(bot1y > 270):
    #             Redrow = 'i';
    #         elif(bot1y > 214):
    #             Redrow = 'j';
    #         elif(bot1y > 157):
    #             Redrow = 'k';
    #         elif(bot1y > 101):
    #             Redrow = 'l';
    #         elif(bot1y > 45):
    #             Redrow = 'm';
    #         elif(bot1y > 9):
    #             Redrow = 'n';
    #         print('Red bot in row,col');
    #         red_bot_pos = [Redrow, Redcol];
    #         print(red_bot_pos);

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         x1, y1, wg, hg = cv2.boundingRect(contour)
    #         imageFrame = cv2.rectangle(imageFrame, (x1, y1),
    #                                    (x1 + wg, y1 + hg),
    #                                    (0, 255, 0), 2)
    #         cv2.putText(imageFrame, 'GreenBot x=' + str(x1) + 'y=' + str(y1), (x1, y1),
    #                     cv2.FONT_HERSHEY_SIMPLEX,
    #                     1.0, (0, 255, 0))
    #
    #         bot2x = x1;
    #         bot2y = y1;
    #
    #         if (bot2x < 86):
    #            Greencol = '1';
    #         elif(bot2x < 138):
    #            Greencol = '2';
    #         elif(bot2x < 193):
    #            Greencol = '3';
    #         elif(bot2x < 241):
    #            Greencol = '4';
    #         elif(bot2x < 298):
    #            Greencol = '5';
    #         elif(bot2x < 351):
    #            Greencol = '6';
    #         elif(bot2x < 407):
    #            Greencol = '7';
    #         elif(bot2x < 462):
    #            Greencol = '8';
    #         elif(bot2x < 515):
    #            Greencol = '9';
    #         elif(bot2x < 572):
    #            Greencol = '10';
    #         elif(bot2x < 627):
    #            Greencol = '11';
    #         elif(bot2x < 684):
    #            Greencol = '12';
    #         elif(bot2x < 743):
    #            Greencol = '13';
    #         elif(bot2x < 798):
    #            Greencol = '14';
    #
    #         if (bot2y > 697):
    #            Greenrow = 'a';
    #         elif(bot2y > 651):
    #            Greenrow = 'b';
    #         elif(bot2y > 597):
    #            Greenrow = 'c';
    #         elif(bot2y > 545):
    #            Greenrow = 'd';
    #         elif(bot2y > 492):
    #            Greenrow = 'e';
    #         elif(bot2y > 435):
    #            Greenrow = 'f';
    #         elif(bot2y > 381):
    #            Greenrow = 'g';
    #         elif(bot2y > 397):
    #            Greenrow = 'h';
    #         elif(bot2y > 270):
    #            Greenrow = 'i';
    #         elif(bot2y > 214):
    #            Greenrow = 'j';
    #         elif(bot2y > 157):
    #            Greenrow = 'k';
    #         elif(bot2y > 101):
    #            Greenrow = 'l';
    #         elif(bot2y > 45):
    #            Greenrow = 'm';
    #         elif(bot2y > 9):
    #            Greenrow = 'n';
    #         print('Green bot in row,col');
    #         Green_bot_pos = [Greenrow, Greencol];
    #         print(Green_bot_pos);

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if (area > 300):
    #         xb, yb, wb, hb = cv2.boundingRect(contour)
    #         imageFrame = cv2.rectangle(imageFrame, (xb, yb),
    #                                    (xb + wb, yb + hb),
    #                                    (255, 0, 0), 2)
    #
    #         cv2.putText(imageFrame, 'BlueBot x=' + str(xb) + 'y=' + str(yb), (xb, yb),
    #                     cv2.FONT_HERSHEY_SIMPLEX,
    #                     1.0, (255, 0, 0))
    #
    #         bot3x = xb;
    #         bot3y = yb;
    #
    #         if (bot3x < 86):
    #             Bluecol = '1';
    #         elif(bot3x < 138):
    #             Bluecol = '2';
    #         elif(bot3x < 193):
    #             Bluecol = '3';
    #         elif(bot3x < 241):
    #             Bluecol = '4';
    #         elif(bot3x < 298):
    #             Bluecol = '5';
    #         elif(bot3x < 351):
    #             Bluecol = '6';
    #         elif(bot3x < 407):
    #             Bluecol = '7';
    #         elif(bot3x < 462):
    #             Bluecol = '8';
    #         elif(bot3x < 515):
    #             Bluecol = '9';
    #         elif(bot3x < 572):
    #             Bluecol = '10';
    #         elif(bot3x < 627):
    #             Bluecol = '11';
    #         elif(bot3x < 684):
    #             Bluecol = '12';
    #         elif(bot3x < 743):
    #             Bluecol = '13';
    #         elif(bot3x < 798):
    #             Bluecol = '14';
    #
    #
    #         if (bot3y > 697):
    #             Bluerow = 'a';
    #         elif(bot3y > 651):
    #             Bluerow = 'b';
    #         elif(bot3y > 597):
    #             Bluerow = 'c';
    #         elif(bot3y > 545):
    #             Bluerow = 'd';
    #         elif(bot3y > 492):
    #             Bluerow = 'e';
    #         elif(bot3y > 435):
    #             Bluerow = 'f';
    #         elif(bot3y > 381):
    #             Bluerow = 'g';
    #         elif(bot3y > 397):
    #             Bluerow = 'h';
    #         elif(bot3y > 270):
    #             Bluerow = 'i';
    #         elif(bot3y > 214):
    #             Bluerow = 'j';
    #         elif(bot3y > 157):
    #             Bluerow = 'k';
    #         elif(bot3y > 101):
    #             Bluerow = 'l';
    #         elif(bot3y > 45):
    #             Bluerow = 'm';
    #         elif(bot3y > 9):
    #             Bluerow = 'n';
    #     print('Blue bot in row,col');
    #     Blue_bot_pos = [Bluerow, Bluecol];
    #     print(Blue_bot_pos);

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break