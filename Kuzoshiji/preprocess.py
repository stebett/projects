# Reference to https://www.kaggle.com/christianwallenwein/visualization-yolo-labels-useful-functions

import os
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont
import shutil

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.inception_v3 import preprocess_input
from keras.utils.data_utils import GeneratorEnqueuer
import math
import regex as re


train_df = pd.read_csv('data/train.csv')
unicode_df = pd.read_csv('data/unicode_translation.csv')
#Save all the paths to vars
input_dir = Path("data/")
test_dir = input_dir/'test_images'
train_dir = input_dir/'train_images'

def toPath(string):
    if ".jpg" not in string:
        string = string + ".jpg"
    return string

def toID(string):
    if string[-4:] ==".jpg":
        string = string[:-4]
    return string

# In the training data, we get an entire string with all the characters in it and that needs to be splitted

# new list, every element is one char + all the information needed to create the bounding box
def splitEachChar(string):
    string = str(string)
    string = (re.findall(r"(?:\S*\s){5}", string))
    return [line[:-1]for line in string]

# new list, split everything by a blank
def splitEachInformation(string):
    string = str(string)
    string = string.split(" ")
    return string
        

unicode_map = {codepoint: char for codepoint, char in pd.read_csv(input_dir/'unicode_translation.csv').values}
unicode_list = list(unicode_map)

def unicodeToCharacter(unicode):
    return unicode_map[unicode]

# unicode to int conversion and the other way around
# unique identifier for every unicode character
def unicodeToInt(unicode):
    return unicode_list.index(unicode)

def intToUnicode(integer):
    return unicode_list[integer]


# returns the image size given the image_id or path to the image
def getImageSize(image):
    path = toPath(image)
    width, height = Image.open(train_dir/path).size
    return [width, height]

# add width and height of image to the df
train_widthheight = pd.DataFrame(train_df.image_id)
train_widthheight[["width", "height"]] = pd.DataFrame(train_widthheight["image_id"].apply(getImageSize).values.tolist(), columns=["width", "height"])

# first we split the labels into values
# then we use the stack method to combine all of the into single colum
yolo_labels = pd.DataFrame(train_df.labels.apply(splitEachChar).tolist(), index=train_df.image_id).stack()

# remove MultiIndex
yolo_labels = yolo_labels.reset_index([0, "image_id"])
yolo_labels.columns = ["image_id", "labels"]

# split labels into character, xmin, ymin, xwidht, yheight
yolo_labels[["unicode", "xmin", "ymin", "xsize", "ysize"]] = yolo_labels["labels"].str.split(' ', expand=True)

# remove labels
yolo_labels = yolo_labels.drop("labels", axis=1)

# change xwidth and yheight to xmax and ymax
yolo_labels["xsize"] = (yolo_labels["xmin"].astype("int32") + yolo_labels["xsize"].astype("int32")).astype("str")
yolo_labels["ysize"] = (yolo_labels["ymin"].astype("int32") + yolo_labels["ysize"].astype("int32")).astype("str")
yolo_labels.rename(columns={"xsize": "xmax", "ysize": "ymax"}, inplace=True)

# replace unicode character by integer
yolo_labels.unicode = yolo_labels.unicode.apply(unicodeToInt)
yolo_labels.rename(columns={"unicode": "class"}, inplace=True)

# add width and height to yolo_labels
yolo_labels = yolo_labels.merge(train_widthheight, how="left", on="image_id")

# display filename instead of image_id
yolo_labels.image_id = yolo_labels.image_id.apply(toPath)
yolo_labels.rename(columns={"image_id": "filename"}, inplace=True)

# rearrange columns
yolo_labels = yolo_labels[["filename", "class", "xmin", "ymin", "xmax", "ymax"]]
yolo_labels.head(1)
yolo_labels.to_csv('data/df_yolo.csv', index=False)

