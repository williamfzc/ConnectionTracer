import socket
import warnings

from ConnectionTracer import config


# GLOBAL CONNECTION
adb_socket = None


def connect():
    """ create socket and connect to adb server """
    global adb_socket
    if adb_socket is not None:
        raise RuntimeError('connection already existed')

    connection = socket.socket()
    connection.connect((config.HOST, config.PORT))

    adb_socket = connection


def disconnect():
    """ close socket """
    global adb_socket
    if adb_socket is not None:
        adb_socket.close()
        return
    warnings.warn('connection already closed')
