import pandas as pd

unicode_map = {codepoint: char for codepoint, char in pd.read_csv('data/unicode_translation.csv').values}
unicode_list = list(unicode_map)

def unicodeToInt(unicode):
    return unicode_list.index(unicode)

class_file = {uc:unicodeToInt(uc) for uc in unicode_list}
f = open('data/class_file.txt', 'w')
for i in class_file:
    f.write(i + '\n')
