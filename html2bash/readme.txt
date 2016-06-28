
html2bash
=========

Execute bash scripts from Kobo browser.


INSTALL:
--------

Download provided zip or create a KoboRoot.tgz with:
- /etc/udev/rules.d/99-html2bash.rules
- /usr/local/html2bash/check.sh
- /mnt/onboard/.html2bash/index.html, scripts

- Customize your own scripts editing index.html and scripts folder.
	- You can do that after install, connecting to a computer and going to /mnt/onboard/.html2bash/
	- Copy your own scripts to folder.
	- Edit index.html to modify array BASH_FILES to include your scripts.


USAGE:
------

- Open Kobo browser and go to file:///mnt/onboard/.html2bash/index.html
- Select a script or write your own.
- Press Save file and when download is done, plug Kobo device to usb-charger.
	
- To uninstall:
	- Create an empty html2bash.uninstall in root folder and plug device to usb-charger.


REQUIREMENTS:
-------------

- You need hacks "Allow download all in Browser" and "Allow launching browser without wifi connected".

- You need a usb-charger that doesn't prompt as a computer when plugged. Probably your mobile phone charger is ok.


INFO:
-----

https://github.com/pipcat/kobo/tree/master/html2bash

- Launching html2bash:

Check script is launched when we plug our device to a usb-charger, but not when we plug to a computer.
I tested with a powercube 2A and a Motorola mobile charger .85A, and works nice. But some people reported different benhaviour and when they plug to usb-charger they get prompted as if connected to a computer. In this case, this method is not valid because autopatch will not be trigered, but maybe could be done similar hooking on "usb_host" rather than "usb_plug".
