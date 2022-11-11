#!/usr/bin/env bash

while true; do
  x="`swaymsg -t get_inputs | jq --raw-output '[.[] | select(.type == "keyboard") | .xkb_active_layout_name | select(contains("English (US)") | not)] | first'`"
  if [[ "${x}" == "null" ]]; then
    echo English
  else
    echo "${x}"
  fi

  sleep 1
done
