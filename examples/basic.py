#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests,logging

from enapi import *

logger = logging.getLogger('BASIC')
en = EnClient.get_client(logger=logger)

book = en.notebook('OxSync')

# for key in book:
#     note = book.get_note(key).load()
#
#     search = u'Evernote ÄÖÜ'
#     tag = book.get_tag_by_name(search)
#
#     if note.tagGuids:
#         for tag in note.tagGuids:
#             print book.get_tag(tag).decode('utf-8')
#
#     print(note.title.decode('utf-8'))

#print en.user_store.getUser().name

#title = u"Note from python {ÄÖÜ}"
#content = title
#tagNames = [u'.NewTagÄÖÜ']

#if isinstance(title, unicode):
#    title = title.encode('utf-8')

#decoded = []
#for tag in tagNames:
#    decoded.append(tag.encode('utf-8'))

#content = EnNote.body(title)
#note = EnNote(notebookGuid=book.guid, title=title, content=content, tagNames=decoded)
#note = note.create()

guid = '5e60c1f2-f42f-4fcf-9b4f-d07de94a2b08'
note = en.get_note(guid,'OxSync')
note = note.load()

tags = note.tags
note.tagGuids = []

note.tagNames = tags + ['.New2', '.New3']
note = note.update()

print note.tagGuids


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



