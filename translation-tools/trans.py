#!/usr/bin/python2
# -- coding: utf-8 --

# More info: http://www.mobileread.com/forums/showthread.php?t=261771

# By pipcat & surquizu. Thanks to: tshering, axaRu, davidfor, mobileread.com

import sys
import os.path
import zlib
import codecs, cgi
import xml.etree.ElementTree as ET


# BIN2QM
# ======

def detect_lang(zo) :
	if zo.find('\x00\x41\x00\x67\x00\x72\x00\x65\x00\x67\x00\x61\x00\x64\x00\x6F') != -1:
		return 'mx' #Agregado
	if zo.find('\x00\x41\x00\xF1\x00\x61\x00\x64\x00\x69\x00\x64\x00\x6F') != -1:
		return 'es' #Añadido
	if zo.find('\x00\x53\x00\x65\x00\x63\x00\xE7\x00\xE3\x00\x6F') != -1:
		return 'pt' #Secção
	if zo.find('\x00\x53\x00\x65\x00\xE7\x00\xE3\x00\x6F') != -1:
		return 'br' #Seção
	if zo.find('\x00\x41\x00\x6A\x00\x6F\x00\x75\x00\x74\x00\xE9') != -1:
		return 'fr' #Ajouté
	if zo.find('\x00\x74\x00\x6F\x00\x65\x00\x67\x00\x65\x00\x76\x00\x6F\x00\x65\x00\x67\x00\x64') != -1:
		return 'nl' #toegevoegd
	if zo.find('\x00\x41\x00\x67\x00\x67\x00\x69\x00\x75\x00\x6E\x00\x74\x00\x6F') != -1:
		return 'it' #Aggiunto
	if zo.find('\x00\x68\x00\x69\x00\x6E\x00\x7A\x00\x75\x00\x67\x00\x65\x00\x66\x00\xFC\x00\x67\x00\x74') != -1:
		return 'de' #hinzugef?gt
	if zo.find('\x00\x20\x30\x92\x8F\xFD\x52\xA0\x08\x00') != -1:
		return 'jp' #??
	if zo.find('\x00\x45\x00\x6B\x00\x6C\x00\x65\x00\x6E\x00\x64\x00\x69') != -1:
		return 'tr' #Kitabevi
	return 'en'

