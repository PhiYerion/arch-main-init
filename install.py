#!/bin/python

import subprocess as sp

def main():
    toInstall = "bash-completion dosfstools linux linux-firmware linux-headers base vim vi grub efibootmgr git reflector python cronie"
    toInstall += " libtool gcc binutils autoconf automake bison file findutils debugedit fakeroot flex libisl libmpc m4 make pkgconf archlinux-keyring rsync patch gettext grep groff pacman texinfo which"   # this instead of base-devel
    addInstall = []
    preCommands = str()
    commands = str()
    raid = False
    sudo = True

    def pmt(prompt, toInstall = str(), defaultY = True, b_install = False):
        if defaultY:
            inp = input(prompt + " (Y/n): ").lower()
            confirm = "n" not in inp
        else:
            inp = input(prompt + " (y/N): ").lower()
            confirm = "y" in inp

        if confirm:
            if b_install:
                addInstall.append(" " + prompt)
            else:
                if len(toInstall) > 0:                      # jank
                    addInstall.append(" " + toInstall)
            return True

    def cmd(command, user = False):
        if user:
            sp.run(["runuser", username, "-Pc", command])
        else:
            sp.run(["runuser", "-Pc", command])

    username = input("What do you want your username to be: ")

    cmd("timedatectl set-ntp true")

    commands += "echo '" + input("What would you like your hostname to be: ") + "' > /etc/hostname;  "

    if input("Doas or Sudo (d/S): ").lower() not in "dD":
        commands += "sed -i 's/# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers;"
        toInstall += " sudo"
    else:
        toInstall += " doas"
        commands += "pacman -Rs sudo; rm /usr/bin/sudo; echo 'permit persist :wheel' > /etc/doas.conf; ln -s /usr/bin/doas /usr/bin/sudo;"
        f = open("postChroot.py", "a")
        f.write("cmd('yay --sudo doas --save; pacman -Rs sudo;')\n")
        f.close()

    if pmt("Are you using mdadm/raid?", "mdadm", False):
        commands += "mdadm --detail --scan >> /etc/mdadm.conf;\
        sed -i 's/\(?<=^HOOKS\)*.\(filesystems\)/ mdadm_udev filesystems/' /etc/mkinitcpio.conf;\
        sed -i 's/\(?<=^GRUB_PRELOAD_MODULES\)*.\(part_gpt\)/\"part_gpt mdraid09 mdraid1x/\" /etc/default/grub;\
        mkinitcpio -P;"

    pmt("Are you going to use nfts?", "ntfs-3g")

    pmt("Virtual machines?", "vde2 virt-manager qemu-base qemu-arch-extra edk2-ovmf bridge-utils")

    pmt("Bluetooth?", "bluez bluez-utils")
    pmt("Wifi?", "wpa_supplicant")
    pmt("Laptop?", "acpi acpi_call tlp acpid")

    if not pmt("Would you like to install more minimal base-devel + my selection? (make, gcc, pacman, cmake already included prior)", "archlinux-keyring gzip plocate"):
        pmt("Then, would you like to install all base-devel?", "archlinux-keyring fakeroot file findutils flex gettext groff gzip libtool m4 patch pkgconf texinfo which")

    if not pmt("My Selection of tools?", "xdg-user-dirs zellij dust nushell lynx wget vnstat tor openbsd-netcat python-pip cronie openssh wireguard-tools htop iotop"):
        if pmt("Would you like to select some instead?"):
            # add aur/surf
            for s in "user-dirs zellij dust nushell lynx wget vnstat tor openbsd-netcat python-pip cronie openssh wireguard htop iotop".split():
                pmt(s)

    if pmt("Do you have a git account?"):
        commands += f"git config --global user.name {input('What is your username: ')}"
        commands += f"git config --global user.email {input('What is your email: ')}"

    if pmt("Firewall?"):
        if not pmt("UFW? (other option is iptables)", "ufw"):
            pmt("iptables-ntf + firewalld?", "iptables-nft ipset firewalld")

    if pmt("Do you want a desktop?)", "xorg xorg-xinit pulseaudio alsa-utils pipewire pipewire-jack piper"):
        if pmt("KDE+Xorg+Wayland support? (Other option is Hyprland + Wayland)", "sddm plasma-desktop konsole plasma-wayland-session"):
            commands += " systemctl enable sddm;"
            if not pmt("Plasma Minimal (plasma-desktop already done)?", "bluedevil drkonqi discover kde-gtk-config khotkeys kpipewire kscreen kscreenlocker ksshaskpass plasma-browser-integration plasma-disks libkscreen plasma-firewall plasma-nm plasma-pa plasma-systemmonitor plasma-vault plasma-workspace plasma-workspace-wallpapers powerdevil sddm-kcm systemsettings"):
                pmt("Plasma group?", "plasma")
            pmt("Plasma Applications?", " kde-applications")
        elif pmt("Hyprland", "hyprpaper waybar xorg-xwayland qt6-wayland qt5-wayland libva gtk-layer-shell egl-wayland kitty"):
            if pmt("nvidia?", "wlroots-nvidia-git hyprland-nvidia"):
                commands += f"echo 'env = XCURSOR_SIZE,24\nenv = LIBVA_DRIVERNAME,nvidia\nenv = XDG_SESSION_TYPE,wayland\nenv = GBM_BACKEND,nvidia-drm\nenv = __GLX_VENDOR_LIBRARY_NAME,nvidia\nenv = WLR_NO_HARDWARE_CURSORS,1\
                >> /home/{username}/.config/hypr/hyprland.conf'"
            else:
                toInstall += "hyprland"
            pmt("Utils?", "imv")
            preCommands += "mv ./hyprland.conf /mnt/root/hyprland.conf"
            commands += f"mkdir --parents /home/{username}/.config/hypr"
            commands += f"mv /root/hyprland.conf /home/{username}/.config/hypr/hyprland.conf"
        else:
            print("Good luck on that.")
        pmt("Basic apps and tools for desktop?", "xdg-utils dolphin filelight")


        for s in "discord element-desktop torbrowser-launcher vlc obs-studio kdenlive".split():
            pmt(s, "", True, True)

    if "yY" in input("Nerd-Fonts? (y/N): ").lower():
        commands += "wget https://raw.githubusercontent.com/PhiYerion/get-nerd-fonts/main/test.py; ./test.py"

    if not pmt("Nushell?", "nushell kitty"):
        if pmt("ZSH for humans?", "zsh"):
            commands += "if command -v curl >/dev/null 2>&1; then sh -c '$(curl -fsSL https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)';\
            else sh -c '$(wget -O- https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)'; fi;"

    for s in ["cups", "flatpak"]:
        pmt(s, "", True, True)

    if pmt("Is this a server?", "", False):
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


    runString = "pacman-key --init; pacstrap -K /mnt " + toInstall + " ".join(addInstall)
    print(runString)
    while True:
        inp = input("Continue with this? (y/n)").lower()
        if "n" in inp:
            exit()
        elif "y" in inp:
            break

    # There is a lot of small things that need to be installed, so setting to 20 for that
    sp.run("sed -i -e 's/# Misc options/# Misc options\\nParallelDownloads = 20/' /etc/pacman.conf", shell=True)
    cmd(runString + "; " + preCommands)
    sp.run("sed -i -e 's/# Misc options/# Misc options\\nParallelDownloads = 10/' /mnt/etc/pacman.conf", shell=True)
    if pmt("Detect other OSes?"):
        commands += "echo 'GRUB_DISABLE_OS_PROBER=false' >> /etc/default/grub"
    cmd("cp -r /root/arch-main-init /mnt/root/arch-main-init")
    f = open("/mnt/root/arch-main-init/phase2.sh", "a")
    f.write(commands)
    f.close()
    cmd(f"genfstab -U /mnt >> /mnt/etc/fstab; arch-chroot /mnt bash -c 'export NEW_USERNAME=\"{username}\"; /root/arch-main-init/postChroot.py'")
    # Chrooted

main()
