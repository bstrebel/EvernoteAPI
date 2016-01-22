#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging
from pyutils import get_logger, LogAdapter
from enapi import *

logger = get_logger('BASIC', logging.DEBUG)
logger.info("Logging initialized ...")
en = EnClient.get_client(logger=logger)

book = en.notebook('OxSync')
exit(0)


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

guid = '25631e18-e2c4-4fcb-8c6a-fdc0e125af35'
note = en.get_note(guid,'OxSync')
props = note.properties()
note = note.load()

title = note['title']
note['title'] = 'NEW'

#tags = note.tags
tags = note['tags']
tags.append('newtag')
note['tags'] = tags



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



