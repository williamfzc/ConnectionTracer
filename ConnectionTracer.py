import socket
import threading


HOST = '127.0.0.1'
PORT = 5037
ENCODING = 'utf-8'


def connect():
    """ create socket and connect to adb server """
    client = socket.socket()
    client.connect((HOST, PORT))
    return client


# connection to adb server
adb_connection = connect()


# start trace
def encode_data(data: str):
    byte_data = data.encode(ENCODING)
    byte_length = "{0:04X}".format(len(byte_data)).encode(ENCODING)
    return byte_length + byte_data


# start track
# all services were provided here:
# https://android.googlesource.com/platform/system/core/+/jb-dev/adb/SERVICES.TXT
ready_data = encode_data('host:track-devices')
adb_connection.send(ready_data)


def socket_reader():
    """ read data from adb socket """
    while True:
        buf = adb_connection.recv(1024)
        if not len(buf):
            # trace end
            adb_connection.close()
        yield buf


# get them
status = adb_connection.recv(4)

# make sure track is ready
if status != b'OKAY':
    raise RuntimeError('connection error, try to restart adb server?')

# reader for socket
# trace this reader
reader = socket_reader()


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
    last_devices = set()
    while True:
        new_line = next(reader)
        current_devices = decode_response(new_line)
        if current_devices == last_devices:
            continue
        hook(current_devices)
        last_devices = current_devices


# API
def start(hook: callable):
    detector = threading.Thread(target=_start, args=(hook,))
    detector.start()
    return detector


# main
def _test_hook(devices):
    print(devices)


if __name__ == '__main__':
    _start(_test_hook)
