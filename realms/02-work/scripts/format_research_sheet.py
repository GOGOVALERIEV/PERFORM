import pickle
from googleapiclient.discovery import build

with open('config/google-token.pickle', 'rb') as f:
    creds = pickle.load(f)

sheets = build('sheets', 'v4', credentials=creds)
sheet_id = open('config/research_template_id.txt').read().strip()

spreadsheet = sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()
ws_id = spreadsheet['sheets'][0]['properties']['sheetId']

def rgb(r, g, b):
    return {'red': r/255, 'green': g/255, 'blue': b/255}

requests = []

# Column widths
col_widths = [(0,1,200),(1,2,180),(2,3,250),(3,4,180),(4,5,180),(5,6,180),(6,7,300)]
for start, end, width in col_widths:
    requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': ws_id, 'dimension': 'COLUMNS', 'startIndex': start, 'endIndex': end},
            'properties': {'pixelSize': width},
            'fields': 'pixelSize'
        }
    })

# Header row - dark green, white bold
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 7},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(56, 118, 29),
                'textFormat': {'bold': True, 'foregroundColor': rgb(255, 255, 255), 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
                'verticalAlignment': 'MIDDLE'
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)'
    }
})

# Dropdown columns light green tint (D, E, F)
for col in [3, 4, 5]:
    requests.append({
        'repeatCell': {
            'range': {'sheetId': ws_id, 'startRowIndex': 1, 'endRowIndex': 15, 'startColumnIndex': col, 'endColumnIndex': col + 1},
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': rgb(217, 234, 211),
                }
            },
            'fields': 'userEnteredFormat(backgroundColor)'
        }
    })

# Yellow reference area (rows 16-36)
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 15, 'endRowIndex': 36, 'startColumnIndex': 0, 'endColumnIndex': 7},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(255, 249, 196),
            }
        },
        'fields': 'userEnteredFormat(backgroundColor)'
    }
})

# Desire Magnitude Scale header (row 22) - bold
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 21, 'endRowIndex': 22, 'startColumnIndex': 0, 'endColumnIndex': 1},
        'cell': {
            'userEnteredFormat': {
                'textFormat': {'bold': True, 'fontSize': 11},
                'backgroundColor': rgb(255, 249, 196),
            }
        },
        'fields': 'userEnteredFormat(textFormat,backgroundColor)'
    }
})

# Desire table headers (row 23) - green bold
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 22, 'endRowIndex': 23, 'startColumnIndex': 0, 'endColumnIndex': 3},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(147, 196, 125),
                'textFormat': {'bold': True},
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
    }
})

# Desire table data (rows 24-26) - light green
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 23, 'endRowIndex': 26, 'startColumnIndex': 0, 'endColumnIndex': 3},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(217, 234, 211),
            }
        },
        'fields': 'userEnteredFormat(backgroundColor)'
    }
})

# Awareness Scale header (row 30) - bold
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 29, 'endRowIndex': 30, 'startColumnIndex': 0, 'endColumnIndex': 1},
        'cell': {
            'userEnteredFormat': {
                'textFormat': {'bold': True, 'fontSize': 11},
                'backgroundColor': rgb(255, 249, 196),
            }
        },
        'fields': 'userEnteredFormat(textFormat,backgroundColor)'
    }
})

# Awareness table headers (row 31) - green bold
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 30, 'endRowIndex': 31, 'startColumnIndex': 0, 'endColumnIndex': 4},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(147, 196, 125),
                'textFormat': {'bold': True},
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
    }
})

# Awareness table data (rows 32-36) - light green
requests.append({
    'repeatCell': {
        'range': {'sheetId': ws_id, 'startRowIndex': 31, 'endRowIndex': 36, 'startColumnIndex': 0, 'endColumnIndex': 4},
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': rgb(217, 234, 211),
            }
        },
        'fields': 'userEnteredFormat(backgroundColor)'
    }
})

# Borders for reference tables
for table in [(22, 26, 0, 3), (30, 36, 0, 4)]:
    requests.append({
        'updateBorders': {
            'range': {'sheetId': ws_id, 'startRowIndex': table[0], 'endRowIndex': table[1], 'startColumnIndex': table[2], 'endColumnIndex': table[3]},
            'top': {'style': 'SOLID', 'width': 1},
            'bottom': {'style': 'SOLID', 'width': 1},
            'left': {'style': 'SOLID', 'width': 1},
            'right': {'style': 'SOLID', 'width': 1},
            'innerHorizontal': {'style': 'SOLID', 'width': 1},
            'innerVertical': {'style': 'SOLID', 'width': 1},
        }
    })

# Borders for main table
requests.append({
    'updateBorders': {
        'range': {'sheetId': ws_id, 'startRowIndex': 0, 'endRowIndex': 15, 'startColumnIndex': 0, 'endColumnIndex': 7},
        'top': {'style': 'SOLID', 'width': 1},
        'bottom': {'style': 'SOLID', 'width': 1},
        'left': {'style': 'SOLID', 'width': 1},
        'right': {'style': 'SOLID', 'width': 1},
        'innerHorizontal': {'style': 'SOLID', 'width': 1},
        'innerVertical': {'style': 'SOLID', 'width': 1},
    }
})

# Data validation: Desire magnetitude (column D)
requests.append({
    'setDataValidation': {
        'range': {'sheetId': ws_id, 'startRowIndex': 1, 'endRowIndex': 15, 'startColumnIndex': 3, 'endColumnIndex': 4},
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': 'Low'}, {'userEnteredValue': 'Medium'}, {'userEnteredValue': 'High'}]
            },
            'showCustomUi': True,
            'strict': True
        }
    }
})

# Data validation: Awareness Level (column E)
requests.append({
    'setDataValidation': {
        'range': {'sheetId': ws_id, 'startRowIndex': 1, 'endRowIndex': 15, 'startColumnIndex': 4, 'endColumnIndex': 5},
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [
                    {'userEnteredValue': 'Unaware'},
                    {'userEnteredValue': 'Problem-Aware'},
                    {'userEnteredValue': 'Solution-Aware'},
                    {'userEnteredValue': 'Product-Aware'},
                    {'userEnteredValue': 'Most Aware'}
                ]
            },
            'showCustomUi': True,
            'strict': True
        }
    }
})

# Data validation: Competition level (column F)
requests.append({
    'setDataValidation': {
        'range': {'sheetId': ws_id, 'startRowIndex': 1, 'endRowIndex': 15, 'startColumnIndex': 5, 'endColumnIndex': 6},
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': 'Low'}, {'userEnteredValue': 'Medium'}, {'userEnteredValue': 'High'}]
            },
            'showCustomUi': True,
            'strict': True
        }
    }
})

# Freeze row 1
requests.append({
    'updateSheetProperties': {
        'properties': {
            'sheetId': ws_id,
            'gridProperties': {'frozenRowCount': 1}
        },
        'fields': 'gridProperties.frozenRowCount'
    }
})

sheets.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={'requests': requests}).execute()
print('Formatting done!')
