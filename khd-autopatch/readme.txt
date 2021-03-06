
khd-autopatch
=============

AutoPatch system to be used with KHD website.


INSTALL:
--------

Create a KoboRoot.tgz with:
- /etc/udev/rules.d/99-khd-autopatch.rules
- /usr/local/khd-autopatch/ patch32lsb, check.sh, patch.sh

Important! you need to include the original binaries of your firmware adding suffix -original:
- /usr/local/Kobo/ libnickel.so.1.0.0-original libadobe.so-original librmsdk.so.1.0.0-original

(it would be nice to find a way to get original binaries automatically, but its a TODO...)


USAGE:
------

- With internet acces in Kobo device:
	- Open Kobo browser and go to http://pip.cat/khd/kobo 
	- Select a profile for your firmware and download.
	- You can create your own profiles registering at http://pip.cat/khd (not from Kobo device)

- Without internet, connecting with usb cable:
	- Create a .zip file with your .patch files or download it from KHD.
	- Copy to root of device with name download.php(.zip)
	
- After a download.php(.zip) is created, plug Kobo device to usb-charger.
	After about 40 seconds, zip file will be processed and deleted and device rebooted to apply changes.
	(40s in a Glo Hd, maybe can take longer on older devices)
	Info about the process will be at:
	- .khd-autopatch/logs : Log files with patching process messages.
	- .khd-autopatch/last : Latest .patch files used to patch binaries.
	- .khd-autopatch/todo : Temporary folder, should be empty after process.

- To restore all original binaries:
	- Create an empty download.php(.zip) in root folder and plug Kobo device to usb-charger.

- To uninstall:
	- Create an empty download.php(.zip) in root folder and an empty file uninstall in .khd-autopatch folder and plug device to usb-charger.


REQUIREMENTS:
-------------

- You need hack "Allow download all in Browser" to download zip files from Kobo browser.

- You need a usb-charger that doesn't prompt as a computer when plugged. Probably your mobile phone charger is ok.

- You are responsible of having need enough disk space to allow patching process.
	(libnickel + libadobe + librmsdk = 23 mb, KoboRoot = 10 mb)


INFO:
-----

- Launching khd-autopatch:

Check script is launched when we plug our device to a usb-charger, but not when we plug to a computer.
I tested with a powercube 2A and a Motorola mobile charger .85A, and works nice.
But some people reported different benhaviour and when they plug to usb-charger they get prompted as if connected to a computer. In this case, this method is not valid because autopatch will not be trigered, but maybe could be done similar hooking on "usb_host" rather than "usb_plug".

- Patching process:

When patch script processes a zip file containing patches, all binaries (libnickel, libadobe and librmsdk) will be patched or restored.
So zip file must always contains all patches to do. It's not intented to patch one by one.

Example, with a zip containing only libnickel.so.1.0.0.patch:
libnickel will be patched from original, and libadobe and librmsdk will be restored to original if they were modified.


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
