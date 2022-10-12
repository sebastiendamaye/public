# DESCRIPTION

If like me you want to have a guest wifi running on your UDM, with random passphrase that updates every day, then this script might be for you.

# INSTALLATION

If you have a separate server on the same network, where the script can be run, it's fine. Otherwise, you can also install the script on the UDM directly, following the below procedure.

1. Install boostchicken's `on_boot.d` script (https://github.com/boostchicken/udm-utilities/blob/master/on-boot-script/README.md)

2. Download udmwifiguest in `/mnt/data/udmwifiguest` and make sure all files are at the root of this folder

2. Create a folder `/mnt/data/cronjobs` and in that folder create a file for each cron job you want to run. We will only run 1 cronjob (udmwifiguest), so our file will be `/mnt/data/cronjobs/wifiguest` and will have the below contents:

  0 12 * * * /usr/bin/python3 /mnt/data/udmwifiguest/udmwifiguest.py

3. Now in `/mnt/data/on_boot.d/`, create an executable file called `20-add-cronjobs.sh` with the following contents:

  #!/bin/sh
  cp /mnt/data/cronjobs/* /etc/cron.d/
  /etc/init.d/crond restart
  exit 0

On the next UDM reboot, any files added into the cronjobs folder (or modifications to existing files) will get loaded into cron.d.
