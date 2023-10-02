#!/bin/bash

BRANCH="DejaVOS"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir "$BASE_DIR/DejaVOS"
archiso=`find /home -regex '.*archlinux.*iso$' -print -quit`

if [[ $archiso == "" ]]; then
	echo "No archlinux iso found. Download archiso somewhere under /home first."
	exit
fi

imageFile="$BASE_DIR/imagefile.img"
socket=127.0.0.1:18901

qemu-img create -f raw "$imageFile" 32G

qemu-system-x86_64 -enable-kvm \
	-cdrom $archiso \
	-boot order=d \
	-drive file=$imageFile,format=raw \
	-m 12G \
	-smp 4 \
	-vga virtio \
	-monitor telnet:$socket,server,nowait \
	-net user,hostfwd=tcp::10022-:22 \
	-net nic \
	&

cmd() {
	sleep 0.2
	for ((i=0;i<20;i++)); do 
		echo "sendkey ctrl-m"
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

sleep 1
cmd "passwd\arch\arch\systemctl start sshd\parted -s /dev/sda mklabel gpt\parted -s /dev/sda mkpart primary ext4 1mib 512mib\parted -s /dev/sda mkpart primary ext4 512mib 100%\sed -i 's/Required DatabaseOptional/Never/g' /etc/pacman.conf\mkfs.vfat -F32 /dev/sda1;mkfs.ext4 /dev/sda2;mount --mkdir /dev/sda2 /mnt;mount --mkdir /dev/sda1 /mnt/boot;pacman -Sy git; git clone https://github.com/phiyerion/arch-main-init; cd arch-main-init; git checkout $BRANCH; git branch $BRANCH; ./install.py" \
	| nc 127.0.0.1 18901
