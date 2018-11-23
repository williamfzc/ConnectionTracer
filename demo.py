import ConnectionTracer


def hook_function(devices):
    print(devices)


ConnectionTracer.start(hook_function)
print('tracer already started :)')
