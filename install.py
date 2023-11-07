#!/bin/python

import subprocess as sp
import time


# packages return struct


class Handler:
    commands: str
    toInstall: str
    aur_install: str
    preCommands: str
    sudo: str
    username: str
    window_manager: str
    raid: bool
    debug: bool

    def __init__(self):
        baseInstall = "bash-completion linux linux-firmware linux-headers base vim vi grub efibootmgr git reflector"
        # this instead of base-devel
        basicRequired = " libtool gcc binutils autoconf automake bison file findutils debugedit fakeroot flex libisl libmpc m4 make pkgconf archlinux-keyring rsync patch gettext grep groff pacman texinfo which gzip xdg-user-dirs"
        basicPackages = "dhcpcd dosfstools cronie rustup python plocate"

        self.commands = str()
        self.preCommands = str()
        self.toInstall = baseInstall + " " + basicPackages + " " + basicRequired + " "
        self.aur_install = str()
        self.sudo = str()
        self.username = str()
        self.window_manager = str()
        self.raid = False
        if "y" in input("Debug mode? (y/N): ").lower():
            self.debug = True
        else:
            self.debug = False

    def pmt(self, prompt, toInstall=str(), defaultY=True, b_install=False):
        if defaultY:
            if self.debug:
                confirm = True
            else:
                inp = input(prompt + " (Y/n): ").lower()
                confirm = "n" not in inp
        else:
            if self.debug:
                confirm = False
            else:
                inp = input(prompt + " (y/N): ").lower()
                confirm = "y" in inp

        if confirm:
            if b_install:
                self.toInstall += " " + prompt
            else:
                if len(toInstall) > 0:  # jank
                    self.toInstall += " " + toInstall
            return True

    def cmd(self, command, user=False):
        if user:
            return sp.run(["runuser", self.username, "-Pc", command])
        else:
            return sp.run(["runuser", "-Pc", command])

    ###### REQUIRED ######

    def getUser(self):
        self.username = (
            "user" if self.debug else input("What do you want your username to be: ")
        )
        self.commands += (
            "echo '"
            + (
                "host"
                if self.debug
                else input("What would you like your hostname to be: ")
            )
            + "' > /etc/hostname;  "
        )
        if self.pmt("Do you have a git account?"):
            self.commands += (
                f"git config --global user.name {input('What is your username: ')}"
            )
            self.commands += (
                f"git config --global user.email {input('What is your email: ')}"
            )

    def getAuthPackage(self):
        if input("Doas or Sudo (d/S): ").lower() not in "dD":
            self.sudo = "sudo"
            self.commands += "sed -i 's/# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers;"
            self.toInstall += " sudo "
        else:
            self.sudo = "doas"
            self.toInstall += " doas "
            self.commands += "pacman -Rs sudo; rm /usr/bin/sudo; echo 'permit persist :wheel' > /etc/doas.conf; ln -s /usr/bin/doas /usr/bin/sudo;"

    ###### SYS CONFIG ######

    def firewall(self):
        if self.pmt("Firewall?"):
            if not self.pmt("UFW? (other option is iptables)", "ufw"):
                self.pmt("iptables-ntf + firewalld?", "iptables-nft ipset firewalld")

    def getRaid(self):
        if self.pmt("Are you using mdadm/raid?", "mdadm", False):
            self.commands += "mdadm --detail --scan >> /etc/mdadm.conf;\
            sed -i 's/\(?<=^HOOKS\)*.\(filesystems\)/ mdadm_udev filesystems/' /etc/mkinitcpio.conf;\
            sed -i 's/\(?<=^GRUB_PRELOAD_MODULES\)*.\(part_gpt\)/\"part_gpt mdraid09 mdraid1x/\" /etc/default/grub;\
            mkinitcpio -P;"
        else:
            self.raid = False

    ###### TOOLS ######

    def miscTools(self):
        myTools = "xdg-user-dirs zellij dust nushell lynx wget vnstat tor openbsd-netcat python-pip cronie openssh wireguard-tools htop iotop"
        virtualMachines = "vde2 virt-manager qemu-full edk2-ovmf bridge-utils libvirt"
        self.pmt("Are you going to use ntfs?", "ntfs-3g")
        self.pmt("Bluetooth?", "bluez bluez-utils")
        self.pmt("Wifi?", "wpa_supplicant")

        self.pmt("Virtual machines?", virtualMachines)
        self.pmt("Would you like to install all base-devel?", myTools)
        if not self.pmt("My Selection of tools?", myTools):
            if self.pmt("Would you like to select some instead?"):
                # add aur/surf
                for s in myTools.split():
                    self.pmt(s)
        for s in ["cups", "flatpak"]:
            self.pmt(s, "", True, True)

    def cybersec(self):
        msRubyVersion = "ruby-3.0.5"
        if self.pmt("Cybersec tools?"):
            # maltego
            # autopsy forensic browser
            # nikto
            # yersinia
            # Social Engineering Toolkit
            metasploit = " metasploit postgresql  "
            self.aur_install = "skipfish"
            self.toInstall += (
                " radare2 zaproxy wireshark-qt hashcat nmap lynis wpscan aircrack-ng hydra sqlmap "
                + metasploit
            )
            self.commands += f"curl -L get.rvm.io > rvm-install; sudo bash < ./rvm-install; rm -f ./rvm-install; usermod {self.username} -aG rvm; source ~/.rvm/scripts/rvm; cd /opt/metasploit; rvm install {msRubyVersion}; runuser {self.username} -c 'gem install bunder'; runuser {self.username} -c 'bundle install'; cd; runuser {self.username} -c 'initdb -D /var/lib/postgres/data'; systemctl start postgresql; msfdb init --connection-string=postgresql://postgres@localhost:5432/postgres; "

    ###### PERSONAL CONFIG ######

    def personalConfig(self):
        if "yY" in input("Nerd-Fonts? (y/N): ").lower():
            self.commands += "wget https://raw.githubusercontent.com/PhiYerion/get-nerd-fonts/main/test.py; ./test.py"
        if not self.pmt("Nushell?", "nushell kitty"):
            if self.pmt("ZSH for humans?", "zsh"):
                self.commands += "if command -v curl >/dev/null 2>&1; then sh -c '$(curl -fsSL https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)';\
                else sh -c '$(wget -O- https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)'; fi;"

    ##### DEVICE TYPE AND HARDWARE ######

    def laptop(self):
        if self.pmt("Power Management?", "tlp tlp-rdw"):
            self.aur_install += "tlpui"
            self.commands += (
                "systemctl enable tlp.service; systemctl enable tlp-sleep.service;"
            )
        self.pmt("Touchpad?", "xf86-input-libinput")
        self.pmt("Brightness?", "brightnessctl")
        self.pmt("Webcam?", "v4l-utils")
        self.pmt("Power management?", "powertop")

    def server(self):
        self.pmt(
            "Network server utils? - installdnsmasq dnsutils inetutils nss-mdns",
            "dnsmasq dnsutils inetutils nss-mdns",
        )

    def hardware(self):
        if "GenuineIntel" in open("/proc/cpuinfo", "r").read():
            self.toInstall += " intel-ucode"
        if "AuthenticAMD" in open("/proc/cpuinfo", "r").read():
            self.toInstall += " amd-ucode"
        if self.pmt("Nvidia?"):
            self.toInstall += " nvidia nvidia-utils cuda "
        elif self.pmt("AMD GPU?"):
            self.toInstall += " mesa AMDGPU"

    ###### DESKTOPS ######

    def kde(self):
        self.toInstall += " sddm plasma-desktop plasma-wayland-session "
        self.window_manager = "plasma"
        self.commands += " systemctl enable sddm;"
        if self.pmt(
            "My selection of plasma tools and theme?",
            "khotkeys kpipewire kscreen kscreenlocker ksshaskpass plasma-disks libkscreen plasma-firewall plasma-nm plasma-pa plasma-systemmonitor plasma-vault plasma-workspace plasma-workspace-wallpapers powerdevil sddm-kcm systemsettings",
        ):
            self.aur_install += "candy-icons-git"
            self.commands += f"wget 'https://r4.wallpaperflare.com/wallpaper/906/970/555/digital-art-eclipse-clouds-berserk-wallpaper-c970584d01facd0b06a7688f9071767d.jpg' -O /home/{self.username}/Pictures/wallpaper.jpg; cd $(mktemp -d); git clone https://github.com/pwyde/monochrome-kde; cd monochrome-kde; ./install.sh -i; "
        else:
            self.pmt(
                "Plasma Minimal (plasma-desktop already done)?",
                "bluedevil drkonqi discover kde-gtk-config khotkeys kpipewire kscreen kscreenlocker ksshaskpass plasma-browser-integration plasma-disks libkscreen plasma-firewall plasma-nm plasma-pa plasma-systemmonitor plasma-vault plasma-workspace plasma-workspace-wallpapers powerdevil sddm-kcm systemsettings konsole",
            )

        self.pmt("Plasma group?", "plasma")

        self.pmt("Plasma Applications?", " kde-applications")

    def hyprland(self):
        window_manager = "hyprland"
        self.toInstall += "hyprpaper waybar xorg-xwayland qt6-wayland qt5-wayland libva gtk-layer-shell egl-wayland kitty"
        if self.pmt("nvidia?", "wlroots-nvidia-git hyprland-nvidia"):
            self.commands += f"echo 'env = XCURSOR_SIZE,24\nenv = LIBVA_DRIVERNAME,nvidia\nenv = XDG_SESSION_TYPE,wayland\nenv = GBM_BACKEND,nvidia-drm\nenv = __GLX_VENDOR_LIBRARY_NAME,nvidia\nenv = WLR_NO_HARDWARE_CURSORS,1\
            >> /home/{self.username}/.config/hypr/hyprland.conf'"
        else:
            self.toInstall += "hyprland"
        self.pmt("Utils?", "imv")
        self.preCommands += "mv ./hyprland.conf /mnt/root/hyprland.conf"
        self.commands += f"mkdir --parents /home/{self.username}/.config/hypr"
        self.commands += (
            f"mv /root/hyprland.conf /home/{self.username}/.config/hypr/hyprland.conf"
        )

    def dwm(self):
        self.toInstall += "xfce4-panel feh xcompmgr"
        self.window_manager = "dwm"
        print("There will be a custom dwm installed")

    def windowManager(self):
        self.toInstall += (
            " xorg xorg-xinit pulseaudio alsa-utils pipewire pipewire-jack piper "
        )
        if self.pmt("KDE+Xorg+Wayland support? (Other option is Hyprland + Wayland)"):
            self.kde()
        elif self.pmt("Hyprland"):
            self.hyprland()
        elif self.pmt("dwm"):
            self.dwm()
        else:
            print("Good luck on that.")

        self.pmt("Basic apps and tools for desktop?", "xdg-utils dolphin filelight")

        for s in "discord element-desktop torbrowser-launcher vlc obs-studio kdenlive".split():
            self.pmt(s, "", True, True)


