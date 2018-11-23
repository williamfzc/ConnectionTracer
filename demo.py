import ConnectionTracer


def hook_function(devices):
    print(devices)


# also, you can custom port and host
ConnectionTracer.PORT = 5037

ConnectionTracer.start(hook_function)
print('tracer already started :)')
