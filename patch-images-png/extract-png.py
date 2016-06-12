#!/usr/bin/python2
# -- coding: utf-8 --
#
# Extracts png streams from binaries.
#
# By pipcat. Thanks to: Surquizu, GeoffR, tshering, davidfor, mobileread.com

KOBO_FW_FOLDER = '/home/username/kobo/kobo-update-3.19.5761/KoboRoot/usr/local/Kobo/'

PNG_EXTRACT_FOLDER = 'pngs/'
FILENAMES_WITH_SIZE = True  # True: includes width and height in filenames. False: No.

import struct

def save_file(name, data) :
	f = open(name, 'wb')
	f.write(data)
	f.close()
	print 'Saved file '+name

def extract_pngstreams(filename) :
	with open(KOBO_FW_FOLDER+filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	found = 0
	while pos < len(data) :
		if data[pos:pos+8] == '\x89PNG\x0d\x0a\x1a\x0a':
			pos_end = data.find('IEND\xaeB\x60\x82', pos)
			if pos_end != -1:
				found += 1
				if data[pos+12:pos+16] == 'IHDR':
					png_width, png_height, png_bitdepth, png_colortype = struct.unpack('>LLBB', data[pos+16:pos+26])
				else:
					png_width, png_height = (0, 0)
				fn = '%s%s-%04d-%06x-%dx%d.png' % (PNG_EXTRACT_FOLDER, filename, found, pos, png_width, png_height) if FILENAMES_WITH_SIZE else '%s%s-%04d-%06x.png' % (PNG_EXTRACT_FOLDER, filename, found, pos)
				save_file(fn, data[pos:pos_end+8])
				pos = pos_end + 8

		pos += 1
		if pos >= len(data):
			break

	print '%d png streams saved from %s' % (found, filename)

extract_pngstreams('nickel')
extract_pngstreams('libsudoku.so')
extract_pngstreams('librushhour.so')
extract_pngstreams('libcrossword.so')
#~ extract_pngstreams('libchess.so')