def zipstreams(filename, lang_to_save) :
	with open(filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	langs = []

	while pos < len(data) :
		if data[pos:pos+2] == '\x78\x9C':
			try:
				zo = zlib.decompress(data[pos:])
				if zo[0:6] == '\x3C\xB8\x64\x18\xCA\xEF':
					lang = detect_lang(zo)
					langs.append(lang)
					if lang_to_save == lang:
						f = open('temp.qm', 'wb')
						f.write(zo)
						f.close()
						return
			except zlib.error:
				pos = pos
		pos += 1
		if pos == len(data):
			break

	return langs


# QM2TS
# =====

def clean_text(txt, is_utf) :
	if is_utf == False:
		txt = txt.decode('utf-16be').encode('utf-8', 'ignore')
		txt = txt.rstrip() #bypass errors on trans_ca
	else:
		txt = txt.replace('\x20\xB7', '\x20\xC2\xB7') #bypass errors on trans_ca
		txt = txt.replace('\x54\xFC', '\x54\xC3\xBC') #bypass errors on trans_ca
		txt = txt.replace('\x6B\xE7', '\x6B\xC3\xA7') #bypass errors on trans_ca

	txt = cgi.escape(txt)
	return txt

def qm2ts(qm_filename, ts_filename, lang_to_save) :
	with open(qm_filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	found = 0
	last_t3 = ''

	f = open(ts_filename, 'w')
	f.write(codecs.BOM_UTF8)
	f.write('<?xml version="1.0" encoding="utf-8"?>\n')
	f.write('<!DOCTYPE TS>\n')
	la = 'es_MX' if lang_to_save == 'mx' else 'pt_BR' if lang_to_save == 'br' else lang_to_save
	f.write('<TS version="2.1" language="'+la+'">\n')

	while pos < len(data) :
		if data[pos:pos+3] == '\x03\x00\x00':
			l1 = (ord(data[pos+3]) * 256) + ord(data[pos+4])
			t1 = data[pos+5:pos+5+l1]
			t1b = ''
			t1c = ''

			if data[pos+5+l1:pos+5+l1+3] == '\x03\x00\x00': #optional, when exists singular/plural
				l1b = (ord(data[pos+5+l1+3]) * 256) + ord(data[pos+5+l1+4])
				t1b = data[pos+5+l1+5:pos+5+l1+5+l1b]
				pos = pos+l1b+5

			if data[pos+5+l1:pos+5+l1+3] == '\x03\x00\x00': #optional, when exists singular/undecal/plural
				l1c = (ord(data[pos+5+l1+3]) * 256) + ord(data[pos+5+l1+4])
				t1c = data[pos+5+l1+5:pos+5+l1+5+l1c]
				pos = pos+l1c+5

			if data[pos+5+l1:pos+5+l1+8] == '\x08\x00\x00\x00\x00\x06\x00\x00':
				pos = pos+5+l1+8
				l2 = (ord(data[pos]) * 256) + ord(data[pos+1])
				t2 = data[pos+2:pos+2+l2]

				if data[pos+2+l2:pos+2+l2+3] == '\x07\x00\x00':
					pos = pos+2+l2+3
					l3 = (ord(data[pos]) * 256) + ord(data[pos+1])
					t3 = data[pos+2:pos+2+l3]
					found += 1
					
					# save xml
					if last_t3 != t3:
						if last_t3 != '':
							f.write('</context>\n')
						f.write('<context>\n')
						f.write('\t<name>'+t3+'</name>\n')
						last_t3 = t3

					f.write('\t<message>\n') if t1b == '' else f.write('\t<message numerus="yes">\n')
					f.write('\t\t<source>'+clean_text(t2, True)+'</source>\n')
					if t1b == '':
						f.write('\t\t<translation>'+clean_text(t1, False)+'</translation>\n')
					else:
						f.write('\t\t<translation>\n')
						f.write('\t\t\t<numerusform>'+clean_text(t1, False)+'</numerusform>\n')
						f.write('\t\t\t<numerusform>'+clean_text(t1b, False)+'</numerusform>\n')
						if t1c != '':
							f.write('\t\t\t<numerusform>'+clean_text(t1c, False)+'</numerusform>\n')
						f.write('\t\t</translation>\n')
					f.write('\t</message>\n')
					
		pos += 1
		if pos >= len(data):
			break

	if last_t3 != '':
		f.write('</context>\n')
	f.write('</TS>\n')
	f.close()
	return found


# TS2TS
# =====

def find_translation(name, source, plurals):
	numerus = ['', '', '']
	for co2 in root_trans.iter('context'):
		name2 = co2.find('name').text
		if name2 == name:
			for me2 in co2.iter('message'):
				source2 = me2.find('source').text
				if source2 == source:
					if plurals == 'yes':
						i2 = 0
						for nm2 in me2.iter('numerusform'):
							numerus[i2] = nm2.text
							i2 += 1
							if i2 > 2:
								break
						return numerus
					else:
						return me2.find('translation').text

	return '' if plurals == 'no' else numerus

def ts2ts(ts_nickel, ts_trans, ts_save) :
	global root_trans
	tree = ET.parse(ts_nickel)
	root = tree.getroot()

	tree_trans = ET.parse(ts_trans)
	root_trans = tree_trans.getroot()

	found = 0
	no_found = 0
	for co in root.iter('context'):
		name = co.find('name').text
		for me in co.iter('message'):
			source = me.find('source').text

			if me.get('numerus', 'no') == 'yes':
				new_t1 = find_translation(name, source, 'yes')
				i = 0
				for nm in me.iter('numerusform'):
					if i == 0:
						if new_t1[i] == '':
							me.find('translation').set('type', 'unfinished')
							no_found += 1
						else:
							found += 1
					if new_t1[i] != '' and nm.text != new_t1[i]:
						nm.text = new_t1[i]
					i += 1

			else:
				t1 = me.find('translation').text
				new_t1 = find_translation(name, source, 'no')
				
				if new_t1 == '':
					me.find('translation').set('type', 'unfinished')
					no_found += 1
				else:
					found += 1
					if new_t1 != t1:
						me.find('translation').text = new_t1


	tree.write(ts_save)
	return [found, no_found]


# MAIN
# ====

LAST_NICKEL = 'nickel'

# 1: Extract .qm from nickel
# ==========================

if os.path.isfile(LAST_NICKEL) == False:
	sys.exit('nickel not found! Extract it from latest firmware to this folder.')

langs = zipstreams(LAST_NICKEL, '')
if len(langs) == 0:
	sys.exit('No languages found!')

print '%d languages detected. %s' % (len(langs), ', '.join(sorted(langs)))
base_lang = raw_input('Choose a language: ')
if base_lang not in langs:
	sys.exit('Language not available!')

zipstreams(LAST_NICKEL, base_lang)


# 2: Convert .qm to .ts
# =====================

num_strings = qm2ts('temp.qm', 'temp.ts', base_lang)
print '%d strings for language %s' % (num_strings, base_lang)
os.remove('temp.qm')


# 3: Update translations
# ======================
translations_filename = raw_input('If you have translations, enter filename (.qm or .ts): ')
if translations_filename == '':
	new_filename = 'new-trans_'+base_lang+'.ts'
	os.rename ('temp.ts', new_filename)
	sys.exit('Your .ts file is ready to be translated: '+new_filename)

if os.path.isfile(translations_filename) == False:
	if os.path.isfile(translations_filename+'.ts') == True:
		translations_filename += '.ts'
	elif os.path.isfile(translations_filename+'.qm') == True:
		translations_filename += '.qm'
	else:
		os.remove('temp.ts')
		sys.exit('Translation file not found! Copy it to this folder.')

if translations_filename[-3:] == '.qm':
	new_filename = 'new-'+translations_filename[:-3]+'.ts'
	qm2ts(translations_filename, 'temp_trans.ts', base_lang)
	found, no_found = ts2ts('temp.ts', 'temp_trans.ts', new_filename)
	os.remove('temp_trans.ts')
elif translations_filename[-3:] == '.ts':
	new_filename = 'new-'+translations_filename
	found, no_found = ts2ts('temp.ts', translations_filename, new_filename)
else:
	os.remove('temp.ts')
	sys.exit('Translation file must be .qm or .ts!')


os.remove('temp.ts')
print str(found)+' strings found in translation, '+str(no_found)+' not found.'
print 'Your .ts file is ready to be revised: '+new_filename

