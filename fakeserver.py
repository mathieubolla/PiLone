from bottle import route, run
import time

white = "FFFFFF"
black = "000000"
orange = "DD5E00"
blue = "0000FF"
light_blue = "000090"
red = "FF0000"

@route('/')
def home():
    current = time.localtime(time.time())

    # From 22h00 to 6h50, only display chrono on line 0
    if (current[3] > 22) | ((current[3] < 6) & (current[4] < 50)):
        return {'tasks': [
            [time.time() + 15, 'http://pilone/chrono/0/12/00']
        ]}
    else:
    # From 6h50 to 22h00, also display meteo on line 1
        return {'tasks': [
            [time.time() + 5, 'http://pilone/meteo/1/3021000'],
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
            {'line': line, 'led': 7, 'color1': red, 'color2': red},
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
            {'line': line, 'led': 7, 'color1': red, 'color2': red},
        ]}


def read_from_url(url):
    import urllib2

    value = None

    while value == None:
        try:
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            value = resp.read()
        except urllib2.URLError:
            pass

    import json
    from StringIO import StringIO

    return json.load(StringIO(value))

@route('/meteo/:line/:city_id')
def get_meteo_data(line, city_id):
    url = 'http://api.openweathermap.org/data/2.5/history/city?id='+city_id+'&type=hour&start=' + str(
        time.time() - time.timezone - 24 * 3600) + '&cnt=1'

    weather_history = read_from_url(url)
    weather_current = read_from_url('http://api.openweathermap.org/data/2.5/weather?id='+city_id)
    weather_forecast = read_from_url('http://api.openweathermap.org/data/2.5/forecast/daily?id='+city_id+'&cnt=1')['list'][0]

    temp_celsius_history = float(weather_history['list'][0]['main']['temp']) - 273.15
    temp_celsius_current = float(weather_current['main']['temp']) - 273.15

    # As defined here : http://pluiesextremes.meteo.fr/intensite-de-precipitations---equivalence-entre-millimetres-de-pluie-et-volumes-d-eau-precipites_r67.html
    rain_intensity_table = {
        0:0,
        1:1, 2:1, 3:1,
        4:2, 5:2, 6:1, 7:1,
        }

    rain_mm_forecast = 0
    if ('rain' in weather_forecast):
        rain_mm_forecast = weather_forecast['rain']

    try:
        rain_intensity_forecast = rain_intensity_table[int(rain_mm_forecast)]
    except:
        rain_intensity_forecast = 4

    delta = int(temp_celsius_current - temp_celsius_history)

    delta_color_1 = red if delta > 0 else blue if delta < 0 else black
    delta_color_2 = delta_color_1 if abs(delta) < 2 else black # blink to black if delta over 2

    return {'data':[
                {'line': line, 'led': 0, 'color1': delta_color_1, 'color2': delta_color_2},
                {'line': line, 'led': 1, 'color1': delta_color_1 if abs(delta) > 0 else black, 'color2': delta_color_2 if abs(delta) > 0 else black},
                {'line': line, 'led': 2, 'color1': delta_color_1 if abs(delta) > 1 else black, 'color2': delta_color_2 if abs(delta) > 1 else black},
                {'line': line, 'led': 3, 'color1': blue if rain_intensity_forecast > 3 else black, 'color2': black},
                {'line': line, 'led': 4, 'color1': blue if rain_intensity_forecast > 2 else black, 'color2': light_blue if rain_intensity_forecast > 2 else black},
                {'line': line, 'led': 5, 'color1': blue if rain_intensity_forecast > 1 else black, 'color2': light_blue if rain_intensity_forecast > 1 else black},
                {'line': line, 'led': 6, 'color1': blue if rain_intensity_forecast > 0 else black, 'color2': light_blue if rain_intensity_forecast > 0 else black},
                {'line': line, 'led': 7, 'color1': orange, 'color2': orange},
            ]}

run(host='localhost', port=8080)