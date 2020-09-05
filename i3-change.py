#!/usr/bin/python3


import click
import json
import logging
import os
import re
import subprocess


log = logging.getLogger(__name__)


def get_current_workspace():
    process = subprocess.run([
        'i3-msg',
        '-t',
        'get_workspaces',
    ], check=True, stdout=subprocess.PIPE)

    return [workspace['name'] for workspace in json.loads(process.stdout) if workspace['focused']][0]  # noqa: E501


def get_current_window_id():
    ps = subprocess.Popen([
        'i3-msg',
        '-t',
        'get_tree',
    ], stdout=subprocess.PIPE)

    process = subprocess.run([
        'jq',
        '-r',
        '.. | select(.focused? and .focused == true).id'
    ], check=True, stdin=ps.stdout, stdout=subprocess.PIPE)

    ps.wait()
    return process.stdout.decode('utf-8').strip()


def get_current_window_id2():
    process = subprocess.run([
        'i3-msg',
        '-t',
        'get_tree',
    ], check=True, stdout=subprocess.PIPE)

    def find(element, results=[]):
        if 'focused' in element and element['focused']:
            results.append(element)
        if 'nodes' in element:
            for node in element['nodes']:
                find(node, results)
        return results

    return find(json.loads(process.stdout))[0]['id']


def get_current_mouse():
    process = subprocess.run([
        'xdotool',
        'getmouselocation',
    ], check=True, stdout=subprocess.PIPE)

    match = re.match('x:(\\d+) y:(\\d+) screen:(\\d+) window:(\\d+)', process.stdout.decode('utf-8'))  # noqa: E501
    return match[1], match[2]


def communicate(data: str):
    fifo = '/tmp/in-memory-storage'
    if not os.path.exists(fifo):
        return None

    with open(fifo, 'w') as f:
        f.write(data)
    with open(fifo, 'r') as f:
        return f.read()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--due', type=click.Choice(['left', 'up', 'down', 'right']))
def focus(due):
    old = get_current_workspace()
    mouse_x, mouse_y = get_current_mouse()
    communicate(f'i3-workspace-{old}={mouse_x} {mouse_y}')

    subprocess.run([
        'i3-msg',
        'focus',
        due,
    ], check=True)

    new = get_current_workspace()
    if old == new:
        return

    match = re.match('(\\d+) (\\d+)', communicate(f'i3-workspace-{new}'))
    if match:
        window_id = get_current_window_id2()

        subprocess.run([
            'xdotool',
            'mousemove',
            match[1],
            match[2],
        ], check=True)

        subprocess.run([
            'i3-msg',
            f'[con_id="{window_id}"] focus',
        ], check=True, stdout=subprocess.PIPE)


@cli.command()
@click.argument('name')
def workspace(name):
    mouse_x, mouse_y = get_current_mouse()
    communicate(f'i3-workspace-{get_current_workspace()}={mouse_x} {mouse_y}')

    subprocess.run([
        'i3-msg',
        'workspace',
        name,
    ], check=True)

    match = re.match('(\\d+) (\\d+)', communicate(f'i3-workspace-{name}'))
    if match:
        subprocess.run([
            'xdotool',
            'mousemove',
            match[1],
            match[2],
        ], check=True)


if __name__ == '__main__':
    cli()
