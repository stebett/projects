from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    start_time = datetime.datetime(
        2019, 11, 1, 12, 00, 00, 100005).isoformat() + 'Z'
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
    for event in events:
        start = event['start']['dateTime'][:10]
        print(start, event['summary'])

if __name__ == '__main__':
    main()
