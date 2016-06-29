#!/bin/sh

if [ "$STARTUP" == "1" ]; then
	exit;
fi

LOG_FILE="/mnt/onboard/.html2bash/info.log"

TMP_FILE="/mnt/onboard/html2bash.tmp"
if [ -f $TMP_FILE ]; then
	echo "--------------- $(date +%c) ---------------" >> $LOG_FILE

	# If empty file, download failed ;-(
	if [ ! -s $TMP_FILE ]; then
		echo "Empty file. Download was not ok." >> "$LOG_FILE"
	else
		# remove /html2bash.tmp at end of file, save to .sh, set execution flag, run.
		SH_FILE="$TMP_FILE".sh
		sed 's/\/html2bash\.tmp$//g' <$TMP_FILE >$SH_FILE
		chmod +x $SH_FILE
		$SH_FILE >> $LOG_FILE 2>&1 & 
	fi
	rm $TMP_FILE
fi


UNINSTALL_FILE="/mnt/onboard/html2bash.uninstall"
if [ -f $UNINSTALL_FILE ]; then
	echo "$(date +%c) Uninstalling" >> $LOG_FILE
	rm /etc/udev/rules.d/99-html2bash.rules
	rm -rf /usr/local/html2bash
	rm $UNINSTALL_FILE
fi
