#!/bin/sh
#script adapted from following source:
#https://bugs.winehq.org/show_bug.cgi?id=35828

if kdesudo 2>/dev/null; then
    gsu="kdesudo"
else
    gsu="gksudo"
fi

cd /tmp/
wget -qO gte-global.zip https://bugs.winehq.org/attachment.cgi?id=51579
unzip -o gte-global.zip
`$gsu "sh -c 'mkdir -p /usr/local/share/ca-certificates;cp /tmp/gte-global/gte-global.pem /usr/local/share/ca-certificates/gte-global.crt;/usr/sbin/update-ca-certificates'"`
notify-send "Terminé" "Certificat installé. Relancer Origin"
