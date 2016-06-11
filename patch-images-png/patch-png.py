#!/usr/bin/python2
# -- coding: utf-8 --
#
# Patch png streams into binaries.
# - new png images could not be larger than original ones!
# - Use a compressor to reduce them if you need. Ex: compresspng.com optimizepng.com tinypng.com etc...
#
# By pipcat. Thanks to: Surquizu, GeoffR, tshering, davidfor, mobileread.com

import os
import zlib
import re

KOBO_FW_FOLDER = '/home/username/kobo/kobo-update-3.19.5761/KoboRoot/usr/local/Kobo/'


def make_executable(path):
	mode = os.stat(path).st_mode
	mode |= (mode & 0o444) >> 2    # copy R bits to X
	os.chmod(path, mode)

def save_file(name, data) :
	f = open(name, 'wb')
	f.write(data)
	f.close()

def patch_pngstreams(filename, new_filename, NEW_IMAGES) :
	with open(KOBO_FW_FOLDER+filename, 'rb') as fh:
		data = fh.read()

	found = 0
	for new_img in NEW_IMAGES:
		if not os.path.isfile(new_img):
			print 'Png image not found! %s' % new_img
			continue
		
		# get pos from filename
		matchObj = re.search( r'-([0-9]{4})-([0-9a-f]{6})', new_img)
		numfound, hexpos = matchObj.groups()
		pos = int(hexpos, 16)

		# get old data from pos
		data_old = ''
		if data[pos:pos+8] == '\x89PNG\x0d\x0a\x1a\x0a':
			pos_end = data.find('IEND\xaeB\x60\x82', pos)
			if pos_end != -1:
				data_old = data[pos:pos_end+8]

		# get new data from file
		with open(new_img, 'rb') as fh:
			data_new = fh.read()
		len_new = len(data_new)

		# check lengths
		len_old = len(data_old)
		if len_old == 0:
			print 'Old png image not found at %x' % pos
		elif len_new == 0:
			print 'Png image empty! %s' % new_img
		elif len_new > len_old:
			print 'ERROR, image too big! %s' % new_img
		else:
			if len_new == len_old:
				data = data[:pos] + data_new + data[pos+len_old:]
			elif len_new < len_old:
				dif_len = len_old - len_new
				data = data[:pos] + data_new + ('\x00' * dif_len) + data[pos+len_old:]
			print 'OK, image patched. %s' % new_img
			found += 1

	patched_file = KOBO_FW_FOLDER+new_filename
	save_file(patched_file, data)
	make_executable(patched_file)
	print '%d png streams modified in %s' % (found, patched_file)


# Fill with file to patch and images:
NEW_IMAGES = [
#	'pngs/compresspng/libsudoku.so-0003-01fdda-new-min.png', 
#	'pngs/compresspng/libsudoku.so-0006-020f88-new-min.png', 
#	'pngs/compresspng/libsudoku.so-0015-022335-new-min.png', 
	'pngs/compresspng/libsudoku.so-0020-0237b6-new-min.png'
]
patch_pngstreams('libsudoku.so', 'libsudoku.so-modif', NEW_IMAGES)

NEW_IMAGES = [
	'pngs/compresspng/nickel-0375-175c6a-new-min.png'
]
#~ patch_pngstreams('nickel-css-modif', 'nickel-css-img-modif', NEW_IMAGES)
patch_pngstreams('nickel', 'nickel-img-modif', NEW_IMAGES)
