#!/bin/sh

swayidle -w -d \
	timeout 100 '~/.config/sway/lock.sh -f --grace 12 --fade-in 10' \
	timeout 140 'swaymsg "output * dpms off"' \
	resume 'swaymsg "output * dpms on"; sleep 2; swaymsg "output * enable"' \
	before-sleep 'pgrep swaylock || ~/.config/sway/lock.sh -f --fade-in 0 && true'
