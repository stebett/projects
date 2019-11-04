from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def dict_scheduled(start_time):
    ####################
    creds = None
    if os.path.exists('cal_api/token.pickle'):
        with open('cal_api/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cal_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('cal_api/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    ####################

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC tim

    calendar_list_result = service.calendarList().list().execute()
    cal_1_name = calendar_list_result['items'][0]['summary']
    cal_2_name = calendar_list_result['items'][1]['summary']
    cal_1_id = calendar_list_result['items'][0]['id']
    cal_2_id = calendar_list_result['items'][1]['id']
    cal_dict = {cal_1_name: cal_1_id, cal_2_name: cal_2_id}

    events_result = service.events().list(calendarId=cal_dict['Lezioni Ste '],
                                          timeMin=start_time,
                                          timeMax=now,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_list = []
    name_list = []
    for event in events:
        date = event['start']['dateTime'][:10]
        name = event['summary']
        if name not in name_list:
            name_list.append(name)
        event_list.append((name, date))

    event_dict = {i: [] for i in name_list}

    for couple in event_list:
        event_dict[couple[0]].append(couple[1])

    return event_dict


if __name__ == "__main__":
    print(dict_scheduled())
