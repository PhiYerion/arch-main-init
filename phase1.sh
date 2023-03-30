#!/bin/bash

genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
systemctl enable NetworkManager
ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
hwclock --systohc
locale-gen
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg

useradd -mG wheel user

cd /home/user
runuser user -c "git clone https://git.suckless.org/9base"
cd 9base/
runuser user -c "make"
cd ..
rm -rf 9base/

echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
reflector -c US -a 6 --sort rate --save /etc/pacman.d/mirrorlist
pacman -S sudo openssh openvpn
ssh-keygen
ssh-keygen -t ed25519

git clone https://aur.archlinux.org/yay.git

echo "colorscheme slate
set number
set relativenumber
set tabstop=4
set autoindent
set mouse=a" >> ~/.vimrc


