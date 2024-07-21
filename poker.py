import time
import datetime
import os
import re
from art import text2art, FONT_NAMES

# for f in FONT_NAMES:
#     print(f)
#     print(text2art('33:04 / break', font=f))
#     print(text2art('11:04 / break', font=f))
# exit()

INDENT = '  '
FONT = 'univers'
SECONDS_PER_LEVEL = 10 * 60
LEVELS = [
    # { 'type': 'blinds',   'small': 100,     'big': 200,      'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'break',                                       'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'blinds',   'small': 200,     'big': 400,      'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'blinds',   'small': 300,     'big': 600,      'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'blinds',   'small': 500,     'big': 1000,     'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'blinds',   'small': 800,     'big': 1600,     'duration': SECONDS_PER_LEVEL  },
    # { 'type': 'blinds',   'small': 1000,    'big': 2000,     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 2000,    'big': 4000,     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 4000,    'big': 8000,     'duration': SECONDS_PER_LEVEL  },
]

def format_seconds(secs):
    s = str(datetime.timedelta(seconds=secs))
    return re.sub(r'^0:', '', s)

def format_level_display(level):
    if level['type'] == 'blinds':
        return [
            f'{INDENT}S: {level['small']}',
            f'{INDENT}B: {level['big']}'
        ]
    elif level['type'] == 'break':
        return [f'{INDENT}Break']
    else:
        raise Exception('Unknown level type')

def format_level_speech(level):
    if level['type'] == 'blinds':
        return f'{level['small']}, {level['big']}'
    elif level['type'] == 'break':
        return 'Break time'
    else:
        raise Exception('Unknown level type')

def main():
    level = 0
    time_passed = 0

    while True:
        time.sleep(1)
        duration = LEVELS[level]['duration']

        print('\n' * 25)
        time_msg = f'{INDENT}{format_seconds(time_passed)} / {format_seconds(duration)}'
        print(text2art(time_msg, font=FONT))
        for line in format_level_display(LEVELS[level]):
            print(text2art(line, font=FONT))
        print('\n' * 3)

        time_passed = time_passed + 1
        time_left = SECONDS_PER_LEVEL - time_passed

        if time_passed == 1 or time_passed == 6:
            os.system(f'say "the current stage is {format_level_speech(LEVELS[level])}" &')
        elif time_left >= 0 and time_left <= 4:
            os.system(f'say "{time_left + 1}" &')

        if time_passed == SECONDS_PER_LEVEL:
            level = level + 1
            time_passed = 0

if __name__ == "__main__":
    main()
