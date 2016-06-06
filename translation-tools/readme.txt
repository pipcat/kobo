Python Tools for Kobo Translation
=================================

bin2qm.py => Extracts .qm streams from nickel binaries.
qm2ts.py  => Converts a .qm file to a .ts file.
ts2ts.py  => Matching between two .ts files to update changes.

trans.py  => Interactive script with bin2qm, qm2ts and ts2ts.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions using trans.py:
- Copy nickel and your last translation (if you have one) to your Python Tools folder.
- Execute python trans.py
- With the .ts file you got continue to Step 6

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step by step instructions to translate Kobo interface:

0- You need Python installed and Qt Linguist http://doc.qt.io/

1- Download latest Kobo Firmware (or older if you need)
http://www.mobileread.com/forums/showthread.php?t=185660

2- Extract nickel file from Kobo firmware to your Python Tools folder 
nickel is found at: kobo-update-(version).zip/KoboRoot/usr/local/Kobo/nickel

3- Execute python bin2qm.py to create all .qm files (one for each language)

4- Edit qm2ts.py and write the name of the .qm file you want to convert to .ts file (bottom of code).

5- Execute python qm2ts.py to create the .ts file

6- Edit .ts file manually (it's xml) or with Qt Linguist software.

7- On Qt Linguist release to create .qm file from your modified .ts file.

8- Rename to trans_xx.qm where xx is your two char language code.

9- Pack it in a KoboRoot.tgz at /usr/local/Kobo/translations/ and install as other hacks.


If you already have a translation and want to update it to the latest firmware, you could use ts2ts.py
- After creating .ts file on step 5,
- edit ts2ts.py script and fill 'last_ts_nickel' and 'last_ts_translation' (top of code)
- Execute ts2ts.py to create translated-xxx.ts
- Continue to step 6 with translated-xxx.ts

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update 0.1: 
- Languages with 3 numerus (singular/undecal/plural)
- Language detection (po/br)
- Interactive script trans.py 

Update 0.2:
- Portuguese => pt
- mx => es_MX and br => pt_BR (when creating .ts on trans.py)

