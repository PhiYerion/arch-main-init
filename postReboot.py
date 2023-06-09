#!/bin/python

import subprocess as sp

def main():
    addInstall = []
    def pmt(p, s = str(), defaultY = True, b_install = False):
        inp = input(p.capitalize() + " (Y/n)").lower()
        if defaultY:
            b = 'n' not in inp
        else:
            b = 'y' in inp

        if b:
            if b_install:
                addInstall.append(" " + p)
            else:
                if len(s) > 0:                   # jank
                    addInstall.append(" " + s)
            return True

    def cmd(s, user = False):
        if user:
            sp.run(['runuser', 'user', '-Pc', s])
        else:
            sp.run(['runuser', '-Pc', s])


    if pmt("Games/Emulation? (Wine, proton, steam, lutris)"):
        cmd("sed -zi 's/#\[multilib\]\n#/\[multilib\]\n/)' /etc/pacman.conf")
        cmd('pacman -Sy ttf-liberation lib32-systemd wine wine-gecko wine-mono lib32-alsa-lib lib32-alsa-plugins lib32-libpulse lib32-pipewire pipewire-pulse lib32-libpulse flatpak;\
            pacman -Syuu')
        if pmt("Nvidia?"):
            cmd('pacman -S lib32-nvidia-utils')
        elif pmt("AMD GPU?"):
            cmd('pacman -S lib32-mesa')
            if pmt('display?'):
                cmd('pacman -S xf86-video-amdgpu')
        if pmt("Steam?"):
            cmd('flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo;\
            flatpak --user install flathub com.valvesoftware.Steam;\
            flatpak run com.valvesoftware.Steam', True)
        if pmt("Lutris?"):
            cmd('flatpak install flathub net.lutris.Lutris', True)

    for s in 'ckb-next protonvpn-cli protonvpn google-chrome'.split():
        pmt(s, "", True, True)

    seperator = ' '
    cmd("yay -S" + seperator.join(addInstall), True)

main()
