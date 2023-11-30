# -----------------------------------------------
# Raspberry Pi OS Software Updater
# Downloads New Security Patches and Reboots
# -----------------------------------------------

# Downloads the Latest Updates from the Linux Repositories
apt-get update

# Automatically Upgrades Everything
apt-get upgrade -y

# Tells the Raspberry Pi to Reboot
shutdown -r now
