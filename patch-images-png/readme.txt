
Tool to extract and patch png images inside Kobo binaries
=========================================================

- python search.py
	- Edit variable KOBO_FW_FOLDER to fill your path to Kobo firmware files.
	- Execute to find streams in Kobo firmware files.
	- With firmware 3.19.5761 we get this:
	0 zlib streams, 58 png streams. libchess.so
	0 zlib streams, 8 png streams. libcrossword.so
	0 zlib streams, 7 png streams. librushhour.so
	52 zlib streams, 0 png streams. libsolitaire.so
	{'.css': 0, '.mng': 0, '.png': 0, '.txt': 52, '.qm': 0}
	2 zlib streams, 20 png streams. libsudoku.so
	{'.css': 0, '.mng': 0, '.png': 2, '.txt': 0, '.qm': 0}
	43 zlib streams, 1239 png streams. nickel
	{'.css': 25, '.mng': 1, '.png': 4, '.txt': 2, '.qm': 11}

- python extract-png.py
	- Edit variable KOBO_FW_FOLDER to fill your path to Kobo firmware files.
	- Execute to extract png images.

- If you want to modify images, some tips:
	- Edit the png images you want to modify with your preferred software.
	- Don't remove image number and hexadecimal position from images filename (it's needed to find them in binaries when patching!)
	- New png images could not be larger than original ones!
	- Normally you can't change a simple image with a high-resolution photo for example because you are limited by filesize.
	- But you can make some changes if you careful and optimize image.
	- After your changes, use a compressor to reduce image filesize. Ex: compresspng.com optimizepng.com tinypng.com etc...

- nickel images:
	- There are 1.239 png embedded in nickel 3.19.5761
	- Some images are repeated with diferent resolutions for diferent devices.
	- You probably must try-and-hope to locate wich images you need to change for your device.
	- I only changed an image shown on my "About Kobo Glo Hd" (nickel-0375-175c6a.png) with a custom logo, 
	because it was very easy to locate (1 ocurrence with Model N437)

- python patch-png.py
	- Edit variable KOBO_FW_FOLDER to fill your path to Kobo firmware files.
	- Edit variables NEW_IMAGES and calls to patch_pngstreams with your selection.
	- If you already patched nickel, you may want to indicate it in call to patch_pngstreams.
	- Execute to patch png images.

- Execute ./publish.sh to create KoboRoot.tgz, and copy to folder .kobo/ in your device.
	- Edit lines starting with cp $DIR_BINARY/ to select wich files to patch.
