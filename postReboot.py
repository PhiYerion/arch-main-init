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

    if pmt("Games/Emulation? (Wine, proton, steam, lutris)"):
        f = open("/etc/pacman.conf", "a")
        f.write('[multilib]\nInclude = /etc/pacman.d/mirrorlist')
        f.close()
        sp.run('pacman -Sy ttf-liberation lib32-systemd wine wine-gecko wine-mono lib32-alsa-lib lib32-alsa-plugins lib32-libpulse lib32-pipewire pipewire-pulse lib32-libpulse\
            pacman -Syuu'.split())
        if pmt("Nvidia?"):
            sp.run('pacman -S lib32-nvidia-utils'.split())
        elif pmt("AMD GPU?"):
            sp.run('pacman -S lib32-mesa'.split())
            if pmt('display?'):
                sp.run('pacman -S xf86-video-amdgpu'.split())
        if pmt("Steam?"):
            sp.run('pacman -S flatpak;\
            flatpak --user remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo;\
            flatpak --user install flathub com.valvesoftware.Steam;\
            flatpak run com.valvesoftware.Steam'.split())
        if pmt("Lutris?"):
            sp.run('flatpak install flathub net.lutris.Lutris'.split())

    for s in 'ckb-next protonvpn-cli protonvpn google-chrome'.split():
        pmt(s, "", True, True)
