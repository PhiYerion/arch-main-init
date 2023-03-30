#!/bin/bash

passwd
useradd -mG wheel user
passwd user

cp makepkg.conf /etc/makepkg.conf

runuser user -c "git clone https://aur.archlinux.org/yay.git /home/user/yay"
cd /home/user/yay
runuser user -c "makepkg -si"
cd /root
