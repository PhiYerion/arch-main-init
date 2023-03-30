#!/bin/python

import subprocess as sp

def main():
    toInstall = "bash-completion dosfstools linux linux-firmware linux-headers base vim vi grub efibootmgr git reflector python cronie"
    toInstall += " gcc make pacman cmake fakeroot" # this instead of base-devel
    addInstall = []
    commands = str()
    raid = False
    sudo = True

    def pmt(p, s = str(), defaultY = True, b_install = False):
        if defaultY:
            inp = input(p + " (Y/n)").lower()
            b = 'n' not in inp
        else:
            inp = input(p + " (y/N)").lower()
            b = 'y' in inp

        if b:
            if b_install:
                addInstall.append(" " + p)
            else:
                if len(s) > 0:                   # jank
                    addInstall.append(" " + s)
            return True

    sp.run(
        ('echo "' + input("What would you like your hostname to be?") + '" > /mnt/etc/hostname').split())


    if input("Doas or Sudo (d/s)").lower() in 'sS':
        toInstall += " sudo"
    else:
        toInstall += " doas"

    if pmt("Are you using mdadm/raid?", "mdadm"):
        raid = True

    pmt("Are you going to use nfts?", "ntfs-3g")

    pmt("Virtual machines?", "vde2 virt-manager qemu-base qemu-arch-extra edk2-ovmf bridge-utils")

    pmt("Bluetooth?", "bluz bluez-utils")
    pmt("Wifi?", "wpa_supplicant")
    pmt("Laptop?", "acpi acpi_call tlp acpid")

    if not pmt("Would you like to install more minimal base-devel + my selection? (make, gcc, pacman, cmake already included prior)", "archlinux-keyring gzip"):
        pmt("Then, would you like to install all base-devel?", "archlinux-keyring fakeroot file findutils flex gettext groff gzip libtool m4 patch pkgconf texinfo which")

    if not pmt("My Selection of tools?", "xdg-user-dirs tmux lynx wget vnstat tor openbsd-netcat python-pip cronie openssh htop sensors"):
        if pmt("Would you like to select some instead?"):
            for s in "xdg-user-dirs tmux lynx wget vnstat tor openbsd-netcat python-pip openssh htop sensors".split():
                pmt(s)

    if pmt("Firewall?"):
        if not pmt("UFW? (other option is iptables)", "ufw"):
            pmt("iptables-ntf + firewalld?", "iptables-nft ipset firewalld")

    if pmt("Do you want a desktop?)", "xorg xorg-xinit pulseaudio alsa-utils pipewire pipewire-jack piper"):
        if pmt("KDE+Xorg?", "sddm plasma"):
            commands += " systemctl enable sddm;"
            pmt("Plasma Applications?", " kde-applications")
        else:
            print("Good luck on that.")
        
        for s in ["discord", "element-desktop", "torbrowser-launcher", "vlc", "obs-studio", "xdg-utils", "kdenlive"]:
            pmt(s, "", True, True)

    if pmt("ZSH for humans?", "zsh"):
        s = str()
        if 'yY' in input("Nerd-Fonts? - this will take a long time (y/N)").lower():
            s += 'git clone https://github.com/ryanoasis/nerd-fonts.git; cd nerd-fonts; ./install.sh;'
        
        s += 'if command -v curl >/dev/null 2>&1; then sh -c "$(curl -fsSL https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"; else sh -c "$(wget -O- https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"; fi;'
        commands += s

    for s in ["cups", "flatpak"]:
        pmt(s, "", True, True)

    if pmt("Is this a server?"):
        pmt("Network server utils? - installdnsmasq dnsutils inetutils nss-mdns", "dnsmasq dnsutils inetutils nss-mdns")

    # Hardware
    if "GenuineIntel" in open("/proc/cpuinfo", "r").read():
        toInstall += " intel-ucode"
    if "AuthenticAMD" in open("/proc/cpuinfo", "r").read():
        toInstall += " amd-ucode"
    if pmt("Nvidia?"):
        toInstall += " nvidia nvidia-utils"
    elif pmt("AMD GPU?"):
        toInstall += " mesa AMDGPU"

    for s in addInstall:
        toInstall += s
    runString = "pacstrap -K /mnt " + toInstall
    print(runString)
    while True:
        inp = input("Continue with this? (y/n)").lower()
        if 'n' in inp:
            exit()
        elif 'y' in inp:
            break

    sp.run(runString.split())
    sp.run('systemctl enable cronie'.split())
    if pmt("Detect other OSes?"):
        sp.run(
            'echo "GRUB_DISABLE_OS_PROBER=false" >> /mnt/etc/default/grub'
            .split())

    sp.run('cd pwd; cp -r ../arch-main-init /mnt/root/arch-main-init'.split())
    sp.run('bash /root/arch-main-init/phase1.sh'.split())
    # Chrooted
    sp.run('cd /root/arch-main-init'.split())
    sp.run('pacman -Syuu'.split())



    if sudo:
        sp.run(
            'sed -i \'s/# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/\' /etc/sudoers'.split())
    else:
        sp.run(
            'echo "permit :wheel" > /etc/doas.conf; echo "yay --sudo doas --save" >> phase2.sh'.split())


    if raid:
        sp.run(
            'mdadm --detail --scan >> /etc/mdadm.conf\
            sed -i \'s/\(?<=^HOOKS\)*.\(filesystems\)/ mdadm_udev filesystems/\' /etc/mkinitcpio.conf\
            sed -i \'s/\(?<=^GRUB_PRELOAD_MODULES\)*.\(part_gpt\)/"part_gpt mdraid09 mdraid1x/\' /etc/default/grub\
            mkinitcpio -P'.split())

    for s in commands:
        runString += s
    sp.run(runString.split())

    print("time to reboot")

main()
