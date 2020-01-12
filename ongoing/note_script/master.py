from pathlib import Path
from re import match
from subprocess import Popen


ROOT_DIR = Path('~/Courses').expanduser()


class Lectures():
    def __init__(self, selectedCourse):
        self.coursePath = ROOT_DIR / selectedCourse
        self.lecturesPaths = self.GetLectures()
        self.lectureNumAndDatePath = self.CreateDict()

    def GetLectures(self):
        lecturesPaths = sorted(f for f in self.coursePath.glob('*.tex'))

        return lecturesPaths

    def CreateDict(self):
        lectureNumAndDatePath = {}
        for path in self.lecturesPaths:
            lectureNum = getLectureNumber(path)
            lectureDate = getLectureDate(path)

            lectureNumAndDatePath["Lecture {}".format(lectureNum) +
                                  lectureDate.rjust(164)] = path

        return lectureNumAndDatePath

    def EditLecture(self, lecturePath):
        Popen(['st', '-e', 'bash', '-i', '-c', 'nvim ' + str(lecturePath)])

    def InitLecture(self):
        Num = len(self.lecturesPaths)
        Path = self.coursePath / 'lec_{0:02d}.tex'.format(Num)

        Popen(['st', '-e', 'bash', '-i', '-c',
            'nvim {} "+:normal ihead\t"'.format(str(Path))])

    # def CompileMaster(self):


def getLectureDate(lecturePath):
    with lecturePath.open() as f:
        for line in f:
            dateMatch = match(r'\\date\{(.*)\}', line)
            if dateMatch:
                break
    try:
        date = dateMatch.group(1)
    except Exception:
        date = '29 Febbraio 2020'

    return date


def getLectureNumber(lecturePath):
    return (str(lecturePath.stem).replace('.tex', '')
                                 .replace('lec_', '')
                                 .replace('master', '00'))


def getLectureFromNumber(lectureNumber):
    return 'lec_{0:02d}.tex'.format(lectureNumber)
