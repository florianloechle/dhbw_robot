import threading
import time
import click
import os

from flask import Flask, send_from_directory, request
from find_animal import find_animal

@click.command()
@click.option('--host', '-h', type=str, default='localhost')
@click.option('--port', '-p', type=int, default=8000)
def main(host, port):

    app = Flask('Robot Remote')
    public_dir = './web/build'

    # Add serve directory for index page
    @app.route('/', methods=['GET'])
    def index():
        return send_from_directory(public_dir, 'index.html')

    # Add route to serve static files
    @app.route('/static/<type>/<file>', methods=['GET'])
    def send_static(type, file):
        return send_from_directory(public_dir + '/static/' + type, file)

    start_remote(app, host, port)


def start_remote(server, host, port):

    state = {
        'debug': False,
        'animal': None,
    }

    @server.route('/debug', methods=['PUT'])
    def set_debug():
        state.__setitem__('debug', not state['debug'])
        return state

    @server.route('/animal/<animal>', methods=['POST'])
    def start_find_animal(animal):
        animals = ['frog', 'turtle', 'leopard', 'tomato', 'dino']

        if not animal in animals:
            return 'Unexpected animal ' + animal.upper(), 400

        if state.get('animal') is not None:
            return 'Finding process is already in progress.', 406

        state.__setitem__('animal', animal)
        find_animal(animal,state.get('debug'))
        state.__setitem__('animal', None)

        return state


    server.run(host=host, port=port,
               debug=False, use_reloader=False)


if __name__ == '__main__':
    main()
