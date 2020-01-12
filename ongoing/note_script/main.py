#!/usr/bin/env python3

from os import listdir
from dmenu_script import dmenu
from master import ROOT_DIR, Lectures


if __name__ == "__main__":
    courses = listdir(ROOT_DIR)
    courseSelected = dmenu('Select Course', courses)

    lectures = Lectures(courseSelected)

    lectureKey = dmenu('Select Lecture', lectures.lectureNumAndDatePath.keys())

    if 'new' in lectureKey:
        lectures.InitLecture()
    elif '00' in lectureKey:
        lectures.CompileMaster()
    else:
        lectureSelected = lectures.lectureNumAndDatePath[lectureKey]
        lectures.EditLecture(lectureSelected)
