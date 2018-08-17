# Check if victim is assigned to volunteer

# import serious stuff
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# setup essential variables
SCOPES = "https://www.googleapis.com/auth/spreadsheets"
RESCUE_SHEET_ID = "1womn9fd11hBCc3WFkxCf85WX6W9-Xcps7TvQZD57g9c"
RANGE = "number_sheet!A:A"


# check if assigned to a person
def check_if_assigned(phone_number):
    # setup API
    store = file.Storage("credentials.json")
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)

    service = build("sheets", "v4", http = creds.authorize(Http()))

    request = service.spreadsheets().values().get(spreadsheetId = RESCUE_SHEET_ID,
    range = RANGE)

    response = request.execute()

    for number in response["values"]:
        if number[0] == phone_number:
            return True

    return False
