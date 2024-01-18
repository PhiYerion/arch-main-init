while true; do
	voltage="$(cat /sys/class/power_supply/BAT0/voltage_now)"
	current="$(cat /sys/class/power_supply/BAT0/current_now)"
	draw=$((voltage * current / 1000000 ))
	echo "Watt: $(( draw ))"
	sleep 1
done
