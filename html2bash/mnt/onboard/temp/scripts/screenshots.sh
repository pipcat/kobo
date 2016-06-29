#!/bin/sh

# Change Screenshots=true/false in ﻿[FeatureSettings] for Kobo eReader.conf

KOBO_CONF="/mnt/onboard/.kobo/Kobo/Kobo eReader.conf"

sed 's/^Screenshots=true$/Screenshots=false/g' <"$KOBO_CONF" >"$KOBO_CONF".tmp && mv "$KOBO_CONF".tmp "$KOBO_CONF"
