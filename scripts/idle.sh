#!/bin/env bash
swayidle \
	timeout 60 '~/.config/sway/scripts/lock.sh --grace 2 --fade-in 4' \
	timeout 65 'swaymsg "output * dpms off"' \
	resume 'swaymsg "output * dpms on"' \
	before-sleep '~/.config/sway/scripts/lock.sh'
