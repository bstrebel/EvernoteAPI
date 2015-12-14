#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, re, requests, logging
from pyutils import LogAdapter

from evernote.api.client import EvernoteClient

class EnClient(EvernoteClient):

    #from enapi import EnBook
    _client = None

    @staticmethod
    def get_client(token=None, logger=None):
        if not EnClient._client:
            if not token: token = os.environ.get('EVERNOTE_TOKEN')
            # if not logger: logger = logging.getLogger('enapi')
            EnClient._client = EnClient(token=token, sandbox=False, logger=logger)
        return EnClient._client

    @staticmethod
    def set_client(client):
        EnClient._client = client

    def __init__(self, **kwargs):
        EvernoteClient.__init__(self, **kwargs)

        self._user_store = None
        self._note_store = None
        self._notebooks = None
        self._books = None
        self._stacks = None
        self._user = None
        self._guids = None

        if kwargs.get('logger') is None: self._logger = logging.getLogger('enapi')
        else: self._logger = kwargs.get('logger')
        self._adapter = LogAdapter(self._logger, {'package': 'enapi'})

        self.logger.debug("Evernote client initialized")
        EnClient.set_client(self)

    @property
    def logger(self): return self._adapter

    @property
    def service(self):
        if self.sandbox:
            return 'sandbox.evernote.com'
        else:
            return 'www.evernote.com'

    @property
    def user_id(self):
        #return self._user_store.userId()
        pass

    def __initialize(self):
        from enapi import EnBook
        try:
            self._notebooks = {}
            self._books = {}
            self._stacks = {}
            for nb in self.note_store.listNotebooks():
                nb = EnBook.initialize(nb)
                self._notebooks[nb.name] = nb
                self._books[nb.guid] = nb
                if nb.stack:
                    if nb.stack not in self._stacks: self._stacks[nb.stack] = []
                    self._stacks[nb.stack].append(nb)
        except Exception, e:
            self.logger.exception(e)

    @property
    def user_store(self):
        if self._user_store is None:
            self._user_store = EvernoteClient.get_user_store(self)
        return self._user_store

    @property
    def user(self):
        if self._user is None:
            self._user = self.user_store.getUser()
        return self._user

    @property
    def note_store(self):
        if self._note_store is None:
            self._note_store = EvernoteClient.get_note_store(self)
        return self._note_store

    @property
    def notebooks(self):
        if not self._notebooks:
            self.__initialize()
        return self._notebooks

    def notebook(self, name):

        if not self._notebooks:
            self.__initialize()

        if re.match('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', name):
            return self._books.get(name)

        return self._notebooks.get(name)

    def get_note(self, guid, book=None):
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

    def delete_note(self, note):
        if not isinstance(note, str):
            note = note.guid
        self.note_store.deleteNote(note)

    def create_note(self, note, book=None):
        from enapi import EnNote
        if book:
            note.notebookGuid = self.notebook(book).guid

        return(EnNote.initialize(self.note_store.createNote(note.encoded)))

    def update_note(self, note):
        try:
            note = self.note_store.updateNote(note.encoded)
            return note
        except Exception, e:
            self.logger.exception(e)
            return None

