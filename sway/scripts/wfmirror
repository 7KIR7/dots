#!/bin/bash
# sway-mirror OPTIONS
#
# Examples:
#
# SDL_VIDEODRIVER=wayland sway-mirror
#
# SDL_VIDEODRIVER=x11 sway-mirror
#
# sway-mirror --output LVDS-1
#
instance=sway-mirror$$
wf-recorder "$@" -c rawvideo -m sdl -f pipe:$instance &
sleep 1
if kill -0 $! 2>/dev/null && swaymsg "[title=\"^pipe:$instance\$\"] nop" >/dev/null; then
	while read type ; read name ; do 
		if [[ $type == '"close"' && $name == "\"pipe:$instance\"" ]]; then
			break
		fi
	done < <(swaymsg -mt subscribe '["window"]' | jq --unbuffered .change,.container.name)
	#while jobs '%1' >/dev/null && swaymsg "[title=\"^pipe:wf-mirror$$\$\"] nop" >/dev/null; do
	#	sleep 1
	#done
fi
kill -INT '%1'
exit 0
