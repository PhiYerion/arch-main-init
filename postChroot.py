import subprocess as sb
import os.path

sp.run('chmod +x /root/arch-main-init/phase2.sh')
sp.run('pacman -Syuu'.split())
sp.run('bash /root/arch-main-init/phase2.sh')

if os.path.isfile("/etc/sudoers"):
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

print("time to reboot")