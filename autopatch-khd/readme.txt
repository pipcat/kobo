
AutoPatchKHD
============

Mod of AutoPatch to be used with KHD website.


INSTALL:
--------

Create a KoboRoot.tgz with:
- /etc/udev/rules.d/autopatch-khd.rules
- /usr/local/AutopatchKHD/ patch32lsb, autopatch-khd.sh

If your device does not have the original binaries because you already patched them, include:
- /usr/local/Kobo/ libnickel.so.1.0.0-original libadobe.so-original librmsdk.so.1.0.0-original


USAGE:
------

AutoPatchKHD script is launched when device restarts.
If there is a download.php(.zip) in root folder it will be processed and deleted.

- With internet acces in Kobo device:
	- Open Kobo browser and go to http://pip.cat/khd/kobo 
	- Select a profile for your firmware and download.
	- You can create your own profiles registering at http://pip.cat/khd (not from Kobo device)

- Without internet, connecting with usb cable:
	- Create a .zip file with your .patch files or download it from KHD.
	- Copy to root of device with name download.php(.zip)
	
- After a download.php(.zip) is created, restart Kobo device to apply changes. Info will be at:
	- .autopatch-khd/logs : Log files with patching process messages.
	- .autopatch-khd/last : Last .patch files used to patch binaries.
	- .autopatch-khd/todo : Temporary folder, should be empty after process.

- To restore all original files:
	- Create an empty download.php(.zip) and restart device.

- To uninstall:
	- Create an empty file uninstall in .autopatch-khd folder and restart device.


INFO:
-----

- When AutoPatchKHD processes a zip file containing patches, all binaries (libnickel, libadobe and librmsdk) will be patched or restored.
- So zip file must always contains all patches to do. It's not intented to patch one by one.

- Example, with a zip containing only libnickel.so.1.0.0.patch
	- libnickel will be patched from original, and libadobe and librmsdk will be restored to original if they were modified.


ABOUT:
------

- AutoPatch is a tool created by frostschutz
https://github.com/frostschutz/Kobo

- patch32lsb is an open source program created by GeoffR, used by AutoPatch and Metazoa.

- Metazoa firmware patches are packs of hacks maintained by GeoffR
http://www.mobileread.com/forums/showthread.php?t=260100

- KHD (Kobo Hacks Database) is a website created and maintained by pipcat
http://pip.cat/khd


Other info:
-----------

- Writing udev rules: http://www.reactivated.net/writing_udev_rules.html
