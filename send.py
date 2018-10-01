#!/usr/bin/python3
"""
Requirements:
  sudo apt install python3-pip
  pip3 install termcolor
"""

"""
Requirements:
  sudo apt install libnotify-bin
"""

import json
import os
import subprocess
from termcolor import colored


def parse(data):
    size = len(data["list"])

    # Ask if run
    for index, item in enumerate(data["list"]):
        item["input"] = input("{}/{}: Run command {} for {}? (y/N) ".format(
            index + 1,
            size,
            colored(item["command"], "green"),
            colored(item["name"], "yellow"),
        ))

    # Run if confirmed
    for index, item in enumerate(data["list"]):
        if item["input"].lower() == "y":
            print("{}/{}: Running {} for {}...".format(
                index + 1,
                size,
                colored(item["command"], "green"),
                colored(item["name"], "yellow"),
            ))
            item["status"] = subprocess.run(item["command"], shell=True)

            print("{}/{}: {} finished as {}".format(
                index + 1,
                size,
                colored(item["name"], "green"),
                colored(item["status"], "yellow"),
            ))
            os.system("notify-send {} done".format(item["name"]))
            input(colored(
                "Press ENTER to continue...",
                "green",
                attrs=["reverse", "blink"],
            ))

    print("")
    print("+---------+")
    print("| Results |")
    print("+---------+")
    for item in data["list"]:
        if "status" in item:
            print("{}: {}".format(
                colored(item["name"], "green"),
                colored(item["status"], "yellow"),
            ))
        else:
            print("{}: {}".format(
                colored(item["name"], "green"),
                colored("skipped", "yellow"),
            ))


if __name__ == "__main__":
    with open("send.json") as f:
        parse(json.load(f))
