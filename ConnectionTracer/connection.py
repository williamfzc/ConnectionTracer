import socket
import warnings
import subprocess

from ConnectionTracer import config


# GLOBAL CONNECTION
adb_socket = None


def connect():
    """ create socket and connect to adb server """
    global adb_socket
    if adb_socket is not None:
        raise RuntimeError('connection already existed')

    host, port = config.HOST, config.PORT

    connection = socket.socket()
    try:
        connection.connect((host, port))
    except ConnectionError as _:
        warn_msg = 'failed when connecting to adb server: {}:{}, retrying ...'.format(host, port)
        warnings.warn(warn_msg)
        reboot_adb_server()
        connect()
        return

    adb_socket = connection


def disconnect():
    """ close socket """
    global adb_socket
    if adb_socket is not None:
        adb_socket.close()
        adb_socket = None
        return
    warnings.warn('connection already closed')


def get_status():
    """ get connection status: true or false """
    global adb_socket
    return adb_socket is not None


def reboot_adb_server():
    """ execute 'adb devices' to start adb server """
    _reboot_count = 0
    _max_retry = 1

    def _reboot():
        nonlocal _reboot_count
        if _reboot_count >= _max_retry:
            raise RuntimeError('fail after retry {} times'.format(_max_retry))
        _reboot_count += 1

        return_code = subprocess.call(['adb', 'devices'], stdout=subprocess.DEVNULL)
        if bool(return_code):
            warnings.warn('return not zero, execute "adb version" failed')
            raise EnvironmentError('adb did not work :(')

    return _reboot


reboot_adb_server = reboot_adb_server()
