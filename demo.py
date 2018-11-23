import adb_device_trace


def hook_function(devices):
    print(devices)


adb_device_trace.start(hook_function)
print('tracer already started :)')
