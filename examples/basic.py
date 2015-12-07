#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from enapi import EnClient

en = EnClient.get_client()
print en.user_store.getUser().name

for name in en.notebooks:
    print name

book = en.notebook('Office')
for key in book:
    #note = nmd.get_note()
    #print(nmd.title)
    note = book.get_note(key)
    print(note.title)

guid = '134ca312-f2a0-4f29-a521-aa54245780b7'

note = en.get_note('Office',guid)
pass

#book = en.notebook('OxSync')
#note = book.get_note('XXX')
#pass



#en._initialize()



