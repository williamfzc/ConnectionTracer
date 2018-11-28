# ConnectionTracer

[![PyPI version](https://badge.fury.io/py/ConnectionTracer.svg)](https://badge.fury.io/py/ConnectionTracer)

> when connected devices changed, do sth :)

## How it works?

Use a socket to connect adb server. Nothing about `subprocess` or `os.system`.

View [socket2adb](https://github.com/williamfzc/socket2adb) for detail.

## Installation

```
pip install ConnectionTracer 
```

## How to use?

```python
import ConnectionTracer
import time


# also, you can custom port and host
ConnectionTracer.config.PORT = 5037


# bind hook function
def hook_function(devices):
    print(devices)


ConnectionTracer.start(hook_function)
print('tracer already started :)')

# do something else you want
time.sleep(10)

# stop it
ConnectionTracer.stop()
print('tracer stopped')
```

When connected devices changed, `hook_function` would be called.

## More?

Code is quite simple, you can view [100-lines-ver](https://github.com/williamfzc/ConnectionTracer/blob/99aaea27e7014ded49bae02bfee3ce9f8bd2e14c/ConnectionTracer.py) for detail.
