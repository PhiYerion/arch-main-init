#!/bin/python

import subprocess as sp
import os.path

username = os.environ.get('NEW_USERNAME')

def cmd(s, user = False):
    if user:
        sp.run(['runuser', username, '-Pc', s])
    else:
        sp.run(['runuser', '-Pc', s])

cmd('pacman-key --init; pacman-key --populate archlinux; pacman -Syuu')
cmd('chmod +x /root/arch-main-init/phase2.sh')
cmd('bash /root/arch-main-init/phase2.sh')
cmd('git clone https://aur.archlinux.org/paru.git /home/user/paru; cd /home/user/paru; makepkg -si; cd /root/arch-main-init;', True)

print("time to reboot")
