#https://gitlab.com/eflinux/arch-basic/-/blob/master/base-uefi.sh

# Probably for all installations
pacstrap -K /mnt dosfstools ntfs-3g networkmanager dialog rsync intel-ucode reflector base base-devel bash-completion linux linux-headers linux-firmware vim grub efibootmgr
genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
systemctl enable NetworkManager
ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime
hwclock --systohc
locale-gen

grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
echo "GRUB_DISABLE_OS_PROBER=false" >> /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg
mv makepkg.conf /etc/makepkg.conf

# useradd -mG wheel user
# Uncomment %wheel ALL=(ALL:ALL) ALL

echo "colorscheme slate
set number
set relativenumber
set tabstop=4
set autoindent
set mouse=a" >> ~/.vimrc

echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
reflector -a 6 --sort rate --save /etc/pacman.d/mirrorlist
pacman -S sudo openssh openvpn
ssh-keygen
ssh-keygen -t ed25519

# Hardware stuff
pacman -S nvidia nvidia-utils nvidia-settings

# Optionals
pacman -S discord vnstat wget curl lynx xdg-utils xdg-user-dirs git vim obs-studio vlc kdenlive tmux htop

# Accessory stuff
pacman -S pulseaudio cups alsa-utils pipewire pipewire-alsa pipewire-pulse pipewire-jack piper 
## Laptop
###  pacman -S acpid bluez bluez-utils acpi acpi_call tlp

# Display
pacman -S xorg xorg-server xorg-xinit xorg-apps sddm plasma kde-applications 
systemctl enable sddm

# Server
# pacman -S installdnsmasq dnsutils inetutils nss-mdns

# Additional Optional
pacman -S iptables-nft ipset firewalld openbsd-netcat dosfstools mtools flatpak

useradd -mG wheel user
echo '%wheel ALL=(ALL:ALL) ALL' >> /etc/sudoers

git clone https://aur.archlinux.org/yay.git
cd yay.git

# Now reboot
