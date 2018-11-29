import ConnectionTracer
import time


# also, you can custom port and host
ConnectionTracer.config.PORT = 5037


# bind hook function
def hook_function(devices: set):
    print(devices)


ConnectionTracer.start(hook_function)
print('tracer already started :)')

# do something else you want
time.sleep(30)

# stop it
ConnectionTracer.stop()
print('tracer stopped')
