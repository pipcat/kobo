#!/bin/sh

# ZIP_FILE to process is passed as first parm ($1). Ex: patch.sh /mnt/onboard/download.php

FILES_TO_PATCH="/usr/local/Kobo/libnickel.so.1.0.0 /usr/local/Kobo/libadobe.so /usr/local/Kobo/librmsdk.so.1.0.0"

PATCH32LSB_BIN="usr/local/khd-autopatch/patch32lsb"

AUTOPATCH="/mnt/onboard/.khd-autopatch"
AUTOPATCH_LOGS="$AUTOPATCH/logs"
AUTOPATCH_LAST="$AUTOPATCH/last"
AUTOPATCH_TODO="$AUTOPATCH/todo"
AUTOPATCH_TEMP="$AUTOPATCH/temp"
AUTOPATCH_UNINSTALL="$AUTOPATCH/uninstall"

LOG_FILE="$AUTOPATCH_LOGS/$(date +%F).log"

# -----------------------------------------------------------------------------------

# !? udev_workarounds

# Uninstall / Install
# -------------------
if [ -e "$AUTOPATCH_UNINSTALL" ]; then
	#~ rm -rf "$AUTOPATCH"
	echo "$(date +%c) Uninstalling" >> "$LOG_FILE"
	mv "$AUTOPATCH" "$AUTOPATCH"-delete
	rm /etc/udev/rules.d/99-khd-autopatch.rules
	rm -rf /usr/local/khd-autopatch
	rm "$1"
	sync
	exit;
fi

# Create necessary folders (only needed first time)
if [ ! -e "$AUTOPATCH_LOGS" ]; then
	mkdir -p "$AUTOPATCH_LOGS" "$AUTOPATCH_TODO" "$AUTOPATCH_LAST"
	echo "$(date +%c) Created initial folders" >> "$LOG_FILE"
fi


# Main-process
# ------------

# Check zip file as first parm
if [ "1" == "1$1" ]; then
	echo "$(date +%c) No zip file!" >> "$LOG_FILE"
	exit;
fi

# If there is a downloaded zip with patches extract and process
if [ -f "$1" ]; then
	echo "$(date +%c) Processing $1" >> "$LOG_FILE"

	rm -rf "$AUTOPATCH_TEMP"
	rm -f "$AUTOPATCH_TODO"/*
	rm -f "$AUTOPATCH_LAST"/*

	unzip -o "$1" *.patch -d "$AUTOPATCH_TODO" >> "$LOG_FILE" 2>&1
	rm "$1"

	# Patch binaries or restore original
	for file in $FILES_TO_PATCH; do
		echo '' >> "$LOG_FILE"

		fileoriginal="$file"-original
		if [ ! -f "$fileoriginal" ]; then
			echo "Original binary not found! $fileoriginal" >> "$LOG_FILE"
			continue
		fi
		filemodified="$AUTOPATCH_TEMP$file"
		mkdir -p `dirname $filemodified`
		
		base=$(basename "$file")
		patchtodo="$AUTOPATCH_TODO/$base.patch"
		patchlast="$AUTOPATCH_LAST/$base.patch"
		if [ -f "$patchtodo" ]; then # apply patch:
			"$PATCH32LSB_BIN" -i "$fileoriginal" -o "$filemodified" -p "$patchtodo" >> "$LOG_FILE" 2>&1
			mv "$patchtodo" "$patchlast"
		else # restore if it's not the original:
			cmp "$file" "$fileoriginal" >> "$LOG_FILE" && echo "No need to restore $file" >> "$LOG_FILE" && continue
			cp "$fileoriginal" "$filemodified"
			echo -e "Restoring original binary $fileoriginal" >> "$LOG_FILE"
		fi
		chmod `stat -c %a $file` "$filemodified"
	done
	sync
	echo "----------------------------------------" >> "$LOG_FILE"

	# Create KoboRoot.tgz and force reboot
	tar cvzf /mnt/onboard/.kobo/KoboRoot.tgz --directory=$AUTOPATCH_TEMP ./usr
	rm -rf "$AUTOPATCH_TEMP"
	reboot
fi
