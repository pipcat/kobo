#!/usr/bin/python2
# -- coding: utf-8 --

# Extracts all .qm streams from nickel binaries.
# More info: http://www.mobileread.com/forums/showthread.php?t=261771

# Get 'nickel' file from latest firmware release. Ex: kobo-update-3.19.5671.zip/KoboRoot/usr/local/Kobo/nickel
# More info: http://www.mobileread.com/forums/showthread.php?t=185660

# By pipcat & surquizu. Thanks to: tshering, axaRu, davidfor, mobileread.com

import zlib

def save_file(name, data) :
    f = open(name, 'wb')
    f.write(data)
    f.close()
    print 'File saved: '+name

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

def zipstreams(filename) :
    with open(filename, 'rb') as fh:
        data = fh.read()

    pos = 0
    found = 0

    while pos < len(data) :
        if data[pos:pos+2] == '\x78\x9C':
            try:
                zo = zlib.decompress(data[pos:])
                if zo[0:6] == '\x3C\xB8\x64\x18\xCA\xEF':
                    found += 1
                    lang = detect_lang(zo)
                    save_file(filename+'-'+str(found)+'-'+lang+'.qm', zo)
            except zlib.error:
                pos = pos
        pos += 1
        if pos == len(data):
            break

#zipstreams('nickel-3.17.3')
#zipstreams('nickel-3.18.0')
#zipstreams('nickel-3.19.5613')
#zipstreams('nickel-3.19.5761')
zipstreams('nickel')


