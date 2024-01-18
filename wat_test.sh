frames=0
draw=0
while true; do
	voltage="$(cat /sys/class/power_supply/BAT0/voltage_now)"
	current="$(cat /sys/class/power_supply/BAT0/current_now)"
	frames=$(( frames + 1 ))
	draw=$((draw + voltage * current / 1000000 ))
	echo "Watt: $(( draw / frames ))"
	sleep 1
done
