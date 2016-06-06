# kobo
Tools for Kobo e-readers

## translation-tools
Python scripts to translate Kobo interface.
* Extracts .qm streams from nickel binaries.
* Converts .qm files to .ts files.
* Matching between two .ts files to update changes.
* Interactive script with bin2qm, qm2ts and ts2ts.
* Includes catalan translation.

## patch-nickel-css
Python scripts to extract and patch all css streams inside nickel.
* Extracts css streams (compressed or not) from nickel binaries.
* Patch css streams with your own customizations, minifying them if needed.
* Sample mods and info about css streams.

## kobo-hacks-database
Web site to browse and download hacks and also to manage them.
http://pip.cat/khd
* Contains all metazoa patches from firmware 3.8.0 until last one.
* User register/login to manage your own hacks.
