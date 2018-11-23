# ConnectionTracer

[![PyPI version](https://badge.fury.io/py/ConnectionTracer.svg)](https://badge.fury.io/py/ConnectionTracer)

> when connected devices changed, do sth :)

## How it works?

Use a socket to connect adb server. Nothing about `subprocess` or `os.system`.

## How to use?

```python
import ConnectionTracer


def hook_function(devices):
    # devices is: current devices set
    print(devices)

# also, you can custom port and host
ConnectionTracer.PORT = 5037

ConnectionTracer.start(hook_function)
print('tracer already started :)')
```

When connected devices changed, `hook_function` would be called.

## More?

100 lines only. You can read [it](ConnectionTracer.py) for detail directly.
