#!/usr/bin/python3
import re
import subprocess
from PyInquirer import prompt


def choose_dev():
    device_list = [{
        "type": "list",
        "name": "dev",
        "message": "Select device:",
        "choices": [],
    }]
    with subprocess.Popen(
        "xinput list".split(),
        stdout=subprocess.PIPE,
    ) as proc:
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if line == "":
                break
            m = re.match("(.*)id=(\\d+).*", line)
            if m:
                device_list[0]["choices"].append({
                    "name": "{} ({})".format(m.group(1).rstrip(), m.group(2)),
                    "value": m.group(2),
                })
    return prompt(device_list)["dev"]


def choose_prop(dev):
    prop_list = [{
        "type": "list",
        "name": "prop",
        "message": "Select property:",
        "choices": [],
    }]
    with subprocess.Popen(
        "xinput list-props {}".format(dev).split(),
        stdout=subprocess.PIPE,
    ) as proc:
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if line == "":
                break

            m = re.match("[ ]*([^(]*)\\((\\d+)\\):(.*)", line)
            if m:
                print("{} ({}): {}".format(
                    m.group(1).strip(),
                    m.group(2),
                    m.group(3).strip(),
                ))
                prop_list[0]["choices"].append({
                    "name": "{} ({}): {}".format(
                        m.group(1).strip(),
                        m.group(2),
                        m.group(3).strip(),
                    ),
                    "value": m.group(2),
                })
    return prompt(prop_list)["prop"]


def enter_val(dev, prop):
    val = prompt([{
        "type": "input",
        "name": "val",
        "message": "Type new value:",
    }])["val"]

    cmd = "xinput set-prop {} {} {}".format(dev, prop, val)
    if prompt([{
        "type": "confirm",
        "name": "execute",
        "message": "Execute command: '{}'?".format(cmd)
    }])["execute"]:
        with subprocess.Popen(
            "xinput set-prop {} {} {}".format(dev, prop, val).split(),
            stdout=subprocess.PIPE,
        ) as proc:
            while True:
                line = proc.stdout.readline().decode("utf-8")
                if line == "":
                    break
                print(line)


dev = choose_dev()
prop = choose_prop(dev)
enter_val(dev, prop)