def main():
    handler = Handler()
    handler.getUser()
    handler.getAuthPackage()
    handler.hardware()

    # dmidecode --type 3 | grep Type | sed 's/.* //'
    if handler.pmt("Laptop?"):
        handler.laptop()

    if handler.pmt("Server?"):
        handler.server()
    else:
        handler.windowManager()

    handler.firewall()
    handler.getRaid()
    handler.miscTools()
    handler.cybersec()
    handler.personalConfig()

    handler.cmd("timedatectl set-ntp true")

    runString = "pacstrap -K /mnt " + handler.toInstall
    print(runString)

    while True:
        inp = input("Continue with this? (y/n)").lower()
        if "n" in inp:
            exit()
        elif "y" in inp:
            break

    # There is a lot of small things that need to be installed, so setting to 20 for that
    handler.cmd(
        "echo 'Server = http://10.0.2.2/arch-repo/$repo/os/$arch' > /etc/pacman.d/mirrorlist"
    )
    handler.cmd(
        "sed -i -e 's/# Misc options/# Misc options\\nParallelDownloads = 20/' /etc/pacman.conf"
    )
    handler.cmd(
        "sed -i -e 's/\[options\]/\[options\]\\nDisableDownloadTimeout/' /etc/pacman.conf"
    )
    print("starting the range")
    for i in range(10):
        try:
            print(f"run {i}")
            result = handler.cmd(runString)
            break
        except:
            time.sleep(3)
            continue

    handler.cmd(handler.preCommands)
    # sp.run("echo 'DisableDownloadTimeout' >> /mnt/etc/pacman.conf", shell=True)
    sp.run(
        "sed -i -e 's/# Misc options/# Misc options\\nParallelDownloads = 10/' /mnt/etc/pacman.conf",
        shell=True,
    )

    if handler.pmt("Detect other OSes?"):
        handler.commands += "echo 'GRUB_DISABLE_OS_PROBER=false' >> /etc/default/grub"
    handler.cmd("cp -r /root/arch-main-init /mnt/root/arch-main-init")
    f = open("/mnt/root/arch-main-init/phase2.sh", "a")
    f.write(handler.commands)
    f.close()
    print("chrooting...")
    handler.cmd(
        f'genfstab -U /mnt >> /mnt/etc/fstab; arch-chroot /mnt bash -c \'export NEW_USERNAME="{handler.username}"; export SUDO="{handler.sudo}"; export WINDOW_MANAGER="{handler.window_manager}"; /root/arch-main-init/postChroot.py\''
    )
    # Chrooted


main()
