#!/usr/bin/python2
# -- coding: utf-8 --
#
# Analyze files in Kobo Firmware folder to find zlib streams and png streams.
#
# By pipcat. Thanks to: Surquizu, GeoffR, tshering, davidfor, mobileread.com

import os
import zlib

KOBO_FW_FOLDER = '/home/username/kobo/kobo-update-3.19.5761/KoboRoot/usr/local/Kobo/'

# Terminal colors:
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_NC='\033[0m' # No Color

# Check if a stream contains css code
def is_css(stream) :
	open_bracket = stream.find('{')
	close_bracket = stream.find('}')
	two_points = stream.find(':')
	if open_bracket == -1 or close_bracket == -1 or two_points == -1:
		return False
	if close_bracket > open_bracket and two_points > open_bracket and two_points < close_bracket:
		return True
	return False

def zipstreams(filename) :
	with open(KOBO_FW_FOLDER+filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	found = {'zlib': 0, 'png': 0}
	found_zlib = {'.png': 0, '.mng': 0, '.qm': 0, '.txt': 0, '.css': 0}

	while pos < len(data) :
		if data[pos:pos+2] == '\x78\x9C':
			try:
				stream = zlib.decompress(data[pos:])
				if stream[0:4] == '\x89PNG':
					ext = '.png'
				elif stream[0:4] == '\x8AMNG':
					ext = '.mng'
				elif stream[0:6] == '\x3C\xB8\x64\x18\xCA\xEF':
					ext = '.qm'
				else:
					ext = '.css' if is_css(stream) else '.txt'
				found['zlib'] += 1
				found_zlib[ext] += 1
				stream_compressed = zlib.compress(stream)
				len_compressed = len(stream_compressed)
				pos = pos + len_compressed - 1
				
			except zlib.error:
				pos = pos
			
		elif data[pos:pos+4] == '\x89PNG':
			found['png'] += 1

		pos += 1
		if pos >= len(data):
			break

	txt_zlib = '%s zlib streams' % found['zlib']
	colored_txt_zlib = txt_zlib if found['zlib'] == 0 else COLOR_GREEN + txt_zlib + COLOR_NC
	txt_png = '%s png streams' % found['png']
	colored_txt_png = txt_png if found['png'] == 0 else COLOR_GREEN + txt_png + COLOR_NC
	colored_filename = filename if found['zlib'] == 0 and found['png'] == 0 else COLOR_GREEN + filename + COLOR_NC

	print '%s, %s. %s' % (colored_txt_zlib, colored_txt_png, colored_filename)
	if found['zlib'] > 0:
		print found_zlib


for fn in sorted(os.listdir(KOBO_FW_FOLDER)):
	ffn = KOBO_FW_FOLDER+fn
	ext = os.path.splitext(ffn)[1]
	if os.path.isfile(ffn) and not os.path.islink(ffn) and ext not in ['.sh','.txt']:
		zipstreams(fn)
