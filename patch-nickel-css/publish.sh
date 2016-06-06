#!/bin/sh

# Creates KoboRoot.tgz with patched nickel

NEW_NICKEL=nickel-modif

SOURCE_DIR=temp-source
DEST_DIR=$SOURCE_DIR/usr/local/Kobo

echo "Creating KoboRoot.tgz ..."

mkdir -p $DEST_DIR
cp $NEW_NICKEL $DEST_DIR/nickel

tar cvzf KoboRoot.tgz --directory=$SOURCE_DIR ./usr

echo "Created KoboRoot.tgz"
rm -rf $SOURCE_DIR
