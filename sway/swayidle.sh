#!/bin/env bash
swayidle timeout 100 "~/.config/swaylock/lock.sh 50" \
  timeout 110 'swaymsg "output * dpms off"' \
  resume 'swaymsg "output * dpms on"' \
  before-sleep "~/.config/swaylock/lock.sh 50" &
