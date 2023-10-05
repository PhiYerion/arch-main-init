#!/bin/bash

BRANCH="DejaVOS"
WD="$(cd "$(dirname "$0")" && pwd)/DejaVOS"
mkdir $WD
cd $WD
archiso=`find /home -regex '.*archlinux.*iso$' -print -quit`

if [[ $archiso == "" ]]; then
	echo "No archlinux iso found. Download archiso somewhere under /home first."
	exit
fi
echo "Arch found at $archiso"

imageFile="$WD/imagefile.img"
socket=127.0.0.1:18901

#cp /usr/share/edk2-ovmf/x64/OVMF.fd $WD/OVMF.fd
#chmod +rw $WD/OVMF.fd

qemu-system-x86_64 \
	-enable-kvm \
	-drive if=pflash,format=raw,file=$WD/OVMF.fd \
	#-cdrom $archiso \
	-boot order=d \
	-drive file=$imageFile,format=raw \
	-m 12G \
	#-smp 4 \
	#-vga virtio \
	#-monitor telnet:$socket,server,nowait \
	#-net user,hostfwd=tcp::10022-:22 \
	#-net nic
