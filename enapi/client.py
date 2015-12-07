#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,json,requests

from evernote.api.client import EvernoteClient

class EnClient(EvernoteClient):

    #from enapi import EnBook
    _client = None

    @staticmethod
    def get_client(token=None):
        if not EnClient._client:
            if not token: token = token = os.environ.get('EVERNOTE_TOKEN')
            EnClient._client = EnClient(token=token, sandbox=False)
        return EnClient._client

    @staticmethod
    def set_client(client):
        EnClient._client = client

    def __init__(self, **kwargs):

        EvernoteClient.__init__(self, **kwargs)

        self._user_store = None
        self._note_store = None
        self._notebooks = None
        self._stacks = None
        self._guids = None

        EnClient.set_client(self)

    def _initialize(self):
        from enapi import EnBook
        self._notebooks = {}
        self._stacks = {}
        for nb in self.note_store.listNotebooks():
            nb = EnBook.initialize(nb)
            self._notebooks[nb.name] = nb
            if nb.stack:
                if nb.stack not in self._stacks: self._stacks[nb.stack] = []
                self._stacks[nb.stack].append(nb)

    @property
    def user_store(self):
        if self._user_store is None:
            self._user_store = EvernoteClient.get_user_store(self)
        return self._user_store

    @property
    def note_store(self):
        if self._note_store is None:
            self._note_store = EvernoteClient.get_note_store(self)
        return self._note_store

    @property
    def notebooks(self):
        if not self._notebooks:
            self._initialize()
        return self._notebooks

    def notebook(self, name):
        if not self._notebooks:
            self._initialize()
        return self._notebooks.get(name, None)

    def get_note(self, guid, book):
        from enapi import EnNote
        if book:
            return self.notebook(book).get_note(guid)
        else:
            filter = self.note_store.NoteFilter(guid=guid)
            spec = self.note_store.NotesMetadataResultSpec(includeTitle=True,
                                                                includeContentLength=True,
                                                                includeCreated=True,
                                                                includeUpdated=True,
                                                                includeDeleted=True,
                                                                includeTagGuids=True,
                                                                includeAttributes=True)

            nmds = self.note_store.findNotesMetadata(filter, 0, 1, spec).notes
            nmd = EnNote.initialize(nmds[0])
            return nmd

    def delete_note(self,guid):
        self.note_store.deleteNote(guid)

