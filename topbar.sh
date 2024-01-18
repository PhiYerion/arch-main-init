while true; do
	date="$(date "+%Y-%m-%d %H:%M:%S.%1N")"
	load="$(uptime | grep -Po '([0-9]+\.[0-9][0-9]+(, )?)+')"
	max_charge_design="$(cat /sys/class/power_supply/BAT0/charge_full_design)"
	max_charge_now="$(cat /sys/class/power_supply/BAT0/charge_full)"
	charge="$(cat /sys/class/power_supply/BAT0/charge_now)"
	voltage="$(cat /sys/class/power_supply/BAT0/voltage_now)"
	current="$(cat /sys/class/power_supply/BAT0/current_now)"

	draw=$(( voltage * current / 1000000 ))
	charge_percent=$(( charge * 100 / max_charge_now ))
	bat_degredation=$(( max_charge_now * 10000 / max_charge_design ))

	xsetroot -name "$(( bat_degredation / 100 )).$(( bat_degredation % 100 ))% | $charge_percent% | $(( draw / 1000000 )).$(( draw % 1000000 ))w | $load | $date"
	sleep 0.1
done
