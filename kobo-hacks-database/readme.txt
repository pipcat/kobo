Kobo Hacks Database (KHD) http://pip.cat/khd
=========================

KHD can be used to browse and download hacks and also to manage them.

Browse hacks:
- Select your Kobo firmware (most recent is selected by default).
- For each hack, this information is displayed:
	- Included in Metazoa pack or found elsewhere.
	- Included in previous firmware or it's a new hack.
	- Multi-version (same patch can be done on different firmwares).
	- Name (if preceded by an icon it's a grouped hack, mutually-exclusive alternatives).
	- Description.
	- Patch code and file to patch.
	- Links to mobileread forums for more info.
	- Checkboxes to enable/select for download.
	- Link to hack details and how user profiles cutomized it.

Download hacks:
- A .zip file is generated with all required .patch files (one for every firmware file to patch).
- You can choose what to include in zip file:
	- .patch files (few KB)
	- .patch files and Tools [patch32lsb for Windows/Linux/Mac] (+/- 500 KB)
	- .patch files, Tools, Firmware [not complete set, but contains all needed files to patch] (+/- 15 MB)
- You can download all hacks (with patch_enable according to checkboxes) or just selected ones.

Manage hacks:
- You need to register your username and login to manage hacks.
- In login form, check "Remember login" to create a permanent cookie to enter directly with your user.
- Custom profiles:
	- Profiles are used to have diferent customizations (Ex: one for Glo Hd, one for Aura H2O, one with differents patches, ...)
	- You have one default profile but you can add more if you need them.
- Upload your own .patch file(s):
	- If you already patched firmware, upload your files (libnickel.so.1.0.0.patch, libadobe.so.patch and librmsdk.so.1.0.0.patch)
	- After upload processing, your selection of hacks enabled or not, and your possible different patch codes are stored in your current profile.
- Besides uploading, you can also customize your hacks from web site:
	- If you check/uncheck a hack, background color changes to yellow, meaning it's your own selection and not the default one (white background).
	- If you modify patch code because some patches requires that to suit your preferences, background color changes to green, meaning patch code is different from default.
	- Checkboxes are directly updated in your profile when you click them, but when you modify patch code in textarea, a buttom will appear to update and you need to click on it to do.
- Transfer hacks selection:
	- This is useful if you change to a new firmware and you want to keep your selected hacks.
	- Your selection of hacks enabled/not enabled will be transfered to another firmware/profile.

Submit hacks:
- This form is only for people who wants to submit new hacks to KHD.
- A small guide of how patch codes are interpreted is shown.
- Paste patch codes and press Analyze to process. You will get a summary of all detected patches.
- Repeat until results are ok for you, and press "Send". 
