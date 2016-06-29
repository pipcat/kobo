#!/bin/sh

KOBO_CONF="/mnt/onboard/.kobo/Kobo/Kobo eReader.conf"
echo "Enabling screenshots in $KOBO_CONF"
sed 's/^Screenshots=false$/Screenshots=true/g' <"$KOBO_CONF" >"$KOBO_CONF".tmp && mv "$KOBO_CONF".tmp "$KOBO_CONF"
