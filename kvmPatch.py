import time
import functools
import os.path
import pyudev
import subprocess
import copy

target_device = "Device('/sys/devices/pci0000:00/"

DESKTOP = 'wayland'

if DESKTOP == 'xorg':
    onRemove = ["/usr/bin/xset", "-display", ":1.0", "dpms", "force", "off"]
    afterOnRemove = [
        "/usr/bin/xset", "-display", ":1.0", "dpms", "force", "on"
    ]
else:
    # Activate screen saver, added bonus of locking with password
    onRemove = [
        "dbus-send --session --dest=org.gnome.ScreenSaver --type=method_call \
          /org/gnome/ScreenSaver org.gnome.ScreenSaver.SetActive boolean:true"
    ]
afterOnRemove = ["echo", "placeholder"]


def swap_screens():
    subprocess.run(onRemove, shell=True)
    time.sleep(10)
    subprocess.run(afterOnRemove, shell=True)


def main():
    base_path = os.path.abspath(os.path.dirname(__file__))
    path = functools.partial(os.path.join, base_path)
    call = lambda x, *args: subprocess.call([path(x)] + list(args))

    while True:
        try:
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem='usb')
            monitor.start()

            for device in iter(monitor.poll, None):
                if device.action == 'remove':
                    if target_device in str(device):
                        swap_screens()
                        break
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print('Exception')
            print(e)


if __name__ == '__main__':
    main()
