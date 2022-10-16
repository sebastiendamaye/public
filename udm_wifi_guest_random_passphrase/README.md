# DESCRIPTION

If like me you want to have a guest wifi running on your UDM, with random passphrase that updates every day, then this script might be for you.

# INSTALLATION

If you have a separate server on the same network, where the script can be run, it's fine. Otherwise, you can also install the script on the UDM directly, following the below procedure.

1. Install boostchicken's `on_boot.d` script (https://github.com/boostchicken/udm-utilities/blob/master/on-boot-script/README.md)

2. Download udmwifiguest in `/mnt/data/udmwifiguest` and make sure all files are at the root of this folder

3. Create a folder `/mnt/data/cronjobs` and in that folder create a file for each cron job you want to run. We will only run 1 cronjob (udmwifiguest), so our file will be `/mnt/data/cronjobs/wifiguest` and will have the below contents:

```
0 12 * * * /usr/bin/python3 /mnt/data/udmwifiguest/udmwifiguest.py
```

4. Now in `/mnt/data/on_boot.d/`, create an executable file called `20-add-cronjobs.sh` with the following contents:

```
#!/bin/sh
cp /mnt/data/cronjobs/* /etc/cron.d/
/etc/init.d/crond restart
exit 0
```

On the next UDM reboot, any files added into the cronjobs folder (or modifications to existing files) will get loaded into cron.d.

5. (optional) If you want to send the wifi file over SSH to a remote location, you'll need more steps:

* generate a SSH key in `/mnt/data/udmwifiguest/ssh` as follows:

```
mkdir /mnt/data/udmwifiguest/ssh/
cd /mnt/data/udmwifiguest/ssh/
dropbearkey -f id_rsa -t rsa
chmod 600 id_rsa
```

* Copy the public key to remote location on `~/.ssh/authorized_keys`

* Manual connect once to your remote server, to add it to the `known_hosts` file.

* Make sure this `known_hosts` file will be copied at each reboot by creating `30-copy-known-hosts` in `/mnt/data/on_boot.d`:

```
#!/bin/sh
cp /mnt/data/udmwifiguest/ssh/known_hosts /root/.ssh/
exit 0
```

* create `/mnt/data/cronjobs/udmwifiguest_transfer` with the following contents:

```
1 12 * * * /usr/bin/scp -i /mnt/data/udmwifiguest/ssh/id_rsa -P <whateversshport> /mnt/data/udmwifiguest/wifi user@remoteip:/remote/location
```

