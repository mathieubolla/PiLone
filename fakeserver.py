from bottle import route, run
import time

white = "FFFFFF"
black = "000000"

@route('/')
def home():
    return {'tasks': [
        [time.time() + 15, 'http://pilone/chrono/0/12/00']
    ]}

@route('/arbitrary/:line/:led/:color1/:color2')
def fake_def(line, led, color1, color2):
    return {'data':[
        {'line': line, 'led': led, 'color1': color1, 'color2': color2},
        {'line': line, 'led': led, 'color1': color2, 'color2': color1}
    ]}

@route('/chrono/:line/:hour/:minute')
def chono_app(line, hour, minute):
    current_secs = time.time()

    current_time = time.localtime(time.time())
    next_secs = time.mktime((current_time[0], current_time[1], current_time[2], int(hour), int(minute), 0, current_time[6], current_time[7], current_time[8]))

    remaining_minutes = (next_secs - current_secs) // 60

    if (remaining_minutes < 0) & (remaining_minutes > -5):
        return {'data':[
            {'line': line, 'led': 0, 'color1': white, 'color2': black},
            {'line': line, 'led': 1, 'color1': white, 'color2': black},
            {'line': line, 'led': 2, 'color1': white, 'color2': black},
            {'line': line, 'led': 3, 'color1': white, 'color2': black},
            {'line': line, 'led': 4, 'color1': white, 'color2': black},
            {'line': line, 'led': 5, 'color1': black, 'color2': black},
            {'line': line, 'led': 6, 'color1': black, 'color2': black},
            {'line': line, 'led': 7, 'color1': black, 'color2': black},
        ]}

    if (remaining_minutes > 5) | (remaining_minutes <= -5):
        return {'data':[
            {'line': line, 'led': 0, 'color1': black, 'color2': black},
            {'line': line, 'led': 1, 'color1': black, 'color2': black},
            {'line': line, 'led': 2, 'color1': black, 'color2': black},
            {'line': line, 'led': 3, 'color1': black, 'color2': black},
            {'line': line, 'led': 4, 'color1': black, 'color2': black},
            {'line': line, 'led': 5, 'color1': black, 'color2': black},
            {'line': line, 'led': 6, 'color1': black, 'color2': black},
            {'line': line, 'led': 7, 'color1': black, 'color2': black},
        ]}

    return {'data':[
            {'line': line, 'led': 0, 'color1': white if remaining_minutes <= 5 else black, 'color2': white if remaining_minutes <= 5 else black},
            {'line': line, 'led': 1, 'color1': white if remaining_minutes <= 4 else black, 'color2': white if remaining_minutes <= 4 else black},
            {'line': line, 'led': 2, 'color1': white if remaining_minutes <= 3 else black, 'color2': white if remaining_minutes <= 3 else black},
            {'line': line, 'led': 3, 'color1': white if remaining_minutes <= 2 else black, 'color2': white if remaining_minutes <= 2 else black},
            {'line': line, 'led': 4, 'color1': white if remaining_minutes <= 1 else black, 'color2': white if remaining_minutes <= 1 else black},
            {'line': line, 'led': 5, 'color1': black, 'color2': black},
            {'line': line, 'led': 6, 'color1': black, 'color2': black},
            {'line': line, 'led': 7, 'color1': black, 'color2': black},
        ]}

run(host='localhost', port=8080)