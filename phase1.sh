#!/bin/bash

genfstab -U /mnt >> /mnt/etc/fstab
arch-chroot /mnt
