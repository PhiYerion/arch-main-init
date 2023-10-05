#!/bin/python

import subprocess as sp
import os.path

username = os.environ.get('NEW_USERNAME')

def cmd(s, user = False):
    if user:
        sp.run(['runuser', username, '-Pc', s])
    else:
        sp.run(['runuser', '-Pc', s])

cmd(f"useradd {username} -mG wheel")
cmd('pacman-key --init; pacman-key --populate archlinux; pacman -Syuu')
cmd('chmod +x /root/arch-main-init/phase2.sh')
cmd('bash /root/arch-main-init/phase2.sh')
cmd("rustup default stable", True)
cmd(f'git clone https://aur.archlinux.org/paru.git /home/{username}/paru; cd /home/{username}/paru; makepkg -si;', True)
if os.environ.get('WINDOW_MANAGER') == 'dwm':
    cmd('/root/arch-main-init/dwm_install.sh', True)

print("time to reboot")
