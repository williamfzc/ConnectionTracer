import socket

from ConnectionTracer import config


# start trace
def encode_data(data: str) -> bytes:
    byte_data = data.encode(config.ENCODING)
    byte_length = "{0:04X}".format(len(byte_data)).encode(config.ENCODING)
    return byte_length + byte_data


def socket_reader(connection: socket, buffer_size: int = 1024):
    """ read data from adb socket """
    while connection is not None:
        try:
            buffer = connection.recv(buffer_size)
            # no output
            if not len(buffer):
                raise ConnectionAbortedError
        except ConnectionAbortedError:
            # socket closed
            print('connection aborted')
            connection.close()
            yield None
        except OSError:
            # still operate connection after it was closed
            print('socket closed')
            connection.close()
            yield None
        else:
            yield buffer


# decode adb response
def decode_response(content: bytes) -> set:
    """ adb response text -> device set """
    content = content[4:].decode(config.ENCODING)
    if '\t' not in content and '\n' not in content:
        return set()

    connected_devices = set()
    device_list = [i for i in content.split('\n') if i]
    for each_device in device_list:
        device_id, device_status = each_device.split('\t')
        if device_status == 'device':
            connected_devices.add(device_id)
    return connected_devices
