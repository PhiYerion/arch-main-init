# With User
su user
yay -S makepkg-optimize

# STEAM
## uncomment from /etc/pacman.conf:
sudo echo '[multilib]
Include = /etc/pacman.d/mirrorlist' >> /etc/pacman.conf
### Maybe do this https://wiki.archlinux.org/title/Systemd-resolved#DNS
sudo pacman -S ttf-liberation lib32-nvidia-utils lib32-systemd wine wine-gecko wine-mono lib32-alsa-lib lib32-alsa-plugins lib32-libpulse lib32-pipewire pipewire-pulse lib32-libpulse
yay -S steamcmd
flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak --user install flathub com.valvesoftware.Steam
flatpak run com.valvesoftware.Steam

# MISC
sudo pacman -S element-desktop keepassxc monero tor
yay -S tor-browser
yay -S ckb-next
yay -S protonvpn-cli
yay -S google-chrome
# yay -S librewolf # This takes a long time to compile, naturally
```
