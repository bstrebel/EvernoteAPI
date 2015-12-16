#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types


import secrets

client = EvernoteClient(token=secrets.dev_token, sandbox=False)

#us = en.get_user_store()
#user = us.getUser()
#info = us.getPremiumInfo()

noteStore = client.get_note_store()
noteBooks = noteStore.listNotebooks()

guids = {}
stacks = {}

for notebook in noteBooks:
    guids[notebook.name] = notebook.guid
    if notebook.stack:
        if notebook.stack not in stacks: stacks[notebook.stack] = []
        stacks[notebook.stack].append(notebook)

for key in guids:
    print key, guids[key]

for stack in stacks:
    print stack, map(lambda nb: nb.name, stacks[stack])

noteFilter = NoteStore.NoteFilter(notebookGuid=guids['Office'])
noteSpec = NoteStore.NotesMetadataResultSpec()

for nmd in noteStore.findNotesMetadata(noteFilter, 0, 10, noteSpec).notes:
    note = noteStore.getNote(nmd.guid, True, False, False, False)






