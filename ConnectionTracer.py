import socket
import threading


HOST = '127.0.0.1'
PORT = 5037
ENCODING = 'utf-8'

# GLOBAL CONNECTION
adb_connection = None


def connect():
    """ create socket and connect to adb server """
    client = socket.socket()
    client.connect((HOST, PORT))
    return client


# start trace
def encode_data(data: str):
    byte_data = data.encode(ENCODING)
    byte_length = "{0:04X}".format(len(byte_data)).encode(ENCODING)
    return byte_length + byte_data


def socket_reader(connection):
    """ read data from adb socket """
    while connection is not None:
        try:
            buf = connection.recv(1024)
        except ConnectionAbortedError:
            print('connection aborted')

        if not len(buf):
            # trace end
            connection.close()
        yield buf


# decode adb response
def decode_response(content: bytes):
    content = content[4:].decode(ENCODING)
    if '\t' not in content and '\n' not in content:
        return set()

    connected_devices = set()
    device_list = [i for i in content.split('\n') if i]
    for each_device in device_list:
        device_id, device_status = each_device.split('\t')
        if device_status == 'device':
            connected_devices.add(device_id)
    return connected_devices


def _start(hook: callable):
    global adb_connection
    # connection to adb server
    adb_connection = connect()

    # start track
    # all services were provided here:
    # https://android.googlesource.com/platform/system/core/+/jb-dev/adb/SERVICES.TXT
    ready_data = encode_data('host:track-devices')
    adb_connection.send(ready_data)

    # get them
    status = adb_connection.recv(4)

    # make sure track is ready
    if status != b'OKAY':
        raise RuntimeError('connection error, try to restart adb server?')

    # reader for socket
    # trace this reader
    reader = socket_reader(adb_connection)

    last_devices = set()
    while adb_connection is not None:
        new_line = next(reader)
        current_devices = decode_response(new_line)
        if current_devices == last_devices:
            continue
        hook(current_devices)
        last_devices = current_devices


# API
def start(hook: callable):
    if adb_connection is not None:
        raise RuntimeError('Tracer instance already existed')
    detector = threading.Thread(target=_start, args=(hook,))
    detector.start()
    return detector


def stop():
    global adb_connection
    adb_connection.close()
    adb_connection = None


# ALL CODE END

# FOR TEST
def _test_hook(devices):
    print(devices)


if __name__ == '__main__':
    _start(_test_hook)
