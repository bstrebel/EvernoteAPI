#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests,logging

from enapi import *

logger = logging.getLogger('BASIC')

en = EnClient.get_client(logger=logger)

exit(0)

print en.user_store.getUser().name

title = "Note from python"
content = EnNote.body("Note body ...")
note = EnNote(title=title, content=content)
note = note.create()
print note.edit_url

exit(0)
#note.title = "New note from python"
#note.content = EnNote.body("Note body ...")
#en.note_store.createNote(note)

for name in en.notebooks:
    print name

book = en.notebook('Office')
for key in book:
    #note = nmd.get_note()
    #print(nmd.title)
    note = book.get_note(key)
    print(note.title)

guid = '134ca312-f2a0-4f29-a521-aa54245780b7'

note = en.get_note(guid,'Office')

pass


#book = en.notebook('OxSync')
#note = book.get_note('XXX')
#pass



#en._initialize()



