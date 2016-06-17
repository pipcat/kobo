#!/bin/sh

FILES_TO_PATCH="/usr/local/Kobo/libnickel.so.1.0.0 /usr/local/Kobo/libadobe.so /usr/local/Kobo/librmsdk.so.1.0.0"

PATCH32LSB="usr/local/AutopatchKHD/patch32lsb"

AUTOPATCH="/mnt/onboard/.autopatch-khd"
AUTOPATCH_LOGS="$AUTOPATCH/logs"
AUTOPATCH_TODO="$AUTOPATCH/todo"
AUTOPATCH_LAST="$AUTOPATCH/last"
AUTOPATCH_UNINSTALL="$AUTOPATCH/uninstall"

LOG_FILE="$AUTOPATCH_LOGS/$(date +%F).log"

DOWNLOADED_ZIP="/mnt/onboard/download.php"

# -----------------------------------------------------------------------------------

# Functions:

udev_workarounds() {
    # udev kills slow scripts
    if [ "$SETSID" != "1" ]
    then
        SETSID=1 setsid "$0" "$@" &
        exit
    fi
}

suspend_nickel() {
    mkdir /tmp/suspend-nickel && (
        pkill -SIGSTOP nickel
        cat /sys/class/graphics/fb0/rotate > /tmp/rotate-nickel
        nice /etc/init.d/on-animator.sh &
    )
    mkdir /tmp/suspend-nickel/"$1" || exit
}

resume_nickel() {
    rmdir /tmp/suspend-nickel/"$1"
    rmdir /tmp/suspend-nickel && (
        killall on-animator.sh pickle
        cat /tmp/rotate-nickel > /sys/class/graphics/fb0/rotate
        cat /sys/class/graphics/fb0/rotate > /sys/class/graphics/fb0/rotate # 180° fix
        pkill -SIGCONT nickel
    )
}

wait_kobo_ready() {
    for i in $(seq 1 10)
    do
        if [ -e /mnt/onboard/.kobo/KoboReader.sqlite ]
        then
            break
        fi
        sleep 1
    done
}

# Main:

# Pre-process
# -----------
udev_workarounds
suspend_nickel autopatch-khd
wait_kobo_ready

# Main-process
# ------------

# Create necessary folder/files for autopatch-khd (only needed one time)
if [ ! -e "$AUTOPATCH_LOGS" ]
then
    # Autopatch folders:
    mkdir -p "$AUTOPATCH_LOGS" "$AUTOPATCH_TODO" "$AUTOPATCH_LAST"

    # Backup of original binaries if doesn't exists:
    for file in $FILES_TO_PATCH
    do
        fileoriginal="$file"-original
        if [ ! -f "$fileoriginal" ]
        then
            cp "$file" "$fileoriginal"
        fi
    done
fi

# If there is a downloaded zip with patches extract and process
if [ -f "$DOWNLOADED_ZIP" ]
then
    echo "$(date +%c)" &>> "$LOG_FILE"

    rm "$AUTOPATCH_TODO/*.patch"
    rm "$AUTOPATCH_LAST/*.patch"

    unzip -o "$DOWNLOADED_ZIP" *.patch -d "$AUTOPATCH_TODO" &>> "$LOG_FILE"
    rm "$DOWNLOADED_ZIP"

    # Patch binaries or restore original
    for file in $FILES_TO_PATCH
    do
        fileoriginal="$file"-original
        base=$(basename "$file")
        patchtodo="$AUTOPATCH_TODO/$base.patch"
        patchlast="$AUTOPATCH_LAST/$base.patch"
        if [ -f "$patchtodo" ] # apply patch:
        then
            echo '' &>> "$LOG_FILE"
            "$PATCH32LSB" -i "$fileoriginal" -o "$file" -p "$patchtodo" &>> "$LOG_FILE"
            mv "$patchtodo" "$patchlast"
        else # restore if it's not the original:
            cmp --silent "$file" "$fileoriginal" && continue
            cp "$fileoriginal" "$file"
            echo -e "\nRestored original binary $file" &>> "$LOG_FILE"
        fi
    done
    sync
    echo "----------------------------------------" &>> "$LOG_FILE"
fi

# Post-process
# ------------
if [ -e "$AUTOPATCH_UNINSTALL" ]
then
    rm "$AUTOPATCH"
    rm /etc/udev/rules.d/autopatch-khd.rules
    rm -rf /usr/local/AutoPatchKHD
    sync
fi

resume_nickel autopatch-khd
