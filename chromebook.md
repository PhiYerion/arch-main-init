# This is for old school chromebooks, and this is a list of ideas.

## Preformance

### Storage (and RAM)
*General idea is to give a lot of priority to the OS and the /bin files. This should help with responsiveness and speeds while devaluing everything within the /home dir (and maybe others). This will be done with much less compression on the / partition and correspondingly high compression on the /home parition. Additionally, adding more weight to the OS via BFQ will help. The chromebooks I've looked at have low space, and thus even the swap partitions are going to have to be compressed. Storage space and ram amount are much more important considering the limitations.*

**IO**: [BFQ](https://algo.ing.unimo.it/people/paolo/disk_sched/), [params](https://docs.kernel.org/block/bfq-iosched.html) Additionally [tuning generic params](https://wiki.archlinux.org/title/improving_performance#Tuning_I/O_scheduler) can be of use.

 - Low latency for slow drives, so this can help with unresponsiveness. This probably is more important considering the use case
 - Look at ioprio, #4 under params link and [this paper](http://algogroup.unimore.it/people/paolo/disk_sched/bfq-v1-suite-results.pdf)

**Swap**: A partition that for likely-to-be-used that can be tuned for preformance w/ fast compression + a swap file for overflow. Agressive [dirty ratio](https://wiki.archlinux.org/title/Sysctl#Virtual_memory) for actual ram. Increase [swapiness](https://wiki.archlinux.org/title/Swap#Swappiness) for less actual ram usage. Increase [priority](https://wiki.archlinux.org/title/Swap#Priority) for partition 

**Root**: One OS partition (/) and one for home (/home).

 - OS: BTRFS for compression, maybe ext4 (idk if mixing works). noatime, ssd, low zstd, no snap shots, COW, . We can increase the BFQ weight for this aswell.
 - Home: BTRFS. noatime, ssd, medium/high zstd, no snap, COW, . 
 - Debug/tuning: sudo iotop -Padbt 60 > ~/.dbg=disk=usage.txt
 - [tmpfs](https://wiki.archlinux.org/title/Tmpfs) for common applications (google, perhaps) on swapfile
 - Consdier where the steam and lutris game files will be and what compression and BFQ settings should be applied specifically to those directories

**General Compression Notes:**

Due to people probably not going to delete programs and such, perhaps there should be an increase in overall compression when storage space gets low. 

Additionally, last file-open time can be used to determine whether a file should have a high compression value assigned to it. If possible, it would be even more optimal to put 'zombie' files into some larger compressed files for futher space-savings.

### General config
- Adjust nicencess? - [Ananicy](https://github.com/Nefeim4ag/Ananicy)
- Configure make config. Disable mitigations, -03, march=native, mtune=native. Consider size of applications and impact on ram when over-optimizing these values.

### Process Speedup
- ompile applications, can resdistribute across laptops
- irqbalance
- [Disable cpu mitigations](https://wiki.archlinux.org/title/improving_performance#Turn_off_CPU_exploit_mitigations)

### Misc
 - Make sure to incorperate [video drivers](https://wiki.archlinux.org/title/Hardware_video_acceleration)
 - systemd-oomd to configure oom handling more and better than kernel.
 - [disable watchdog](https://wiki.archlinux.org/title/improving_performance#Watchdogs)


### Cleanup
 - use ionice to set to background
 - BTRFS cleanup & compression

## Background Applications/daemons
 - [Wine](https://wiki.archlinux.org/title/wine#Installation), wine-mono, winetricks (and #winetrick --auto-update (arch is outdated, idk why or if this will break something), [Steam](https://wiki.archlinux.org/title/steam), Lutris (autoconfig GE-proton or Caffe or else games will run poorly).
 - Flatpak
 - perhaps [vkd3d-proton](https://github.com/HansKristian-Work/vkd3d-proton). Needs mingw-w64
 - DXVK

## User-facing

### Misc
 - Encryption to make people feel cool and some security

### Desktop
 - Make it look like windows. Maybe XFCE for speed and size, or kde for easier setup and easier to get to look good
 - Rice to max. 

### Applications
 - Google chrome, it's what people are familiar with
 - VPN. Free, probably just protonvpn. Maybe auto generate free account via guerilla mail + VPN/TOR -> outlook email -> protonvpn account

