import subprocess as sp
import os.path

sp.run('chmod +x /root/arch-main-init/phase2.sh'.split())
sp.run('pacman -Syuu'.split())
sp.run('bash /root/arch-main-init/phase2.sh'.split())

print("time to reboot")