#!/usr/bin/python2
# -- coding: utf-8 --

# extract/patch nickel css streams. 
# http://www.mobileread.com/forums/showthread.php?t=274813

# By pipcat. Thanks to: Surquizu, GeoffR, tshering, davidfor, mobileread.com


import zlib
import os
import struct
from jsmin import jsmin
import re


def make_executable(path):
	mode = os.stat(path).st_mode
	mode |= (mode & 0o444) >> 2    # copy R bits to X
	os.chmod(path, mode)

def save_file(name, data) :
	f = open(name, 'wb')
	f.write(data)
	f.close()

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

# Get css stream modified by user
def get_changes(pos, found, zlibtype) :
	tosearch = '/* found: %d (%s) pos: %x */\n' % (found, zlibtype, pos)
	pos1 = data_changes.find(tosearch)
	if pos1 == -1:
		return ''
	pos1 += len(tosearch)
	pos2 = data_changes.find('/* found: ', pos1) # find next stream start
	if pos2 == -1:
		pos2 = len(data_changes)
	if data_changes[pos2-2:pos2] == '\n\n':
		pos2 -= 2 # remove \n\n added by extract
	return data_changes[pos1:pos2]

# replaces \n and \t to text
def clean_badeyes(txt):
	#return txt.replace('\n', '\\n').replace('\t', '\\t')
	return txt.encode('string_escape')

# Create patch in bad-eyes format
def fill_badeyes_patch(pos, found, zlibtype, stream, new_stream) :
	action = 'replace_zlib' if zlibtype == 'zlib' else 'replace_string'
	badpos = pos if zlibtype == 'zlib' else pos + 4 # for non-compressed streams, badeyes pos is after four-bytes size.
	patch_badeyes = '<patch>\nname=%X (found %d, %s)\nenabled=true\naction=%s\nposition=autodetect\n' % (badpos, found, zlibtype, action)
	matchObj = re.findall( r'[^\{]*\{[^\}]*\}\n*', stream)
	lines = ''
	for line in matchObj:
		lines += 'oldpart=%s\n' % clean_badeyes(line)
	patch_badeyes += lines
	if new_stream == '':
		patch_badeyes += lines.replace('oldpart=', 'newpart=')
	else:
		matchObj = re.findall( r'[^\{]*\{[^\}]*\}\n*', new_stream)
		for line in matchObj:
			patch_badeyes += 'newpart=%s\n' % clean_badeyes(line)
	patch_badeyes += 'combineparts\n</patch>\n\n'
	return patch_badeyes


