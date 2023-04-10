#!/usr/bin/env bash

sudo pigpiod
sudo python3 test_MotorsAndServos.py &
sudo python3 read_sensors.py &
python3 ws_vid_server.py &
wait




