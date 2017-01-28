#!/usr/bin/env python

from app import app

def get_broadlink_devices():
    devices = broadlink.discover(timeout=5)
    for d in devices:
        d.auth()
    return devices

if __name__ == '__main__':
    app.run(debug = True)