# MAIN
# op: 'extract' or 'patch'. op_type: 'css' or 'badeyes'. filename: nickel binaries.
# 'extract' needs => extract_to: css/txt to generate.
# 'patch' needs => filename_patched: nickel/txt to generate. patch_from: css read with modifications.
def zipstreams(op, op_type, filename, extract_to, filename_patched, patch_from) :
	global data_changes

	if op == 'patch':
		with open(patch_from, 'rb') as fh:
			data_changes = fh.read()

	with open(filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	found = 0
	found_zlib = 0
	found_nozlib = 0
	found_modif = 0
	css_all = ''
	while pos < len(data) :
		window = data[pos:pos+2]
		if window == '\x78\x9C':
			try:
				stream = zlib.decompress(data[pos:])
				if stream[0:4] == '\x89PNG':
					ext = '.png'
				elif stream[0:4] == '\x8AMNG':
					ext = '.mng'
				elif stream[0:6] == '\x3C\xB8\x64\x18\xCA\xEF':
					ext = '.qm'
				else:
					stream = stream.decode('utf-8').encode('utf-8') # force error to skip if not string
					if is_css(stream): #guess css code
						found += 1
						found_zlib += 1
						if op == 'extract':
							css_all += '/* found: %d (zlib) pos: %x */\n%s\n\n' % (found, pos, stream) if op_type == 'css' else fill_badeyes_patch(pos, found, 'zlib', stream, '')

						elif op == 'patch':
							stream_modif = get_changes(pos, found, 'zlib')
							if stream_modif != '' and stream_modif != stream:
								print '*) CHANGES IN found: %d (zlib) pos: %x' % (found, pos)
								# compress stream and compare with original length
								stream_compressed = zlib.compress(stream)
								len_stream = len(stream_compressed)
								modif_compressed = zlib.compress(stream_modif)
								len_modif = len(modif_compressed)
								if len_modif > len_stream: # if too big, try to minify
									modif_mini = jsmin(stream_modif)
									mini_compressed = zlib.compress(modif_mini)
									len_mini = len(mini_compressed)
									if len_mini > len_stream:
										print 'ERROR, patch not applied! compressed code after modification and minifization still longer than original.'
										print 'Original size: %d  New size: %d  New minified size: %d' % (len_stream, len_modif, len_mini)
									else:
										print 'css code too long but minified is ok. Reduced %d chars.' % (len_modif - len_mini)
										len_modif = len_mini
										modif_compressed = mini_compressed
										stream_modif = modif_mini

								if op_type == 'badeyes' and len_modif <= len_stream:
									css_all += fill_badeyes_patch(pos, found, 'zlib', stream, stream_modif)
									print 'OK, css stream size is not longer.'
									found_modif += 1
								else:
									if len_modif == len_stream:
										data = data[:pos] + modif_compressed + data[pos+len_stream:]
										print 'OK, compressed code after modification is same size.'
										found_modif += 1
									elif len_modif < len_stream:
										dif_len = len_stream - len_modif
										data = data[:pos] + modif_compressed+('\x00' * dif_len) + data[pos+len_stream:]
										print 'OK, compressed code after modification is shorter. Padded with %d nulls.' % dif_len
										found_modif += 1

			except:
				pos = pos
			
		elif window == '\x00\x00':
			try:
				len_stream = (ord(data[pos+2]) * 256) + ord(data[pos+3])
				if (len_stream > 16 and len_stream < 2000 and data[pos+4+len_stream:pos+4+len_stream+2] == '\x00\x00'): #possible string with css code
					stream = data[pos+4:pos+4+len_stream]
					stream = stream.decode('utf-8').encode('utf-8') # force error to skip if not string
					if is_css(stream): #guess css code
						found += 1
						found_nozlib += 1
						if op == 'extract':
							css_all += '/* found: %d (nozlib) pos: %x */\n%s\n\n' % (found, pos, stream) if op_type == 'css' else fill_badeyes_patch(pos, found, 'nozlib', stream, '')

						elif op == 'patch':
							stream_modif = get_changes(pos, found, 'nozlib')
							if stream_modif != '' and stream_modif != stream:
								print '*) CHANGES IN found: %d (nozlib) pos: %x' % (found, pos)
								# compare with original length
								len_modif = len(stream_modif)
								if len_modif > len_stream: # if too big, try to minify
									modif_mini = jsmin(stream_modif)
									len_mini = len(modif_mini)
									if len_mini > len_stream:
										print 'ERROR, patch not applied! css code after modification and minifization still longer than original.'
										print 'Original size: %d  New size: %d  New minified size: %d' % (len_stream, len_modif, len_mini)
									else:
										print 'css code too long but minified is ok. Reduced %d chars.' % (len_modif - len_mini)
										len_modif = len_mini
										stream_modif = modif_mini

								if op_type == 'badeyes' and len_modif <= len_stream:
									css_all += fill_badeyes_patch(pos, found, 'nozlib', stream, stream_modif)
									print 'OK, css stream size is not longer.'
									found_modif += 1
								else:
									if len_modif == len_stream:
										data = data[:pos+4] + stream_modif + data[pos+4+len_stream:]
										print 'OK, css code after modification is same size.'
										found_modif += 1
									elif len_modif < len_stream:
										dif_len = len_stream - len_modif
										# change bytes size
										data = data[:pos] + struct.pack('>L', len_modif) + stream_modif+('\x00' * dif_len) + data[pos+4+len_stream:]
										print 'OK, css code after modification is shorter. Padded with %d nulls and changed size.' % dif_len
										found_modif += 1

						pos += 4 + len_stream
			except:
				pos = pos

		pos += 1
		if pos >= len(data):
			break

	# Show stats and Save extracted/patched file
	print '\n%d css streams found in %s. (%d in zlib, %d non-compressed)' % (found, filename, found_zlib, found_nozlib)

	if op == 'extract':
		save_file(extract_to, css_all)
		msg = 'Extracted css' if op_type == 'css' else 'Extracted bad-eyes'
		print '%s saved to: %s\n' % (msg, extract_to)

	elif op == 'patch':
		if op_type == 'badeyes':
			save_file(filename_patched, css_all)
			print '%d css streams modified. Patched bad-eyes saved to: %s\n' % (found_modif, filename_patched)
		else:
			save_file(filename_patched, data)
			make_executable(filename_patched)
			print '%d css streams modified. Patched nickel saved to: %s\n' % (found_modif, filename_patched)


# Functions:
SOURCE_NICKEL = 'nickel'
MODIF_NICKEL  = 'nickel-modif'

EXTRACTED_CSS = 'nickel-extracted.css'
MODIFIED_CSS  = 'nickel-modified.css'

EXTRACTED_BADEYES = 'nickel-extracted-badeyes.txt'
MODIFIED_BADEYES  = 'nickel-modified-badeyes.txt'

def extract(filename=SOURCE_NICKEL, extract_to=EXTRACTED_CSS) :
	zipstreams('extract', 'css', filename, extract_to, '', '')

def patch(filename=SOURCE_NICKEL, filename_patched=MODIF_NICKEL, patch_from=MODIFIED_CSS) :
	zipstreams('patch', 'css', filename, '', filename_patched, patch_from)

def extract_badeyes(filename=SOURCE_NICKEL, extract_to=EXTRACTED_BADEYES) :
	zipstreams('extract', 'badeyes', filename, extract_to, '', '')

def patch_badeyes(filename=SOURCE_NICKEL, filename_patched=MODIFIED_BADEYES, patch_from=MODIFIED_CSS) :
	zipstreams('patch', 'badeyes', filename, '', filename_patched, patch_from)
