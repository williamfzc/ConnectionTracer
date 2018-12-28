import ConnectionTracer
import time


# also, you can custom port and host
ConnectionTracer.config.PORT = 5037


# bind hook function
def hook_function(devices: set):
    print(devices)


ConnectionTracer.start(hook_function)
# also you can directly run:
# ConnectionTracer.start(hook_function, port=8080)

print('tracer already started :)')

# get connection status
print('now status: ', ConnectionTracer.get_status())

# do something else you want
time.sleep(30)

# stop it
ConnectionTracer.stop()
print('tracer stopped')
