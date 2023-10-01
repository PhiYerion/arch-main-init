#!/bin/bash

BRANCH="dejavos"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir "$BASE_DIR/DejaVOS"
archiso=`find /home -regex '.*archlinux.*iso$' -print -quit`

if [[ $archiso == "" ]]; then
	echo "No archlinux iso found. Download archiso somewhere under /home first."
	exit
fi

imageFile="$BASE_DIR/imagefile.img"
socket=127.0.0.1:18901

qemu-img create -f qcow "$imageFile" 12G

qemu-system-x86_64 -enable-kvm \
	-cdrom $archiso \
	-boot order=d \
	-drive file=$imageFile,format=qcow \
	-m 4G \
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
		elif [[ $char == "S" ]]; then
			char="shift-s"
		elif [[ $char == "F" ]]; then
			char="shift-f"
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
cmd "passwd\arch\arch\systemctl start sshd\parted -s /dev/sda mklabel gpt\parted -s /dev/sda mkpart primary ext4 1mib 512mib\parted -s /dev/sda mkpart primary ext4 512mib 100%\mkfs.vfat -F32 /dev/sda1;mkfs.ext4 -F /dev/sda2;mount --mkdir /dev/sda2 /mnt;mount --mkdir /dev/sda1 /mnt/boot;pacman -Sy git; git clone https://github.com/phiyerion/arch-main-init; cd arch-main-init; git checkout $BRANCH; git branch $BRANCH; ./install.py\n\n\n\n\n\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y\y" \
	| nc 127.0.0.1 18901
