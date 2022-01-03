import os
import flask
from flask import jsonify
from werkzeug.utils import secure_filename
import json
import numpy as np
import cv2
from imutils import contours
port = 5100
app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    file = flask.request.files['filename']
    filename = secure_filename(file.filename)
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, "uploads/", filename)
    file.save(path)
    if os.path.isfile(path):
        image = cv2.imread(path)
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3,3), 0)
        canny = cv2.Canny(blurred, 120, 255, 1)
        charachters_files = []
        charachters_files_bw = []
        # Find contours
        contour_list = []
        detected_character_counter = 0
        cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts, _ = contours.sort_contours(cnts, method="left-to-right")
        for index, contour in enumerate(cnts):
            # Obtain bounding rectangle for each contour
            # When rectangles are nested
            x,y,w,h = cv2.boundingRect(contour)
            # When current rectangle is nested in rectangle before
            if h * w > 170:
                # When current rectangle is nested in rectangle before
                if index != 0:
                    x2, y2, w2, h2 = cv2.boundingRect(cnts[index-1])
                    difference_x = abs(x - x2)
                    if difference_x < 5 and w2 > w:
                        continue 
                # When current rectangle is nested next rectangle 
                if  index != len(cnts) - 1:
                    x2, y2, w2, h2 = cv2.boundingRect(cnts[index+1])
                    difference_x = (x2 - x)
                    if difference_x < 5 and w2 > w:
                        continue
                cropped_image = image[y:y+h, x:x+w]
            cropped_image_copy = original[y:y+h, x:x+w]
            # Draw bounding box rectangle, crop using Numpy slicing
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
            path2 = os.path.join(basedir, "uploads/", "character_{}.png".format(detected_character_counter))
            cv2.imwrite(path2, cropped_image_copy)
            im_gray = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)     
            (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
            thresh = 133
            im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
            path3 = os.path.join(basedir, "uploads/", "character_bw_{}.png".format(detected_character_counter))
            cv2.imwrite(path3, im_bw)
            charachters_files.append(path2)
            charachters_files_bw.append(path3)
            detected_character_counter += 1
        return jsonify(message="Image Uploaded Successfully",status=200)
    else:
        return jsonify(message="ERROR",status=200)
    
