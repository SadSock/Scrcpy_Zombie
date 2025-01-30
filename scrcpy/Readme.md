```bash
sudo apt install v4l2loopback-dkms   # install v4l2loopback
sudo modprobe v4l2loopback           # create a video device
scrcpy --v4l2-sink=/dev/video0 --no-window --audio-source=playback --audio-dup
ffplay -i /dev/video0                # test
```