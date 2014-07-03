__author__ = 'mathieubolla'

import time

current_secs = time.time()
current = time.localtime(time.time())
print current

next = time.mktime((current[0], current[1], current[2], 22, 12, 0, current[6], current[7], current[8]))

print next - current_secs

remaining_minutes = (next - current_secs) // 60

print remaining_minutes

white = "FFFFFF"
black = "000000"

print {'data':[
        {'line': 0, 'led': 0, 'color1': white if remaining_minutes <= 5 else black, 'color2': white if remaining_minutes <= 5 else black},
        {'line': 0, 'led': 1, 'color1': white if remaining_minutes <= 4 else black, 'color2': white if remaining_minutes <= 4 else black},
        {'line': 0, 'led': 2, 'color1': white if remaining_minutes <= 3 else black, 'color2': white if remaining_minutes <= 3 else black},
        {'line': 0, 'led': 3, 'color1': white if remaining_minutes <= 2 else black, 'color2': white if remaining_minutes <= 2 else black},
        {'line': 0, 'led': 4, 'color1': white if remaining_minutes <= 1 else black, 'color2': white if remaining_minutes <= 1 else black},
        {'line': 0, 'led': 5, 'color1': black, 'color2': black},
        {'line': 0, 'led': 6, 'color1': black, 'color2': black},
        {'line': 0, 'led': 7, 'color1': black, 'color2': black},
    ]}