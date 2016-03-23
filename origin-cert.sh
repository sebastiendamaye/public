#!/bin/sh
"""
script adapted from following source:
https://bugs.winehq.org/show_bug.cgi?id=35828
"""
if [[ $EUID -ne 0 ]]; then
	echo "You need to be root to run this script."
	exit 1
fi

wget -qO /tmp/gte-global.zip https://bugs.winehq.org/attachment.cgi?id=51579
unzip /tmp/gte-global.zip
mkdir -p /usr/local/share/ca-certificates
cp /tmp/gte-global.pem /usr/local/share/ca-certificates/gte-global.crt
update-ca-certificates
echo "Certificat installé. Relancer Origin"
