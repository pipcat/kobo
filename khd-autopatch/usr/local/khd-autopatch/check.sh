#!/bin/sh

if [ "$STARTUP" == "1" ]; then
	exit;
fi

DOWNLOADED_ZIP="/mnt/onboard/download.php"

if [ -f $DOWNLOADED_ZIP ]; then
	/usr/local/khd-autopatch/patch.sh $DOWNLOADED_ZIP &
fi
