#!/bin/sh
# This is bash program to display Hello World
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"
export XDG_RUNTIME_DIR="/run/user/1000"

bat_lvl=$(acpi -b | grep "Battery 0" | grep -P -o '[0-9]+(?=%)')
bat_discharge=$(acpi -b | grep "Battery 0" | grep -c "Discharging")

if [ "$bat_lvl" -eq 20 ]; then
    notify-send --icon="~/.config/scripts/battery/bt-low.svg"  -u critical "Battery Critically Low";
mpv ~/.config/scripts/battery/warn.mp3
fi
if [ "$bat_lvl" -eq 30 ]; then
    notify-send --icon="~/.config/scripts/battery/bt-low.svg"  -u critical "Battery Low";
mpv ~/.config/scripts/battery/warn.mp3
fi
if [ "$bat_lvl" -eq 80 ] && [ "$bat_discharge" -eq 0 ]; then
    notify-send --icon="~/.config/scripts/battery/bt-full.svg" -u critical "Battery Almost Full";
fi
if [ "$bat_lvl" -eq 90 ] && [ "$bat_discharge" -eq 0 ]; then
    notify-send --icon="~/.config/scripts/battery/bt-full.svg" -u critical "Battery Full";
fi
