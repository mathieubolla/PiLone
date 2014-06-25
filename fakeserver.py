from bottle import route, run
import time

@route('/')
def home():
    return {'tasks': [
        [time.time() + 5, 'http://localhost:8080/0/0/F00000/000000'],
        [time.time() + 5, 'http://localhost:8080/0/1/00F000/000000'],
        [time.time() + 5, 'http://localhost:8080/0/2/0000F0/000000'],
        [time.time() + 5, 'http://localhost:8080/0/3/FFFFFF/000000'],
        [time.time() + 15, 'http://localhost:8080/1/0/FFF000/000FFF'],
        ]}

@route('/:line/:led/:color1/:color2')
def fake_def(line, led, color1, color2):
    return {'data':[
        {'line': line, 'led': led, 'color1': color1, 'color2': color2},
        {'line': line, 'led': led, 'color1': color2, 'color2': color1}
    ]}

run(host='localhost', port=8080)