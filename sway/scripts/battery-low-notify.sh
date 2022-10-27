#!/bin/sh

need_notify_low=1
need_notify_critical=1

while true; do
	acpi="$(acpi -b)"
	percent="$(echo "$acpi" | grep -P -o '[0-9]+(?=%)')"
	status="$(echo "$acpi" | grep -P -o '(?<=: )[^,]+')"

	if [ "$status" = "Discharging" ]; then
		if [ "$need_notify_critical" -eq 1 ] && [ "$percent" -eq 20 ]; then
			notify-send -i critical -i /usr/share/icons/ePapirus/48x48/status/battery-caution.svg "Battery critical" "$percent% remaining";  mpv .config/sway/scripts/LowBattery.mp3
			need_notify_critical=0
			need_notify_low=0
		elif [ "$need_notify_low" -eq 1 ] && [ "$percent" -eq 30 ]; then
			notify-send -i /usr/share/icons/ePapirus/48x48/status/battery-low.svg "Battery low" "$percent% remaining"; mpv .config/sway/scripts/LowBattery.mp3
			need_notify_low=0
		fi
	else
		need_notify_low=1
		need_notify_critical=1
	fi

	sleep 5m
done
