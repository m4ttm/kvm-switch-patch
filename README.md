# KVM Switch Patch

## Overview
My KVM switch didn't work properly with a ThinkPad dock as it does not spoof EDIDs. The display works through the switch when the machine is booted, but once switched it cannot be switched back. This patch works around this issue when using a monitor with multiple inputs. If the switch is triggered, USB devices are disconnected. When this occurs, the patch switches off the display temporarily which causes the monitor to switch inputs.

## Setup
- Specify your target device (Optional)
Change the "target_device" variable to be more specific so it will only switch off the display when a specific device connected through the switch is removed
- Copy the Python file to /bin:
`sudo cp -i kvmPatch.py /bin`
- Add A New Cron Job:
`crontab -e`
- Scroll to the bottom and add the following line (after all the #'s):
`@reboot python3 /bin/kvmPatch.py &`
- Test it:
`sudo reboot`
