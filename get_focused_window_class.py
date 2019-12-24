#/bin/bash

xprop -id $(xdotool getactivewindow) | grep -F "WM_CLASS(STRING)" | cut -c 20-
