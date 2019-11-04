from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']


def write_task(dict_):
    ####################
    creds = None
    if os.path.exists('task_api/token.pickle'):
        with open('task_api/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'task_api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('task_api/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)
    ####################
    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    list_dict = {item['title']: item['id'] for item in items}

    dict_keys = list(dict_.keys())
    for key in dict_keys:
        for task in dict_[key]:
            if key == "Lavoro":
                body = {"title": 'questo va sistemato',
                        "notes": task}
            else:
                body = {"title": 'Recupero Lezione del ' + task}

            _ = service.tasks().insert(
                tasklist=list_dict[key], body=body).execute()
