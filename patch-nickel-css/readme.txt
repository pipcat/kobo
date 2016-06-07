
Tool to patch css styles inside nickel
======================================

- Copy your nickel file from your firmware to this folder.

- Execute python extract.py to extract all css streams to nickel-extracted.css
	With firmware 3.19.5761 there are 39 css streams (25 compressed, 14 .css non-compressed).

- Edit nickel-extracted.css, change what you want and save as nickel-modified.css
	Each css stream starts with a header like /* found: n (zlib/nozlib) pos: hex */
	Don't modify streams headers lines! Add your comments/changes in next lines.

	Your nickel-modified.css can contain only your modified streams or the whole streams.
	You can change streams order to organize them to your needs.

	Note that replaced css code could not be larger than original one.
	If your code is larger it will be minified to try to suit.
	Remove code related to other devices if you still need to shorten.

- Execute python patch.py to create a nickel-modif with your patches.
	Check messages to verify modifications are well done.

- Execute ./publish.sh to create KoboRoot.tgz, and copy to folder .kobo/ in your device.
	For windows it should be a publish.bat (if you can do, please post it to include ;-)


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nickel-modified-myglohd.css is an example with some customizations for a Kobo Glo Hd.
- /* [MOD]: Enabled games in Beta features */
- /* [MOD]: Increased dictionary view */
- /* [MOD]: Removed cover border in small thumbnails (recent and new books) */
- /* [MOD]: Removed cover border in most recent book thumbnail */
- /* [MOD]: Removed cover border in small thumbnails (added to library) */

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Info about streams in firmware 3.19.5761:
http://www.mobileread.com/forums/showpost.php?p=3328586&postcount=2

/* found: 1 (zlib) pos: 49ebf4 */    : the longer stream (41,7 kb). (entities)
/* found: 2 (zlib) pos: 49fbf7 */    : (generic classes)
/* found: 3 (zlib) pos: 4a002b */    : font sizes only for qApp_deviceIsAlyssum (Glo Hd).
/* found: 9 (zlib) pos: 4a0b96 */    : (smaller other recent book tiles, SmallRecentBookTile)
/* found: 12 (zlib) pos: 4a1388 */   : related to Beta features (to enable/disable games).
/* found: 15 (zlib) pos: 4a17bd */   : (Library recent books tile ,bookCoverListTile).
/* found: 16 (nozlib) pos: 4a192a */ : #InlineDictionaryView (to increase frame size)
/* found: 28 (zlib) pos: 4a3061 */   : (biggest most recent book tile, RecentBookTile)
/* found: 31 (zlib) pos: 4a39b1 */   : (PocketRecentlyReadTile)
/* found: 39 (nozlib) pos: 4a47b9 */ : (PhoenixSmallRecentBookTile)
... 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Notes:

Some css code are applyed depending of your device type. For example:
- Glo Hd : qApp_deviceIsDragon="true", qApp_deviceIsAlyssum="true"

If you have another device, and you want to know wich conditions are done:
- a) in your nickel-modified.css, locate /* found: 12 (zlib) pos: 4a1388 */ and replace content with:
- b) or create an empty nickel-modified.css, add a first line with /* found: 12 (zlib) pos: 4a1388 */ and add content:
#spacerWidget,
#description {
  padding-right: 12px;
  padding-top: 12px;
}
#boggleContainer,
#solitaireContainer,
#rushHourContainer,
#browserContainer,
#sudokuContainer,
#sketchPadContainer {
  qproperty-bottomMargin: 10;
}
#boggleDescription,
#solitaireDescription,
#rushHourDescription,
#browserDescription,
#sudokuDescription,
#scribbleDescription {
  padding-top: 12px;
  padding-bottom: 12px;
}
/* To test which conditions are set on a device:  */
#boggleContainer[qApp_deviceIsTrilogy="true"] { qproperty-visible: false; }
#solitaireContainer[qApp_deviceIsPhoenix="true"] { qproperty-visible: false; }
#rushHourContainer[qApp_deviceIsDragon="true"] { qproperty-visible: false; }
#browserContainer[qApp_deviceIsAlyssum="true"] { qproperty-visible: false; }
#sudokuContainer[qApp_deviceIsPika="true"] { qproperty-visible: false; }
#sketchPadContainer[qApp_deviceIsTrilogy="true"] { qproperty-visible: false; }

- After patching your device, go to Beta Features, and check wich games you can't see.
If you can't see a game, his condition qApp_deviceIs... is accomplished.
If you post your device conditions, i will update this information.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Changes log:

v01:
- http://www.mobileread.com/forums/showpost.php?p=3327984&postcount=229

v02:
- http://www.mobileread.com/forums/showthread.php?t=274813
- Extract and patch also non-compressed css code.
- Added jmin to minify css code.
	https://pypi.python.org/pypi/jsmin

v03:
- Manage all css streams in one single file.
- Unified code for extracting and patching in a function.
