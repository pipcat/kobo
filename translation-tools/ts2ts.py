#!/usr/bin/python2
# -- coding: utf-8 --

# Matching between two .ts files to update changes.
# A new file will be created with all strings from 'last_ts_nickel' and translations from 'last_ts_translation'
# Translations not found are marked as "unfinished".
# More info: http://www.mobileread.com/forums/showthread.php?t=261771

# By pipcat & surquizu. Thanks to: tshering, axaRu, davidfor, mobileread.com

last_ts_nickel = 'nickel-5-es.qm.ts'
last_ts_translation  = '3.19.5761_trans_ca.qm.ts'

translated_ts = 'translated-'+last_ts_nickel

# MAIN
import xml.etree.ElementTree as ET

tree = ET.parse(last_ts_nickel)
root = tree.getroot()

tree_trans = ET.parse(last_ts_translation)
root_trans = tree_trans.getroot()


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


tree.write(translated_ts)
print str(found)+' strings found, '+str(no_found)+' not found. Created file: '+translated_ts
