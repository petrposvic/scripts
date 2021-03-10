#!/usr/bin/env python3

import json
import os
import re
import sh
import sys

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Absolute path of config file. The best is use the same directory where this
# script is located.
dirname = os.path.dirname(sys.argv[0])
config_file_path = os.path.join(dirname, 'microphone.json')

# Window to store in config file.
#   'title' - string only for identifying and can be anything (even None); it
#           is overriden after user choose the correct window or it is loaded
#           from config file
#   'id'    - number (int) of window; it is 'None' until user choose
#           the correct window or it is loaded from config file
#   'key'   - event (string) that is triggered by xdotools
window = {
    'title': 'meet chrome window',
    'id': None,
    'key': 'Ctrl+d',
}
# -----------------------------------------------------------------------------

assert config_file_path.endswith('.json'), "Config file should end with json suffix"
assert 'id' in window, "Window object has to contain 'id' attribute"


def select_window():
    out = sh.xwininfo('-int')
    out = out.stdout.decode('utf-8')
    m = re.search(r'xwininfo: Window id: (\d+) ([^\n]+)', out)
    return m.group(1), m.group(2)


def init():
    print(f"Select window: {window['title']}")
    window['id'], window['title'] = select_window()
    if not window['id']:
        print("Can't found window ID")
        sys.exit(1)

    with open(config_file_path, 'w') as f:
        json.dump(window, f)
        print("Next launch:")
        print("1) focus on window {} ({})".format(window['id'], window['title']))
        print("2) send event {}".format(window['key']))
        print("3) focus on previous (source) window")


def _i3_get_current_windows():
    def find(element, results=[]):
        if 'focused' in element and element['focused']:
            results.append(element)
        if 'nodes' in element:
            for node in element['nodes']:
                find(node, results)
        return results
    tree = json.loads(sh.i3_msg('-t', 'get_tree').stdout)
    return find(tree)


if __name__ == '__main__':
    # Sleep some time to provide time to release all pressed keys
    sh.sleep(1)

    try:
        with open(config_file_path) as f:
            window = json.load(f)
            print(f"Using '{config_file_path}' config: {window}")
            print("Delete config file if you need to change windows:")
            print(f"  rm {config_file_path}")
            try:
                current_window_id = _i3_get_current_windows()[0]['window']
                sh.xdotool('windowactivate', window['id'])
                sh.xdotool('key', window['key'])
                sh.xdotool('windowactivate', current_window_id)
            except sh.ErrorReturnCode:
                print("Some command fails")

    except FileNotFoundError:
        print(f"File '{config_file_path}' not found")
        init()
