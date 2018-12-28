import threading

from ConnectionTracer import connection
from ConnectionTracer import utils
from ConnectionTracer import config


def _start(hook: callable):
    # reader for socket
    # trace this reader
    reader = utils.socket_reader(connection.adb_socket)

    last_devices = set()
    while connection.adb_socket is not None:
        new_line = next(reader)
        if not new_line:
            break
        current_devices = utils.decode_response(new_line)
        if current_devices == last_devices:
            continue
        hook(current_devices)
        last_devices = current_devices


def _init():
    """ build connection and init it"""
    connection.connect()

    # start track
    # all services were provided here:
    # https://android.googlesource.com/platform/system/core/+/jb-dev/adb/SERVICES.TXT
    ready_data = utils.encode_data('host:track-devices')
    connection.adb_socket.send(ready_data)

    # get status
    status = connection.adb_socket.recv(4)

    # make sure track is ready
    if status != b'OKAY':
        raise RuntimeError('adb server return "{}", not OKAY'.format(str(status)))


# API
def start(hook: callable, host=None, port=None):
    config.HOST = host or config.HOST
    config.PORT = port or config.PORT
    print('adb host: ', config.HOST)
    print('adb port: ', config.PORT)

    _init()
    tracer_thread = threading.Thread(target=_start, args=(hook,))
    tracer_thread.start()


def stop():
    connection.disconnect()


get_status = connection.get_status


__all__ = [
    'start',
    'stop',
    'config',
    'get_status',
]
