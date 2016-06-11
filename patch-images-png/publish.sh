#!/bin/sh

# Creates KoboRoot.tgz with patched file

DIR_BINARY='/home/username/kobo/kobo-update-3.19.5761/KoboRoot/usr/local/Kobo'

SOURCE_DIR=temp-source
DEST_DIR=$SOURCE_DIR/usr/local/Kobo

echo "Creating KoboRoot.tgz ..."

mkdir -p $DEST_DIR

cp $DIR_BINARY/libsudoku.so-modif $DEST_DIR/libsudoku.so
cp $DIR_BINARY/nickel-modif $DEST_DIR/nickel

# To restore original files: 
#cp $DIR_BINARY/libsudoku.so $DEST_DIR/libsudoku.so
#cp $DIR_BINARY/nickel $DEST_DIR/nickel

tar cvzf KoboRoot.tgz --directory=$SOURCE_DIR ./usr

echo "Created KoboRoot.tgz"
rm -rf $SOURCE_DIR
