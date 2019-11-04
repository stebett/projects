import datetime
from calendar_reader import dict_scheduled
from note_reader import find_dates


def read_last_time():
    with open('.last_time', 'r') as f:
        last_time = f.read()
    return last_time


def write_time():
    with open('.last_time', 'w') as f:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        f.write(now)


def diff():
    sched = dict_scheduled(start_time=read_last_time())
    subjects = list(sched.keys())

    taken = {subj: find_dates(subj+'/') for subj in subjects}

    diff_dict = {}
    for s in subjects:
        diff = set(sched[s]).difference(set(taken[s]))
        diff_dict[s] = diff

    return diff_dict


def write_task():
    # This has to take diff and write tasks
    diff_dict = diff()
    return diff_dict


def main():
    write_task()
    write_time()
