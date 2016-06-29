#!/bin/sh

KOBO_CONF="/mnt/onboard/.kobo/Kobo/Kobo eReader.conf"
echo "Disabling screenshots in $KOBO_CONF"
sed 's/^Screenshots=true$/Screenshots=false/g' <"$KOBO_CONF" >"$KOBO_CONF".tmp && mv "$KOBO_CONF".tmp "$KOBO_CONF"
