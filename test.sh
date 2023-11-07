#!/bin/bash

BRANCH="DejaVOS"
WD="$(cd "$(dirname "$0")" && pwd)/DejaVOS"
mkdir "$WD"
cd "$WD" || exit
archiso=$( find /home -regex '.*archlinux.*iso$' -print -quit )

if [[ $archiso == "" ]]; then
	echo "No archlinux iso found. Download archiso somewhere under /home first."
	exit
fi
echo "Arch found at $archiso"

imageFile="$WD/imagefile.img"
socket=127.0.0.1:18901

qemu-img create -f raw "$imageFile" 32G
cp /usr/share/edk2-ovmf/x64/OVMF.fd "$WD"/OVMF.fd
chmod +rw "$WD"/OVMF.fd

qemu-system-x86_64 \
	-enable-kvm \
	-drive if=pflash,format=raw,file="$WD"/OVMF.fd \
	-cdrom "$archiso" \
	-boot order=d \
	-drive file="$imageFile",format=raw \
	-m 12G \
	-smp 4 \
	-vga virtio \
	-monitor telnet:$socket,server,nowait \
	-net user,hostfwd=tcp::10022-:22 \
	-net nic \
	&

cmd() {
	sleep 3
	for ((i=0;i<100;i++)); do 
		echo "sendkey ctrl-m"
		echo "sendkey ret"
		echo "sendkey spc"
		sleep 0.1
	done
	sleep 25
	for ((i = 0; i < ${#1}; i++)); do
		char="${1:$i:1}"
		if [[ $char == " " ]]; then
			char="spc"
		elif [[ $char == ";" ]]; then
			char="semicolon"
		elif [[ $char == "%" ]]; then
			char="shift-5"
		elif [[ $char == "-" ]]; then
			char="minus"
		elif [[ $char == "/" ]]; then
			char="slash"
		elif [[ $char == "." ]]; then
			char="dot"
		elif [[ $char == ":" ]]; then
			char="shift-semicolon"
		elif [[ $char == "'" ]]; then
			char="apostrophe"
		elif [[ $char =~ ^[A-Z]+$ ]]; then
			char="shift-${char,,}"
		elif [[ $char == "*" ]]; then
			char="shift-8"
		elif [[ $char == '>' ]]; then
			char="shift-dot"
		elif [[ $char == '=' ]]; then
			char='equal'
		elif [[ $char == '$' ]]; then
			char='shift-4'
		elif [[ $char == "\\" ]]; then
			char="ctrl-m"
			echo "sendkey $char"
			sleep 1
			continue
		fi
		sleep 0.02
			
		echo "sendkey $char"
	done
	echo "sendkey ctrl-m"
}

sleep 2
cmd "echo 'Server = http://10.0.2.2/arch-repo/\$repo/os/\$arch' > /etc/pacman.d/mirrorlist\passwd\arch\arch\systemctl start sshd\parted -s /dev/sda mklabel gpt\parted -s /dev/sda mkpart primary fat32 1mib 512mib\parted -s /dev/sda mkpart primary ext4 512mib 100%\parted /dev/sda set 1 esp on\sed -i 's/Required DatabaseOptional/Never/g' /etc/pacman.conf\mkfs.fat -F32 /dev/sda1;mkfs.ext4 /dev/sda2;mount --mkdir /dev/sda2 /mnt;mount --mkdir /dev/sda1 /mnt/boot;pacman -Sy git; git clone https://github.com/phiyerion/arch-main-init; cd arch-main-init; git checkout $BRANCH; git branch $BRANCH; ./install.py\n\n\n" \
	| nc 127.0.0.1 18901
