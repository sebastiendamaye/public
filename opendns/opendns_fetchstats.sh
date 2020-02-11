#!/bin/bash

USERNAME="************" # me@domain.com
NETWORK_ID="**********" # https://dashboard.opendns.com/stats/***NETWORKID***/topdomains/today/
PASSWORD="************" # escape special chars with backslah (e.g. "$" should be "\$")
DATE=`date -d "-1 day" +%Y-%m-%d` # yesterday

CSVURL="https://dashboard.opendns.com"
LOGINURL="https://login.opendns.com/?source=dashboard"

USERNAME=`echo -n "$USERNAME" | od -A n -t x1 | tr -d '\n' | sed 's/ *$//;s/[ ]\{1,\}/%/g'`

COOKIEJAR=`mktemp /tmp/opendns-fetchstats-XXXXXX`

# Get the signin page's form token
FORMTOKEN=`curl --silent --insecure \
	--cookie-jar "$COOKIEJAR" \
	"$LOGINURL" \
	| grep -m 1 formtoken \
	| sed 's/^.*name="formtoken" value="\([0-9a-f]*\)".*$/\1/' \
`

# Sign into OpenDNS
SIGNIN=`curl --silent --insecure \
	--cookie "$COOKIEJAR" \
	--cookie-jar "$COOKIEJAR" \
	--data "formtoken=$FORMTOKEN&username=$USERNAME&password=$PASSWORD&sign_in_submit=foo" \
	"$LOGINURL" \
	| grep "Logging you in"
`

#if [ "$SIGNIN" == "" ]; then
#	echo "Login failed.  Check username and password." >&2
#	exit 2
#fi

# Fetch pages of Top Domains
GO="yes"
PAGE=1
while [ "yes" == "$GO" ] ; do
	CSV=`curl --silent --insecure \
		--cookie "$COOKIEJAR" \
		"$CSVURL/stats/$NETWORK_ID/topdomains/$DATE/page$PAGE.csv" \
	`
	if [ "$PAGE" == "1" ]; then
		if [ "$CSV" == "" ]; then
			echo "You can not access $NETWORK_ID" >&2
			exit 2
		fi
		HEADING=`echo "$CSV" | head -n 1`
		if [[ "$HEADING" == *DOCTYPE* ]]; then
		    echo "Error retrieving data.  Date range may be outside of available data." >&2
	        exit 2
		fi
	else
		CSV=`echo "$CSV" | tail -n +2`
	fi

	if [ -z "$CSV" ] ; then GO="no"
	else echo "$CSV" ; fi
	PAGE=$(($PAGE + 1))
done

rm -f "$COOKIEJAR"

