#!/usr/local/bin/python
# Author(s): IdleNexus Gaming https://github.com/idlenexusgaming/evetools
# This tool is released under the MIT license. See LICENSE for further details.

###################
# You must change this value before you can use this tool
alliance_name = 'changeme'
###################

import evelink.api
import evelink.eve
from csv import reader
import sys
from os.path import isfile 
import os

if len(sys.argv) == 1:
    print "You must specify a list file as copied from mailing list management"
    sys.exit()

if alliance_name == 'changeme':
    print "You must edit this program and change alliance_name"
    sys.exit()

file_name = sys.argv[1]

if isfile(file_name) and os.access(file_name, os.R_OK):
    with open(file_name,'r') as infile:
        r = reader(infile, delimiter='\t')
        infile.seek(0)
        members = []
        for row in r:
            members.append(row[0])
else:
    print "The file you specified does not exist or is not accessible: argv[1]"
    sys.exit()

c = 1
g = 0
build = ''
nameGroups = [None] * (int(len(members) / 25) + 1)
for index,member in enumerate(members):
    build += member
    if c == 25:
        c = 1
        nameGroups[g] = build
        g += 1
        build = ''
    else:
        build += ','
        c += 1

nameGroups[g] = build[:-1]

idGroups = [None] * len(nameGroups)
api = evelink.api.API()
for index,names in enumerate(nameGroups):
    charIDs = api.get('eve/CharacterID', {'names': names})
    c = 1
    build = ''
    for pilot in charIDs.result.find('rowset').findall('row'):
        charID = pilot.attrib['characterID']
        build += str(charID)
        if c == 25:
            c = 1
            idGroups[index] = build
            build = ''
        else:
            build += ','
            c += 1

idGroups[index] = build[:-1]

for ids in idGroups:
    charAffs = api.get('eve/CharacterAffiliation', {'ids': ids})
    for pilot in charAffs.result.find('rowset').findall('row'):
        name = pilot.attrib['characterName']
        alliance = pilot.attrib['allianceName']
        if alliance != alliance_name:
            if alliance == '':
                alliance = 'No Alliance'
            print name, ' => ', alliance
