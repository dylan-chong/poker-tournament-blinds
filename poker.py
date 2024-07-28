import argparse
import time
import datetime
import os
import re
from art import text2art

# Uncomment to print fonts
# from art import FONT_NAMES
# for f in FONT_NAMES:
#     print(f)
#     print(text2art('33:04 / break', font=f))
#     print(text2art('11:04 / break', font=f))
# exit()


# Turbo 2h with cash chips
SECONDS_PER_LEVEL = 10 * 60
_LEVELS = [
    { 'type': 'blinds',   'small': 1,       'big': 1,        'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 1,       'big': 2,        'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 2,       'big': 3,        'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 3,       'big': 6,        'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 5,       'big': 10,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 8,       'big': 15,       'duration': SECONDS_PER_LEVEL  },

    { 'type': 'break',    'message': 'Break time',           'duration': 180  },
    { 'type': 'blinds',   'small': 10,      'big': 25,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 15,      'big': 30,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 25,      'big': 50,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 40,      'big': 80,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 50,      'big': 100,      'duration': SECONDS_PER_LEVEL  },
]

# 3h tournament with cash chips
SECONDS_PER_LEVEL = 15 * 60
LEVELS = [
    { 'type': 'blinds',   'small': 1,       'big': 1,             'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 1,       'big': 2,             'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 2,       'big': 4,             'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 3,       'big': 6,             'duration': SECONDS_PER_LEVEL  },

    { 'type': 'break',    'message': 'Break,\n  No more re-buys', 'duration': 5 * 60             },
    { 'type': 'blinds',   'small': 5,       'big': 10,            'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 8,       'big': 15,            'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 10,      'big': 20,            'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 15,      'big': 30,            'duration': SECONDS_PER_LEVEL  },

    { 'type': 'break',    'message': 'Break',                     'duration': 5 * 60             },
    { 'type': 'blinds',   'small': 25,      'big': 50,            'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 40,      'big': 80,            'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 50,      'big': 100,           'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 100,     'big': 200,           'duration': SECONDS_PER_LEVEL  },
]

# 3h tournament
SECONDS_PER_LEVEL = 12 * 60
_LEVELS = [
    { 'type': 'blinds',   'small': 25,      'big': 50,       'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 50,      'big': 100,      'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 100,     'big': 200,      'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 200,     'big': 400,      'duration': SECONDS_PER_LEVEL  },
    { 'type': 'break',    'message': 'Break time',           'duration': SECONDS_PER_LEVEL  },

    { 'type': 'blinds',   'small': 300,     'big': 600,      'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 500,     'big': 1000,     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 800,     'big': 1600,     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': '1K',    'big': '2K',     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'break',    'message': 'Break time',           'duration': SECONDS_PER_LEVEL  },

    { 'type': 'blinds',   'small': 1500,    'big': '3K',     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': 2500,    'big': '5K',     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': '4K',    'big': '8K',     'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': '6K',    'big': '12K',    'duration': SECONDS_PER_LEVEL  },
    { 'type': 'blinds',   'small': '10K',   'big': '20K',    'duration': SECONDS_PER_LEVEL  },

    { 'type': 'blinds',   'small': '20K',   'big': '40K',    'duration': SECONDS_PER_LEVEL  },
]

START_LEVEL = 0
START_TIME_PASSED = 0

INDENT = '  '
FONT = 'univers'

def format_seconds(secs):
    s = str(datetime.timedelta(seconds=secs))
    return re.sub(r'^0:', '', s)

def format_level_display(level, prefix):
    if level['type'] == 'blinds':
        return [
            f'{INDENT}{prefix}{level['small']} / {level['big']}',
        ]
    elif level['type'] == 'break':
        return [f'{INDENT}{prefix}{level['message']}']
    else:
        raise Exception('Unknown level type')

def format_level_speech(level):
    if level['type'] == 'blinds':
        return f'{level['small']}, {level['big']}'
    elif level['type'] == 'break':
        return level['message']
    else:
        raise Exception('Unknown level type')

def speak(message, program_args):
    if "'" in message:
        raise ValueError("String contains a single quote!")
    speech_command = program_args.speech_command
    if not speech_command:
        return
    os.system(f"{speech_command} '{message}' &")

def display_state(time_left, duration, level, next_level):
    print('\n' * 25)
    time_msg = f'{INDENT}{format_seconds(time_left)} / {format_seconds(duration)}'
    print(text2art(time_msg, font=FONT))
    for line in format_level_display(level, 'Blinds: '):
        print(text2art(line, font=FONT))
    print('\n' * 6)
    if next_level:
        for line in format_level_display(next_level, 'Next: '):
            print(text2art(line, font=FONT))
    print('\n' * 2)

def main(program_args):
    level_i = START_LEVEL
    time_passed = START_TIME_PASSED

    while True:
        time.sleep(1)
        level = LEVELS[level_i]
        next_level = LEVELS[level_i + 1] if level_i < len(LEVELS) - 1 else None
        duration = level['duration']

        time_left = duration - time_passed

        if time_passed == 1 or time_passed == 6:
            speak(f'the current stage is {format_level_speech(level)}', program_args)
        elif time_left >= 0 and time_left <= 4:
            speak(f'{time_left + 1}', program_args)

        display_state(time_left, duration, level, next_level)

        time_passed = time_passed + 1

        if time_passed == duration:
            level_i = level_i + 1
            time_passed = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--speech-command', type=str, help='Speech command argument')
    args = parser.parse_args()

    # Access the value of --speech-command
    main(args)
