## ASUS XONAR DG AUTO SWITCHER

If jack audio device connected to front panel: automatically switch to `stereo headphones fp`, if device removed, alsamixer changed to `stereo headphones`.
 
Script worked and tested on Manjaro KDE, KDE Neon, Fedora 39.

## Install
download repository as ZIP and unpack

`sudo mkdir /opt/dgx_auto_switcher`

`sudo cd {path_to}/Asus-Xonar-DG-AutoSwitcher-main`

`sudo chmod +x main.py`

`sudo cp * /opt/dgx_auto_switcher/`

## Systemd
### Create link
`sudo ln -s /opt/dgx_auto_switcher/dgx_auto_switcher.service /etc/systemd/system/dgx_auto_switcher.service`
### Commands
`systemctl daemon-reload`
 
`systemctl start dgx_auto_switcher` 

`systemctl enable dgx_auto_switcher` 

`systemctl disable dgx_auto_switcher` 

`systemctl restart dgx_auto_switcher` 

`systemctl stop dgx_auto_switcher` 

`systemctl status dgx_auto_switcher` 
