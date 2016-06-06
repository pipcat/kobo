#!/usr/bin/python2
# -- coding: utf-8 --

# Converts a .qm file to a .ts file.
# More info: http://www.mobileread.com/forums/showthread.php?t=261771

# By pipcat & surquizu. Thanks to: tshering, axaRu, davidfor, mobileread.com

import codecs, cgi

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

def qm2ts(filename) :
	with open(filename, 'rb') as fh:
		data = fh.read()

	pos = 0
	found = 0
	last_t3 = ''

	ts_filename = filename+'.ts'
	f = open(ts_filename, 'w')
	f.write(codecs.BOM_UTF8)
	f.write('<?xml version="1.0" encoding="utf-8"?>\n')
	f.write('<!DOCTYPE TS>\n')
	f.write('<TS version="2.1" language="es">\n') #use a language code with singular/plural if needed (Ex: es)

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
	print 'File saved: '+ts_filename+' with '+str(found)+' strings.'

# MAIN
#qm2ts('nickel-3.17.3-8-es.qm')
#qm2ts('nickel-3.19.5761-5-es.qm')
#qm2ts('3.17.3_trans_ca.qm')
#qm2ts('3.19.5761_trans_ca.qm')
qm2ts('nickel-5-es.qm')

