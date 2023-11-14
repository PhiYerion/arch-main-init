#!/bin/bash

passwd
useradd -mG wheel $NEW_USERNAME
passwd $NEW_USERNAME

cp makepkg.conf /etc/makepkg.conf

systemctl enable NetworkManager
systemctl enable cronie

ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
hwclock --systohc
locale-gen
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

#cd /home/$NEW_USERNAME
#runuser $NEW_USERNAME -c "git clone https://git.suckless.org/9base"
#cd 9base/
#runuser $NEW_USERNAME -c "make"
#cd ..
#rm -rf 9base/

echo "127.0.0.1 localhost\n::1       localhost" > /etc/hosts
echo "nameserver 1.1.1.1" > /etc/resolv.conf
#reflector -c US --age 12 --protocol https -a 6 --sort rate --save /etc/pacman.d/mirrorlist
echo 'Server = http://10.0.2.2/arch-repo/$repo/os/$arch' > /etc/pacman.d/mirrorlist
ssh-keygen
ssh-keygen -t ed25519

echo "colorscheme slate
set number
set relativenumber
set tabstop=4
set autoindent
set mouse=a" >> ~/.vimrc


