#!/bin/bash

su $NEW_USERNAME

dwmDir=/home/$NEW_USERNAME/dwm

git clone https://github.com/phiyerion/dwm $dwmDir
cd $dwmDir
./install.sh
